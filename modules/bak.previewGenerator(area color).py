#ASCII art copy/paste chart
# ╔═╦╗
# ║╬╠╣
# ╚╩╝
# ┌─┬┐
# │┼├┤
# └┴┘
# ☺☻♥♦♣♠
# §▬⌂♪♫₧∙°º○Θ∞φ
# ◄▲►▼
# ←↑→↓↕↨↔
# •◘○◙■

# █▀▀▀▀█
# █    █
# █▄▄▄▄█
# ██▀▀██
# ▌    ▐
# ██▄▄██
# ██■■██
# ▐▌  ▐▌
# ██■■██

#  ░▒▓█
# Area color testing

#  None  Crat  Brin  Norf

# XXXXXX███████▓█▓█▓▓▒▓▒▓▒
# XX  XX██  ███▓  █▓▓▒  ▓▒
# XXXXXX███████▓█▓█▓▓▒▓▒▓▒

# Kraid Ridley Tour  WrSh

# ▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░▒░▒░▒░
# ▓▓  ▓▓▒▒  ▒▒░░  ░░▒░  ▒░
# ▓▓▓▓▓▓▒▒▒▒▒▒░░░░░░▒░▒░▒░

try: from modules.utils import *
except: from utils import *

import re

worldFileIn, prevFileOut, worldFileType = getInOutFileDialog(
	['world','json'],
	'prevMM.txt'
)

if worldFileType == '.world': worldDict = openWorld(worldFileIn)
else: worldDict = openJson(worldFileIn)

#get Minimap Wall character
def getMMWallChar(s:int, doors:list, pos:int=1, areachar:str='██'):
	match s:
		case 0: 						#if closed
			door = next(iter([d for d in doors if d[0] == pos]), None)
			if door is not None:
				match door[1]:			#door color
					case 0: return '  '			#open
					case 1: 								#blue
						match pos:
							case 1: return ' |'
							case 2|4: return '──'	#vertical
							case 3: return '| '
					case 2:									#red
						match pos:
							case 1: return ' ├'
							case 2: return '┴─'
							case 3: return '┤ '
							case 4: return '┬─'
					case 3:									#purple
						match pos:
							case 1: return ' ╞'
							case 2: return '╨─'
							case 3: return '╡ '
							case 4: return '╥─'
					case 4:									#green
						match pos:
							case 1: return ' ║'
							case 2|4: return '══'
							case 3: return '║ '
					case _:									#other
						match pos:
							case 1: return ' ╠'
							case 2: return '╩═'
							case 3: return '╣ '
							case 4: return '╦═'
			return areachar		#closed
		case 1: return '  '	#open
		case 2:							#secret wall
			match pos:
				case 1|2: return ' ▀'	#right or top
				case 3|4: return '▄ '	#left or down
		case 3:							#secret passage
			match pos:
				case 1: return ' :'
				case 2: return "''"
				case 3: return ': '
				case 4: return '..'

#get Minimap corner character
def getMMCornerChar(scr:str, scu:str, scl:str, scd:str, areachar:str='██'):
	cru = (areachar,'▄ ')[scr.isspace() and scu.isspace()]	#if both sides are empty, identify as corner 
	clu = (areachar,' ▄')[scl.isspace() and scu.isspace()]
	cld = (areachar,' ▀')[scl.isspace() and scd.isspace()]
	crd = (areachar,'▀ ')[scr.isspace() and scd.isspace()]
	return cru, clu, cld, crd

#get Minimap middle character
def getMMMiddleChar(eln:int, itn:int):
		mid = ''
		match eln:
			case 2: mid+='▲'
			case 4: mid+='▼'
			case None: mid+=' '
		match itn:
			case None: mid+=' '
			case 7|15|16|17: mid+='•'	#collectible
			case _: mid+='○'	#upgrade
		return mid

#clean Minimap
def cleanMM(mmr1:list[str], mmr2:list[str], mmr3:list[str], r:int, areachar:str='██', elevs:list=[], spwns:list=[]):
	elevPairs = []
	for i, e1 in enumerate(elevs):
		for e2 in elevs[i+1:]:
			if e1["screen_x"] == e2["screen_x"] and e1["dir"] != e2["dir"]:
				elevPairs.append([e1,e2])
				break
	
	eleValid = sum(elevPairs, [])	#valid elevators list

	# for r in range(len(mmr1)):	#row

	for pair in elevPairs:
		if min([e["screen_y"] for e in pair]) < r and r < max([e["screen_y"] for e in pair]):
			c = int(pair[0]["screen_x"] * 6)	#column
			print(mmr1[r][c:c+6])
			if mmr1[r][c:c+6] == '┌────┐':
				mmr1[r] = replaceAtIndex(mmr1[r],'╫──╫',c+1)	#generate elevator rails
				mmr3[r] = replaceAtIndex(mmr3[r],'╫──╫',c+1)
	
	# for spwn in [	#go through every spawn of this row
	# 	s for s in spwns
	# 	if s["screen_y"] == r
	# ]:
	# 	c = int(spwn["screen_x"])	#column

	# 	if len([	#if there's a valid elevator at the same location,
	# 		e for e in eleValid
	# 		if e["screen_x"] == c
	# 		and e["screen_y"] == r
	# 	]) > 0: continue	#skip

	# 	mmr2[r] = replaceAtIndex(mmr2[r], '§', c*6+2)	#replace with spawn symbol
	
	# for elev in [	#go through the last elevator
	# 	e for e in elevs[-1:]
	# 	if e["screen_y"] == r
	# ]:
	# 	c = int(elev["screen_x"] * 6)	#column * block width

	# 	mmr2[r] = replaceAtIndex(mmr2[r],'◘',c+2)	#replace with end symbol
	
	mmr1[r] = re.sub(
		'(?<=[^\s]{2}) ▄|▄ (?=[^\s]{2})', areachar, mmr1[r]	#clean corners
	).replace('▄  ▄','    ')															#clean large rooms
	mmr3[r] = re.sub(
		'(?<=[^\s]{2}) ▀|▀ (?=[^\s]{2})', areachar, mmr3[r]
	).replace('▀  ▀','    ')

#preview Minimap
def prevMinimap(screens:dict, width:int, height:int, elevsList:list[dict]=[], itemsList:list[dict]=[], spwnsList:list[dict]=[], areacharList:list[str]=['XX','██','█▓','▓▒','▓▓','▒▒','░░','▒░']):
	mmr1 = ['' for h in range(height)]	#minimap rows 1
	mmr2 = ['' for h in range(height)]	#minimap rows 2
	mmr3 = ['' for h in range(height)]	#minimap rows 3

	progress('GENERATING BASE LAYOUT')	#-----------------------------------------

	for i, screen in enumerate(screens):
		col = i % width
		row = i //width
		
		if isinstance(screen, (float, int)):	#if empty screen
			mmr1[row] += '┌────┐'
			mmr2[row] += f'{col} {row}'.center(6,' ')
			mmr3[row] += '└────┘'
			continue
		
		areachar = areacharList[int(screen["area"]) % len(areacharList)] #area "color"
		doors = [[int(d["pos"]), d["color"]] for d in screen["DOORS"]] #retrieve door position & color
		elevs = [e["dir"] for e in elevsList if e["screen_x"]==col and e["screen_y"]==row]	#retrieve elevator direction
		items = [i["item"] for i in itemsList if i["screen_x"]==col and i["screen_y"]==row]	#retrieve item item (laugh)

		scr = getMMWallChar(screen["scroll_r"], doors, 1, areachar)	#scrolls (sides)
		scu = getMMWallChar(screen["scroll_u"], doors, 2, areachar)
		scl = getMMWallChar(screen["scroll_l"], doors, 3, areachar)
		scd = getMMWallChar(screen["scroll_d"], doors, 4, areachar)
		cru, clu, cld, crd = getMMCornerChar(scr, scu, scl, scd, areachar)	#corners
		mid = getMMMiddleChar(next(iter(elevs), None), next(iter(items), None))	#middle : first elev & first item 

		mmr1[row] += clu + scu + cru
		mmr2[row] += scl + mid + scr
		mmr3[row] += cld + scd + crd

		cleanMM(mmr1, mmr2, mmr3, row, areachar, elevsList, spwnsList)
	
	progress('ADDING LEGEND')	#---------------------------------------------------

	mmr1.insert(0,'┌─ LEGEND ────────────┬────┬────────────┬────┬─────────────┬────┬────────────────┬──┬─────────┐')
	mmr2.insert(0,'│ ▀▄ │ Secret Wall    │ || │ Blue Door  │ ╞╡ │ Purple Door │ ║║ │ Green Door     │ •│ Item    │')
	mmr3.insert(0,'│ ▀▄ │                │────│            │╨─╥─│             │════│                │ ○│ Upgrade │')
	mmr1.insert(1,'│ :: │ Secret Passage │ ├┤ │ Red Door   │ ╠╣ │ Combat Door │▼ ▲ │ Elevator       │§ │ Spawn   │')
	mmr2.insert(1,"│''..│                │┴─┬─│            │╩═╦═│             │╫──╫│ Elevator Rails │◘ │ End     │")
	mmr3.insert(1,'└────┴────────────────┴────┴────────────┴────┴─────────────┴────┴────────────────┴──┴─────────┘')

	progress('COMBINING ROWS')	#-------------------------------------------------

	minimap = ''
	for i in range(len(mmr1)):
		minimap += mmr1[i] +'\n'+ mmr2[i] +'\n'+ mmr3[i] +'\n'

	progress('PREVIEW GENERATED!',True)	#-----------------------------------------

	return minimap

preview = prevMinimap(
	worldDict["SCREENS"],
	int(worldDict["GENERAL"]["world_w"]),
	int(worldDict["GENERAL"]["world_h"]),
	worldDict["ELEVATORS"],
	worldDict["ITEMS"],
	worldDict["GENERAL"]["spawns"]
)

print(preview)

if getYesNoDialog(
	'Save to text file?',
	['Will be saved as :\n'+prevFileOut],
	False
):

	progress('SAVING MINIMAP')	#-------------------------------------------------

	writeTxt(prevFileOut, preview)

	progress('PREVIEW SAVED!',True)	#---------------------------------------------

pE2C()