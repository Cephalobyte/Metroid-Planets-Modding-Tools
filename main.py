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
	'quit':'Done for now?'
}

while True:
	match getOptionDialog(
		'What would you like to do?', mainOptions, otherOptions
	):
		case 0:
			import modules.world2json
		case 1:
			import modules.json2world
		case 'quit':
			print('See you next Mission!')
			break

pE2C()