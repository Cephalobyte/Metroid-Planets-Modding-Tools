from utils import *

worldFileIn, worldFileOut = getFilesDialog('json','world')

worldDict = openJson(worldFileIn)

newName, newId = getTweaksDialog(worldDict["META"]["name"], worldDict["META"]["id"])

steptodo('TWEAKING...')

try: worldDict["META"]["name"] = newName
except: woops("Couldn't rename the world")
try: worldDict["META"]["id"] = newId
except: woops("Couldn't tweak world Id")

steptodo('TRANSLATING TILES...')

for screen in worldDict["SCREENS"]:
	if isinstance(screen, float): continue #if screen is "disabled"
	tiles = dict([(p,v) for p,v in screen.items() if p[:3] in ['tm_','tb_','tf_','tl_']]) #retrieve tiles
	for co,tile in tiles.items():
		if isinstance(tile, str):
			if len(tile) >= 32: screen.update({co:float(bin2dec(tile))}) #binary mode
			elif co[:3] == 'tl_': screen.update({co:float(packLiquid(tile))}) #simple mode (liquid)
			else: screen.update({co:float(packTile(tile))}) #simple mode
		else: #raw mode
			protip('Raw tile values')
			break

steptodo('TRANSLATING PALETTES...')

for r,room in enumerate(worldDict["ROOMS"]):
	for p,pal in enumerate(room["PALETTES"]):
		for c,col in enumerate(pal[2:]):
			if isinstance(col, str): worldDict["ROOMS"][r]["PALETTES"][p][c+2] = hexc2Gmdecc(col)
			else: break

steptodo('EXPORTING WORLD...')

writeWorld(worldFileOut, worldDict)
writeJson(worldFileOut+'_exp.json', worldDict)

steptodo('WORLD EXPORTED!')
input('Press Enter to continue...')