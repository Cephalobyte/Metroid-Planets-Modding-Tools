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
#  ░▒▓█
# █▀▀▀▀█
# █    █
# █▄▄▄▄█
# ██▀▀██
# ▌    ▐
# ██▄▄██
# ██■■██
# ▐▌  ▐▌
# ██■■██
# area0, Crat, Brin, Norf, Kraid, Ridley, Tout, WrSh, Unused, ... 

try: from modules.utils import *
except: from utils import *

import re
import os

AREACHARDICT = {
	"area 0":				'░ ',
	"Crateria":			'██',
	"Brinstar":			'█▓',
	"Norfair":			'▓▒',
	"Kraid area":		'▓▓',
	"Ridley area":	'▒▒',
	"Tourian":			'░░',
	"Wrecked Ship":	'▒░',
	"Area 8":				'█▒',
	"Area 9":				'█░',
	"Area 10":			'█ ',
	"Area 11":			'▓░',
	"Area 12":			'▓ ',
	"Area 13":			'▒ ',
	"Area 14":			'[]'
}

fileIn, prevFileOut, levelType = getInOutFileDialog(
	['world','json'],
	'prevMM.txt'
)

print(levelType)
match levelType:
	case '.json': levelDict = openJson(fileIn)
	case '.room': levelDict = openRoom(fileIn)
	case _: levelDict = openWorld(fileIn)

def getMMEmptyScreen(x:int, y:int) ->list[str]:
	coords = f'{x} {y}'.center(6)
	# coords = str(x).center(3) + str(y).center(3)
	# coords = str(x).center(3) + f'{y} '.center(3)[:3]
	return [
		'┌────┐',
		coords,
		'└────┘'
	]

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
def getMMCornerChar(scr:str, scu:str, scl:str, scd:str, areachar:str='██', area:int=1):
	a = hex(area)[2:]
	cru = (areachar, '╚'+a)[scr.isspace() and scu.isspace()]	#if both sides are empty, identify as corner + area
	clu = (areachar, '╝'+a)[scl.isspace() and scu.isspace()]
	cld = (areachar, '╗'+a)[scl.isspace() and scd.isspace()]
	crd = (areachar, '╔'+a)[scr.isspace() and scd.isspace()]
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
def cleanMM(mmr1:list[str], mmr2:list[str], mmr3:list[str], areas:list[str]=list(AREACHARDICT.values()), elevs:list=[], spwns:list=[]):
	elevPairs = []
	for i, e1 in enumerate(elevs):	#go through each elevator...
		for e2 in elevs[i+1:]:	#and through each next one...
			if e1["screen_x"] == e2["screen_x"] and e1["dir"] != e2["dir"]:	#if it finds a match,
				elevPairs.append([e1,e2])	#store it in the elevator pairs
				break	#compare the next one
	
	eleValid = sum(elevPairs, [])	#flat version of elevPairs
	
	for r in range(len(mmr1)):	#row
		r1 = mmr1[r]	#for convenience, store minimap rows locally
		r2 = mmr2[r]
		r3 = mmr3[r]

		#------ ELEVATOR RAILS -----------------------------------------------------

		for pair in elevPairs:
			if min([e["screen_y"] for e in pair]) < r and r < max([e["screen_y"] for e in pair]):	#when between elevator rooms
				c = int(pair[0]["screen_x"] * 6)	#column
				if r1[c:c+6] == '┌────┐':	#if in an empty screen
					r1 = replaceAtIndex(r1,'╫──╫',c+1)	#generate elevator rails
					r3 = replaceAtIndex(r3,'╫──╫',c+1)

		#------ DRAW SPAWNS & OVERWRITE ELEVATORS ----------------------------------
		
		for spwn in [	#go through every spawn of this row
			s for s in spwns
			if s["screen_y"] == r
		]:
			c = int(spwn["screen_x"])	#column

			if len([	#if there's a valid elevator at the same location,
				e for e in eleValid
				if e["screen_x"] == c
				and e["screen_y"] == r
			]) > 0: continue	#skip

			r2 = replaceAtIndex(r2, '§', c*6+2)	#replace with spawn symbol
	
		for elev in [	#go through the last elevator
			e for e in elevs[-1:]
			if e["screen_y"] == r
		]:
			c = int(elev["screen_x"] * 6)	#column * block width

			r2 = replaceAtIndex(r2,'◘',c+2)	#replace with end symbol
		
		#------ CLEAN CORNERS ------------------------------------------------------
		
		r1 = re.sub('╚\d╝\d', '    ', r1)	#not corners, large rooms
		r3 = re.sub('╔\d╗\d', '    ', r3)

		pat = '[╚╝╗╔](\d)'	#pattern to find remaining corners

		for match in re.finditer(pat, r1):
			r1 = replaceAtIndex(r1, areas[int(match.group(1), 16)], match.start())

		for match in re.finditer(pat, r3):
			r3 = replaceAtIndex(r3, areas[int(match.group(1), 16)], match.start())

		mmr1[r] = r1	#then re-assign them
		mmr2[r] = r2
		mmr3[r] = r3

#preview Minimap
def prevMinimap(screens:dict, width:int, height:int, elevsList:list[dict]=[], itemsList:list[dict]=[], spwnsList:list[dict]=[], areacharList:list[str]=list(AREACHARDICT.values())):
	mmr1 = ['' for h in range(height)]	#minimap rows 1
	mmr2 = ['' for h in range(height)]	#minimap rows 2
	mmr3 = ['' for h in range(height)]	#minimap rows 3

	progress('GENERATING BASE LAYOUT')	#-----------------------------------------

	# areas = list(set([s["area"] for s in screens if isinstance(s, dict)]))
	# print(areas)

	for i, screen in enumerate(screens):
		col = i % width
		row = i //width
		
		if isinstance(screen, (float, int)):	#if empty screen
			es = getMMEmptyScreen(col,row)
			mmr1[row] += es[0]
			mmr2[row] += es[1]
			mmr3[row] += es[2]
			continue

		area = int(screen["area"])	#area
		areachar = areacharList[area] #area "color"
		doors = [[int(d["pos"]),d["color"]] for d in screen["DOORS"]] #retrieve door position & color
		elevs = [e["dir"] for e in elevsList if e["screen_x"]==col and e["screen_y"]==row]	#retrieve elevator direction
		items = [i["item"] for i in itemsList if i["screen_x"]==col and i["screen_y"]==row]	#retrieve item item (laugh)

		scr = getMMWallChar(screen["scroll_r"], doors, 1, areachar)	#scrolls (sides) right
		scu = getMMWallChar(screen["scroll_u"], doors, 2, areachar)	#up
		scl = getMMWallChar(screen["scroll_l"], doors, 3, areachar)	#left
		scd = getMMWallChar(screen["scroll_d"], doors, 4, areachar)	#down
		cru, clu, cld, crd = getMMCornerChar(scr, scu, scl, scd, areachar, area)	#corners
		mid = getMMMiddleChar(next(iter(elevs), None), next(iter(items), None))	#middle : first elev & first item 

		mmr1[row] += clu + scu + cru
		mmr2[row] += scl + mid + scr
		mmr3[row] += cld + scd + crd
	
	progress('SECOND PASS CLEAN UP')	#-------------------------------------------

	cleanMM(mmr1, mmr2, mmr3, areacharList, elevsList, spwnsList)#, screens)
	
	progress('ADDING LEGEND')	#---------------------------------------------------

	mmr1.insert(0,'┌─ LEGEND ────────────┬────┬──────────────┬────┬─────────────┬────┬────────────────┬──┬─────────┐')
	mmr2.insert(0,'│ ▀▄ │ Secret Wall    │ || │ Blue Door    │ ╞╡ │ Purple Door │ ║║ │ Green Door     │ •│ Item    │')
	mmr3.insert(0,'│ ▀▄ │                │────│              │╨─╥─│             │════│                │ ○│ Upgrade │')
	mmr1.insert(1,'│ :: │ Secret Passage │ ├┤ │ Red Door     │ ╠╣ │ Combat Door │▼ ▲ │ Elevator       │§ │ Spawn   │')
	mmr2.insert(1,"│''..│                │┴─┬─│              │╩═╦═│             │╫──╫│ Elevator Rails │◘ │ End     │")
	mmr3.insert(1,'│ ██ │ Crateria       │ ▓▒ │ Norfair      │ ░░ │ Tourian     │ █░ │ Area 9         │▓ │ Area 12 │')
	mmr1.insert(2,'│ █▓ │ Brinstar       │ ▒▒ │ Ridley area  │ ░  │ Area 0      │ █  │ Area 10        │▒ │ Area 13 │')
	mmr2.insert(2,"│ ▓▓ │ Kraid area     │ ▒░ │ Wrecked Ship │ █▒ │ Area 8      │ ▓░ │ Area 11        │XX│ Area 14 │")
	mmr3.insert(2,'└────┴────────────────┴────┴──────────────┴────┴─────────────┴────┴────────────────┴──┴─────────┘')

	progress('COMBINING ROWS')	#-------------------------------------------------

	minimap = ''
	for i in range(len(mmr1)):
		minimap += mmr1[i]+'\n'+mmr2[i]+'\n'+mmr3[i]+'\n'

	progress('PREVIEW GENERATED!',True)	#-----------------------------------------

	if os.get_terminal_size().columns < max([102, width * 6]):	#if the window isn't large enough for the map
		os.system(f'mode {max([102, width * 6])}')	#enlarge it

	return minimap

match levelType:
	case _:
		preview = prevMinimap(
			levelDict["SCREENS"],
			int(levelDict["GENERAL"]["world_w"]),
			int(levelDict["GENERAL"]["world_h"]),
			levelDict["ELEVATORS"],
			levelDict["ITEMS"],
			levelDict["GENERAL"]["spawns"]
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