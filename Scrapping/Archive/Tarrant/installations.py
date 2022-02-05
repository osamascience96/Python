import subprocess
import sys

class Install():
	def __init__(self):
		if __name__=='__main__':
			with open('requirements.txt', 'r') as file:
				file = file.read().splitlines()

			for pack in file:
				subprocess.check_call([sys.executable, "-m", "pip", "install", pack])

if __name__=='__main__':
	Install()