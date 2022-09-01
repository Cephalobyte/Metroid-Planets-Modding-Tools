
# ╔═╦╗
# ║╬╠╣
# ╚╩╝
# ┌─┬┐
# │┼├┤
# └┴┘
# ◄▲►▼
#  ░▒▓█
# ↕↨←↑→↓↔
# █▀▀▀▀█
# █    █
# █▄▄▄▄█
# ██▀▀██
# ▌    ▐
# ██▄▄██
# ██■■██
# ▐▌  ▐▌
# ██■■██
try: from modules.utils import *
except: from utils import *

worldFileIn, prevFileOut = getFilesDialog('world','prevMM.txt')

worldDict = openWorld(worldFileIn)

def getMMWallChar(n:int, doors:list, pos:int=1):
	match n:
		case 0: 
			if pos in doors:	#door
				match pos:
					case 1: return ' |'
					case 2: return '¯¯'
					case 3: return '| '
					case 4: return '__'
			return '██'				#closed
		case 1: return '  ' #open
		case 2:							#secret wall
			match pos:
				case 1: return ' ▀'
				case 2: return ' ▀'
				case 3: return '▄ '
				case 4: return '▄ '
		case 3: return '░░'	#secret passage

def getMMCornerChar(scl:str, scu:str, scr:str, scd:str):
	clu = ('██',' ▄')[scl.isspace() and scu.isspace()]
	cru = ('██','▄ ')[scr.isspace() and scu.isspace()]
	crd = ('██','▀ ')[scr.isspace() and scd.isspace()]
	cld = ('██',' ▀')[scl.isspace() and scd.isspace()]
	return clu, cru, crd, cld

def getMMMiddleChar(eln:int, itn:int):
		mid = ''
		match eln:
			case 2: mid+='▲'
			case 4: mid+='▼'
			case None: mid+=' '
		match itn:
			case None: mid+=' '
			case _: mid+='○' #item
		return mid

import re

def cleanMM(mRs1:list[str], mRs2:list[str], mRs3:list[str], elevs:list):
	elevPairs = []
	for i, e1 in enumerate(elevs):
		# print(ei, e1)
		for e2 in elevs[i+1:]:
			# print('\t',e2)
			if e1["screen_x"] == e2["screen_x"] and e1["dir"] != e2["dir"]:
				elevPairs.append([e1,e2])
				break

	print(elevPairs,'\n')

	for r in range(len(mRs1)):
		for pair in elevPairs:
			if min([e["screen_y"] for e in pair]) < r and r < max([e["screen_y"] for e in pair]):
				c = int(pair[0]["screen_x"] * 6) #column
				if mRs1[r][c:c+6] == '┌────┐':
					mRs1[r] = replaceAtIndex(mRs1[r],'┌╫──╫┐',c)
					mRs3[r] = replaceAtIndex(mRs3[r],'└╫──╫┘',c)
		
		mRs1[r] = re.sub('(?<=[^\s]{2}) ▄|▄ (?=[^\s]{2})', '██', mRs1[r], 0, re.MULTILINE).replace('▄  ▄','    ')
		mRs3[r] = re.sub('(?<=[^\s]{2}) ▀|▀ (?=[^\s]{2})', '██', mRs3[r], 0, re.MULTILINE).replace('▀  ▀','    ')
		
		elevs += [m.start() for m in re.finditer(' ▀▀ ', mRs2[r])]

def prevMinimap(screens:dict, width:int, height:int, elevsDict:dict=None, itemsDict:dict=None):
	mRs1 = ['' for h in range(height)] #map rows 1
	mRs2 = ['' for h in range(height)] #map rows 2
	mRs3 = ['' for h in range(height)] #map rows 3

	for i, screen in enumerate(screens):
		col = i%width
		row = i//width
		
		if isinstance(screen, (float, int)):
			mRs1[row] += '┌────┐'
			mRs2[row] += f'{row} {col}'.center(6,' ')
			mRs3[row] += '└────┘'
			continue

		doors = [int(d["pos"]) for d in screen["DOORS"]]
		elevs = [e["dir"] for e in elevsDict if e["screen_x"]==col and e["screen_y"]==row]
		items = [i["item"] for i in itemsDict if i["screen_x"]==col and i["screen_y"]==row]

		scl = getMMWallChar(screen["scroll_l"],doors,3)
		scu = getMMWallChar(screen["scroll_u"],doors,2)
		scr = getMMWallChar(screen["scroll_r"],doors,1)
		scd = getMMWallChar(screen["scroll_d"],doors,4)
		clu, cru, crd, cld = getMMCornerChar(scl, scu, scr, scd)
		mid = getMMMiddleChar(next(iter(elevs), None), next(iter(items), None))

		mRs1[row] += clu+scu+cru
		mRs2[row] += scl+mid+scr
		mRs3[row] += cld+scd+crd
	
	cleanMM(mRs1, mRs2, mRs3, elevsDict)
	
	rslt=''
	for i in range(len(mRs1)):
		rslt += mRs1[i]+'\n'+mRs2[i]+'\n'+mRs3[i]+'\n'
	
	return rslt

preview = prevMinimap(worldDict["SCREENS"], int(worldDict["GENERAL"]["world_w"]), int(worldDict["GENERAL"]["world_h"]), worldDict["ELEVATORS"], worldDict["ITEMS"])
print(preview)

if getYesNoDialog(
	'Save to text file?',
	['Will be saved as :\n'+prevFileOut],
	False
):
	writeTxt(prevFileOut, preview)

pE2C()