from os import system

from modules.utils import *

mainOptions = [
	'Import a world (world to json)',	#0
	'Export a world (json to world)',	#1
	# 'Import a room (room to json)',	#2
	# 'Export a room (json to room)',	#3
	# 'Import a save (save to json)',	#4
	# 'Export a save (json to save)',	#5
]
otherOptions = {
	# 'prefs':'Manage your preferences',
	'preview':'Generate ASCII art from your world or json file and save them in a txt file',
	'quit':'Done for now?'
}


def main():
	while True:
		match getOptionDialog(
			'What would you like to do?', mainOptions, otherOptions
		):
			case 0:
				from modules.world2json import world2json
				world2json()
			case 1:
				from modules.json2world import json2world
				json2world()
			case 2:
				from modules.room2json import room2json
				room2json()
			case 'preview':
				from modules.previewGenerator import previewGenerator
				previewGenerator()
			case 'quit':
				print('See you next Mission!')
				break


if __name__ == '__main__':
	system('cls')	#allows ANSI escape sequences

	main()	#run program

	pE2C()