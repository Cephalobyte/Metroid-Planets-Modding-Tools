try: from modules.utils import *
except: from utils import *

worldFileIn, worldFileOut = getInOutFileDialog(
	'json',
	'world'
)

worldDict = openJson(worldFileIn)

newName, newId = getNameIdDialog(
	worldDict["META"]["name"],	#current name
	worldDict["META"]["id"]			#current id
)

progress('RENAMING & IDENTIFYING')	#-------------------------------------------

try: worldDict["META"]["name"] = newName
except: woops("Couldn't rename the world")
try: worldDict["META"]["id"] = newId
except: woops("Couldn't set new world Id")

progress('TRANSLATING TILES')	#-------------------------------------------------

for screen in worldDict["SCREENS"]:	#go through each screen...

	if isinstance(screen, float): continue	#if screen is "disabled", ignore

	tiles = dict(	#retrieve tiles
		[
			(p, v) for p, v in screen.items()
			if p[:3] in ['tm_','tb_','tf_','tl_']
		]
	)

	for co, tile in tiles.items(): #for each coordinate

		if isinstance(tile, str):	#if not raw

			if len(tile) >= 32:		#binary mode
				screen.update({co:float(bin2dec(tile))})
			
			elif co[:3] == 'tl_':	#simple mode (liquid)
				screen.update({co:float(packLiquidSimple(tile))})
			else:									#simple mode (tile)
				screen.update({co:float(packTileSimple(tile))})
		
		else:	#raw mode
			progress('RAW TILE VALUES DETECTED',True)
			progress('IGNORING TILE TRANSLATION')
			break

progress('TRANSLATING PALETTES')	#---------------------------------------------

for r,room in enumerate(worldDict["ROOMS"]):	#go through each room...
	for p,pal in enumerate(room["PALETTES"]):	#each palette...
		for c,col in enumerate(pal[2:]):	#each color...
			if isinstance(col, str):	#if it's a hex color,
				worldDict["ROOMS"][r]["PALETTES"][p][c+2] = hexc2Gmdecc(col)	#convert back
			else: break
		else: continue	#https://note.nkmk.me/en/python-break-nested-loops/
		break
	else: continue
	break

progress('EXPORTING WORLD')	#---------------------------------------------------

writeWorld(worldFileOut, worldDict)

progress('WORLD EXPORTED!',True)	#---------------------------------------------

if getYesNoDialog('Preview the world?', defau=True):

	try: from modules.previewGenerator import prevMinimap
	except: from previewGenerator import prevMinimap

	preview = prevMinimap(
		worldDict["SCREENS"],
		int(worldDict["GENERAL"]["world_w"]),
		int(worldDict["GENERAL"]["world_h"]),
		worldDict["ELEVATORS"],
		worldDict["ITEMS"],
		worldDict["GENERAL"]["spawns"]
	)

	print(preview)

	prevFileOut = worldFileIn.removesuffix('json') + 'prevMM.txt'

	if getYesNoDialog(
		'Save to text file?',
		['Will be saved as :\n'+prevFileOut],
		False
	):

		progress('SAVING MINIMAP')	#-----------------------------------------------

		writeTxt(prevFileOut, preview)

		progress('PREVIEW SAVED!',True)	#-------------------------------------------

pE2C()