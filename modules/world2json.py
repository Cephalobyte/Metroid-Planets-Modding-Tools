from os import system

if __name__ == '__main__': from utils import *
else: from modules.utils import *

#============ Constants ================================================================================================

WORLDPRIORITIES = [
	['GENERAL','META'],
	['ELEVATORS','ITEMS']
]

WORLDLISTSPRIORITIES = [
	['["GENERAL"]["spawns"]', [
	]],
	['["BOSS LOCATIONS"]', [
		['wi','x','y'],
	]],
	['["ELEVATORS"]', [
		['screen_x','screen_y','x','y']
	]],
	['["ITEMS"]', []],
	['["ROOMS"]', [
		['name'],
		['designer'],
	]]
]

WORLDSCREENSPRIORITIES = [
	['x','y'],
	['room_wi'],
	['area'],
	['scroll_r','scroll_u'],
	['scroll_l'],
	['scroll_d']
]

WORLDSCREENSLISTSPRIORITIES = [
	["BLOCKS", [
		['wi'],
		['type','x','y'],
	]],
	["DOORS", [
		['wi'],
		['type'],
		['color','x','y'],
		['pos']
	]],
	["ENEMIES", [
		['n','wi'],
		['type','x','y'],
		['rot'],
		['dir','level','lvl'],
		['lock']
	]]
]

#============ Functions ================================================================================================


def sortScreenProps(screen:dict, props:dict, screenPriorities:list=[], screenListPriorities:list=[]):
	"""
Sort properties present in screens with priorities
	"""
	screen.clear()

	for data in screenListPriorities:
		prop = props.get(data[0])	#get screen property by name
		if prop is None: continue	#prevent searching for a non-existent property

		for stuff in prop:
			stuf2 = stuff.copy()
			stuff.clear()
			stuff.update(sortDictPriority(stuf2, data[1]))
	
	screen.update(sortDictPriority(props, screenPriorities))	#sort the screen's first properties


def sortScreens(screens:dict, tileM:int, screenPriorities:list=[], screenListPriorities:list=[]):
	"""
Sort screen & rearrange tiles with translation.
	"""
	for screen in screens:
		if isinstance(screen, (float, int)): continue	#if screen is "disabled", ignore

		props = dict([(p,screen[p]) for p in screen if p[:3] not in ['tm_','tb_','tf_','tl_']])

		tileMain = sortTiles(screen, 'tm_', tileM)
		tileBack = sortTiles(screen, 'tb_', tileM)
		tileFront = sortTiles(screen, 'tf_', tileM)
		tileLiquid = sortTiles(screen, 'tl_', tileM)
		sortScreenProps(
			screen,
			props,
			screenPriorities,
			screenListPriorities
		)
		screen.update(tileMain)	#add tile layers back to the screen
		screen.update(tileBack)
		screen.update(tileFront)
		screen.update(tileLiquid)


def world2json():
	worldFileIn, worldFileOut = getInOutFileDialog('world','json')

	worldDict = openWorld(worldFileIn)

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

	progress('IMPORTING WORLD')	#-------------------------------------------------

	#------ Sorting --------------------------------------------------------------

	progress('SORTING KEYS')	#---------------------------------------------------

	worldDict = sortDictPriority(worldDict, WORLDPRIORITIES)	#sort the properties alphabetically with priorities

	worldDict['META'] = dict(sorted(worldDict['META'].items()))	#sort META's properties alphabetically

	for data in WORLDLISTSPRIORITIES:	#sort the lists' properties alphabetically with priorities
		prop = eval(f'worldDict{data[0]}')	#get property by name
		if prop is None: continue	#prevent searching for a non-existent property

		for stuff in eval(f'worldDict{data[0]}'):
			stuf2 = stuff.copy()
			stuff.clear()
			stuff.update(sortDictPriority(stuf2, data[1]))

	#------ Sort & Readability ---------------------------------------------------

	progress('SORTING SCREENS')	#-------------------------------------------------

	sortScreens(
		worldDict['SCREENS'],
		tileMode,
		WORLDSCREENSPRIORITIES,
		WORLDSCREENSLISTSPRIORITIES
	)

	if colMode > 0:	#if not raw mode

		progress('TRANSLATING PALETTES')

		for r,room in enumerate(worldDict["ROOMS"]):	#go through each room...
			for p,pal in enumerate(room["PALETTES"]):		#each palette...
				for c,col in enumerate(pal[2:]):					#each color...
					worldDict["ROOMS"][r]["PALETTES"][p][c+2] = gmdecc2Hexc(int(col))	#and convert

	progress('SAVING WORLD')	#---------------------------------------------------

	writeJson(worldFileOut, worldDict)	#write to the json file

	progress('WORLD IMPORTED!',True)	#-------------------------------------------

	if getYesNoDialog('Preview the world?', defau=True):

		if __name__ == '__main__': from previewGenerator import prevMinimap
		else: from modules.previewGenerator import prevMinimap

		preview = prevMinimap(
			worldDict["SCREENS"],
			int(worldDict["GENERAL"]["world_w"]),
			int(worldDict["GENERAL"]["world_h"]),
			worldDict["ELEVATORS"],
			worldDict["ITEMS"],
			worldDict["GENERAL"]["spawns"]
		)

		prevFileOut = worldFileIn.removesuffix('world') + 'prevMM.txt'
		if getYesNoDialog(
			'Save to text file?',
			['Will be saved as :\n'+prevFileOut],
			False
		):

			progress('SAVING MINIMAP')	#---------------------------------------------

			writeTxt(prevFileOut, preview)

			progress('PREVIEW SAVED!',True)	#-----------------------------------------


if __name__ == '__main__':	#if module was run
	system('cls')	#allows ANSI escape sequences

	world2json()	#run module

	while getYesNoDialog(
		'Another?',
		defau = False
	):
		world2json()

	pE2C()