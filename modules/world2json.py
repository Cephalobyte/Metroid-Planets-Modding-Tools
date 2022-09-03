try: from modules.utils import *
except: from utils import *

worldFileIn, worldFileOut = getFilesDialog('world','json')

worldDict = openWorld(worldFileIn)

tileMode = getOptionDialog(#choose tile display mode
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

progress('IMPORTING WORLD')

#---- Sorting ----

progress('SORTING KEYS')

worldDict = sortDictPriority(worldDict, [	#sort the properties alphabetically with priorities
	['GENERAL','META'],
	['ELEVATORS','ITEMS']
])

worldDict['META'] = dict(sorted(worldDict['META'].items()))	#sort META's properties alphabetically

for data in [
	['["GENERAL"]["spawns"]', []],
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
]:	#sort the lists' properties alphabetically with priorities
	for stuff in eval(f'worldDict{data[0]}'):
		stuf2 = stuff.copy()
		stuff.clear()
		stuff.update(sortDictPriority(stuf2, data[1]))

#---- Sort & Readability ----

def sortScreenProps(screen:dict,props:dict,tileMain:dict,tileBack:dict,tileFront:dict,tileLiquid:dict):
	screen.clear()
	for data in [
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
	]:
		prop = props.get(data[0])
		if prop is None: continue	#prevent searching for inexistant property
		for stuff in prop:
			stuf2 = stuff.copy()
			stuff.clear()
			stuff.update(sortDictPriority(stuf2, data[1]))
	
	screen.update(sortDictPriority(props, [	#sort the screen's first properties
		['x','y'],
		['room_wi'],
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
		if isinstance(screen, (float, int)): continue
		props = dict([(p,screen[p]) for p in screen if p[:3] not in ['tm_','tb_','tf_','tl_']])
		tileMain = sortTiles(screen,'tm_',tileM)
		tileBack = sortTiles(screen,'tb_',tileM)
		tileFront = sortTiles(screen,'tf_',tileM)
		tileLiquid = sortTiles(screen,'tl_',tileM)
		sortScreenProps(screen,props,tileMain,tileBack,tileFront,tileLiquid)

progress('SORTING SCREENS')

sortScreens(worldDict['SCREENS'], tileMode)

if colMode > 0:	#if not raw mode

	progress('TRANSLATING PALETTES')

	for r,room in enumerate(worldDict["ROOMS"]):	#go thru each room...
		for p,pal in enumerate(room["PALETTES"]):	#each palette...
			for c,col in enumerate(pal[2:]):	#each color...
				worldDict["ROOMS"][r]["PALETTES"][p][c+2] = gmdecc2Hexc(int(col))	#and convert

progress('SAVING WORLD')

writeJson(worldFileOut, worldDict)	#write to the json file

progress('WORLD IMPORTED!',True)

if getYesNoDialog('Preview the world?', defau=True):
	try: from modules.previewGenerator import prevMinimap
	except: from previewGenerator import prevMinimap
	preview = prevMinimap(worldDict["SCREENS"], int(worldDict["GENERAL"]["world_w"]), int(worldDict["GENERAL"]["world_h"]), worldDict["ELEVATORS"], worldDict["ITEMS"], worldDict["GENERAL"]["spawns"])
	print(preview)

	prevFileOut = worldFileIn.removesuffix('world') + 'prevMM.txt'
	if getYesNoDialog(
		'Save to text file?',
		['Will be saved as :\n'+prevFileOut],
		False
	):

		progress('SAVING MINIMAP')

		writeTxt(prevFileOut, preview)

		progress('PREVIEW SAVED!',True)

pE2C()