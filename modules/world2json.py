from utils import *

worldFileIn, worldFileOut = getFilesDialog('world','json')

worldDict = openWorld(worldFileIn)

if getYesNoDialog( #choose tile display mode
	'Translate tile numbers to binary?',
	[
		'String with a space each 4 char',
		'(Default option when skipping)',
		'Enter n to see other choices'
	],
	True #default
): tileMode = 1 #binary mode
elif getYesNoDialog(
	'Translate tile numbers to a simplified list?',
	[
		'Tiles are separated as such:',
		'  Id Palette Offset Transform',
		'Liquids are separated as such:',
		'  ID ? Set Transform',
		'Enter n or skip to keep original number'
	],
	False #default
): tileMode = 2 #simple mode
else: tileMode = 0 #raw mode

if getYesNoDialog( #get palette color display mode
	'Translate palette color values to hexadecimal?',
	[
		'String with hex values ("bcbcbc")',
		'(Default option when skipping)',
		'Enter n to keep raw number'
	],
	True #default
):
	colMode = 1 #hexadecimal mode
else: colMode = 0 #raw mode

steptodo('IMPORTING WORLD...')

#---- Sorting ----

steptodo('SORTING KEYS...')

worldDict = sortDictPriority(worldDict, [ #sort the properties alphabetically with priorities
	['GENERAL','META'],
	['ELEVATORS','ITEMS']
])

worldDict['META'] = dict(sorted(worldDict['META'].items())) #sort META's properties alphabetically

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
]: #sort the lists' properties alphabetically with priorities
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
		if prop is None: continue #prevent searching for inexistant property
		for stuff in prop:
			stuf2 = stuff.copy()
			stuff.clear()
			stuff.update(sortDictPriority(stuf2, data[1]))
	
	screen.update(sortDictPriority(props, [ #sort the screen's first properties
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
		if isinstance(screen, float): continue
		props = dict([(p,screen[p]) for p in screen if p[:3] not in ['tm_','tb_','tf_','tl_']])
		tileMain = sortTiles(screen,'tm_',tileM)
		tileBack = sortTiles(screen,'tb_',tileM)
		tileFront = sortTiles(screen,'tf_',tileM)
		tileLiquid = sortTiles(screen,'tl_',tileM)
		sortScreenProps(screen,props,tileMain,tileBack,tileFront,tileLiquid)

steptodo('SORTING SCREENS...')

sortScreens(worldDict['SCREENS'], tileMode)

if colMode != 0: #if not raw mode

	steptodo('TRANSLATING PALETTES...')

	for r,room in enumerate(worldDict["ROOMS"]): #go thru each room...
		for p,pal in enumerate(room["PALETTES"]): #each palette...
			for c,col in enumerate(pal[2:]): #each color...
				worldDict["ROOMS"][r]["PALETTES"][p][c+2] = gmdecc2Hexc(col) #and convert

steptodo('SAVING WORLD...')

writeJson(worldFileOut, worldDict) #write to the json file

steptodo('WORLD IMPORTED!')
input('Press Enter to continue...')