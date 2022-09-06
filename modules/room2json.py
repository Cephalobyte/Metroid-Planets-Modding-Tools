from os import system

try: from modules.utils import *
except: from utils import *


def sortScreenProps(screen:dict, props:dict, tileMain:dict, tileBack:dict, tileFront:dict, tileLiquid:dict):
	screen.clear()
	for data in [
		["BLOCKS", [
			['type','x','y'],
		]],
		["DOORS", [
			['type'],
			['color','x','y'],
			['pos']
		]],
		["ELEVATORS", [
			['type','x','y']
		]],
		["ENEMIES", [
			['n','type','x','y'],
			['rot'],
			['dir'],
			['lock']
		]],
		["ITEMS", [
			['type','x','y']
		]]
	]:
		for stuff in props[data[0]]:
			stuf2 = stuff.copy()
			stuff.clear()
			stuff.update(sortDictPriority(stuf2, data[1]))
	
	screen.update(sortDictPriority(props, [
		['x','y'],
		['area'],
		['scroll_l','scroll_u'],
		['scroll_r'],
		['scroll_d']
	]))
	screen.update(tileMain)
	screen.update(tileBack)
	screen.update(tileFront)
	screen.update(tileLiquid)


def sortScreens(screens:dict, tileM:int):
	for screen in screens:
		if isinstance(screen, (float, int)): continue	#if screen is "disabled", ignore

		props = dict([(p,screen[p]) for p in screen if p[:3] not in ['tm_','tb_','tf_','tl_']])
		tileMain = sortTiles(screen,'tm_',tileM)
		tileBack = sortTiles(screen,'tb_',tileM)
		tileFront = sortTiles(screen,'tf_',tileM)
		tileLiquid = sortTiles(screen,'tl_',tileM)
		sortScreenProps(
			screen,
			props,
			tileMain,
			tileBack,
			tileFront,
			tileLiquid
		)


def room2json():
	roomFileIn, roomFileOut = getInOutFileDialog('room','json')

	roomDict = openRoom(roomFileIn)

	tileMode = getOptionDialog(	#choose tile display mode
		'Choose tile number display mode',
		[
			'raw mode - return the original number <float>',
			'binary mode - (default) return the binary equivalent separated each 4 characters <string>',
			'simple mode - return a simplified representation of values (not recommended as it is incomplete) <string>.\n      The 4 numbers for tile numbers are : Id, Palette Id, Animated Palette Offset, Transform\n    The 4 numbers for liquid numbers are : Id, Unknown Number, Liquid Set Id, Transform',
		],
		defau=1
	)

	colMode = getOptionDialog(
		'Choose palette color display mode',
		[
			'raw mode - return the original number <int>',
			'hexadecimal mode - (default) return the hex color code equivalent <string>'
		],
		defau=1
	)

	progress('IMPORTING ROOM')	#-------------------------------------------------

	#------ Sorting --------------------------------------------------------------

	progress('SORTING KEYS')	#---------------------------------------------------
	
	roomDict = dict(sorted(roomDict.items()))
	for data in [
		["GENERAL", [
			['room_name'],
			['designer_name','difficulty','variant'],
			['loc_custom_1','loc_custom_1_name','loc_custom_2','loc_custom_2_name']
		]],
		["META DATA", [
			['id_key','last_save','studio_version'],
			['patch_A','patch_B','patch_C','patch_D'],
			['user_room'],
			['playable'],
		]],
	]:
		roomDict[data[0]] = sortDictPriority(roomDict[data[0]],data[1])

	for stuff in roomDict["PATHING"]:
		stuf2 = stuff.copy()
		stuff.clear()
		stuff.update(sortDictPriority(stuf2, [
			['start'],
			['end']
		]))

	#------ Sort & Readability ---------------------------------------------------

	progress('SORTING SCREENS')	#-------------------------------------------------

	sortScreens(roomDict['SCREENS'], tileMode)

	if colMode > 0:	#if not raw mode

		progress('TRANSLATING PALETTES')

		for p, pal in enumerate(roomDict["PALETTES"]):	#go through each palette...
			for c,col in enumerate(pal[2:]):							#each color...
				roomDict["PALETTES"][p][c+2] = gmdecc2Hexc(col)

	progress('SAVING ROOM')	#---------------------------------------------------

	writeJson(roomFileOut, roomDict)	#write to the json file

	progress('ROOM IMPORTED!',True)	#-------------------------------------------

	# if getYesNoDialog('Preview the room?', defau=True):

	# 	try: from modules.previewGenerator import prevMinimap
	# 	except: from previewGenerator import prevMinimap

	# 	preview = prevMinimap(
	# 		roomDict["SCREENS"],
	# 		int(roomDict["GENERAL"]["room_w"]),
	# 		int(roomDict["GENERAL"]["room_h"]),
	# 		roomDict["ELEVATORS"],
	# 		roomDict["ITEMS"],
	# 		roomDict["GENERAL"]["spawns"]
	# 	)

	# 	prevFileOut = roomFileIn.removesuffix('room') + 'prevMM.txt'
	# 	if getYesNoDialog(
	# 		'Save to text file?',
	# 		['Will be saved as :\n'+prevFileOut],
	# 		False
	# 	):

	# 		progress('SAVING MINIMAP')	#---------------------------------------------

	# 		writeTxt(prevFileOut, preview)

	# 		progress('PREVIEW SAVED!',True)	#-----------------------------------------


if __name__ == '__main__':	#if module was run
	system('cls')	#allows ANSI escape sequences

	room2json()	#run module

	while getYesNoDialog(
		'Another?',
		defau = False
	):
		room2json()

	pE2C()