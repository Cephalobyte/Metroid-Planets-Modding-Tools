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
try: from modules.utils import *
except: from utils import *

worldFileIn, prevFileOut, worldFileType = getFilesDialog(['world','json'],'prevMM.txt')

if worldFileType == '.world': worldDict = openWorld(worldFileIn)
else: worldDict = openJson(worldFileIn)

def getMMWallChar(s:int, doors:list, pos:int=1):
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
			return '██'				#closed
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

def getMMCornerChar(scr:str, scu:str, scl:str, scd:str):
	cru = ('██','▄ ')[scr.isspace() and scu.isspace()]	#if both sides are empty, identify as corner 
	clu = ('██',' ▄')[scl.isspace() and scu.isspace()]
	cld = ('██',' ▀')[scl.isspace() and scd.isspace()]
	crd = ('██','▀ ')[scr.isspace() and scd.isspace()]
	return cru, clu, cld, crd

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

import re

def cleanMM(mRs1:list[str], mRs2:list[str], mRs3:list[str], elevs:list, spwns:list=[]):
	elevPairs = []
	for i, e1 in enumerate(elevs):
		for e2 in elevs[i+1:]:
			if e1["screen_x"] == e2["screen_x"] and e1["dir"] != e2["dir"]:
				elevPairs.append([e1,e2])
				break
	
	eleValid = sum(elevPairs, [])	#valid elevators list

	for r in range(len(mRs1)):	#row
		for pair in elevPairs:
			if min([e["screen_y"] for e in pair]) < r and r < max([e["screen_y"] for e in pair]):
				c = int(pair[0]["screen_x"] * 6)	#column
				if mRs1[r][c:c+6] == '┌────┐':
					mRs1[r] = replaceAtIndex(mRs1[r],'╫──╫',c+1)	#generate elevator rails
					mRs3[r] = replaceAtIndex(mRs3[r],'╫──╫',c+1)
		
		for spwn in [s for s in spwns[:-1] if s["screen_y"] == r]:	#go through every spawn except the last
			c = int(spwn["screen_x"])	#column
			# print(r,c//6,spwn,'\n',[e for e in eleValid if e["screen_x"] == c and e["screen_y"] == r])
			if len([e for e in eleValid if e["screen_x"] == c and e["screen_y"] == r]) > 0: continue	#if there's a valid elevator in place, skip
			mRs2[r] = replaceAtIndex(mRs2[r],'§',c*6+2)	#replace with spawn symbol
		
		for spwn in [s for s in spwns[-1:] if s["screen_y"] == r]:	#go through the last spawn
			c = int(spwn["screen_x"] * 6)	#column
			mRs2[r] = replaceAtIndex(mRs2[r],'⌂',c+2)	#replace last with end symbol
			
		
		mRs1[r] = re.sub('(?<=[^\s]{2}) ▄|▄ (?=[^\s]{2})', '██', mRs1[r], 0, re.MULTILINE).replace('▄  ▄','    ')	#clean corners
		mRs3[r] = re.sub('(?<=[^\s]{2}) ▀|▀ (?=[^\s]{2})', '██', mRs3[r], 0, re.MULTILINE).replace('▀  ▀','    ')

def prevMinimap(screens:dict, width:int, height:int, elevsList:list[dict]=[], itemsList:list[dict]=[], spwnsList:list[dict]=[]):
	mRs1 = ['' for h in range(height)]	#map rows 1
	mRs2 = ['' for h in range(height)]	#map rows 2
	mRs3 = ['' for h in range(height)]	#map rows 3

	progress('GENERATING BASE LAYOUT')

	for i, screen in enumerate(screens):
		col = i%width
		row = i//width
		
		if isinstance(screen, (float, int)):	#if empty screen
			mRs1[row] += '┌────┐'
			mRs2[row] += f'{col} {col}'.center(6,' ')
			mRs3[row] += '└────┘'
			continue

		doors = [[int(d["pos"]),d["color"]] for d in screen["DOORS"]]
		elevs = [e["dir"] for e in elevsList if e["screen_x"]==col and e["screen_y"]==row]
		items = [i["item"] for i in itemsList if i["screen_x"]==col and i["screen_y"]==row]

		scr = getMMWallChar(screen["scroll_r"],doors,1)	#scrolls (sides)
		scu = getMMWallChar(screen["scroll_u"],doors,2)
		scl = getMMWallChar(screen["scroll_l"],doors,3)
		scd = getMMWallChar(screen["scroll_d"],doors,4)
		cru, clu, cld, crd = getMMCornerChar(scr, scu, scl, scd)	#corners
		mid = getMMMiddleChar(next(iter(elevs), None), next(iter(items), None))	#middle : first elev & first item 

		mRs1[row] += clu+scu+cru
		mRs2[row] += scl+mid+scr
		mRs3[row] += cld+scd+crd
	
	progress('SECOND PASS CLEAN UP')

	cleanMM(mRs1, mRs2, mRs3, elevsList, spwnsList)

	progress('COMBINING ROWS')
	mRs1.insert(0,'┌─ LEGEND ────────────┬────┬────────────┬────┬─────────────┬────┬────────────────┬──┬─────────┐')
	mRs2.insert(0,'│ ▀▄ │ Secret Wall    │ || │ Blue Door  │ ╞╡ │ Purple Door │ ║║ │ Green Door     │ •│ Item    │')
	mRs3.insert(0,'│ ▀▄ │                │────│            │╨─╥─│             │════│                │ ○│ Upgrade │')
	mRs1.insert(1,'│ :: │ Secret Passage │ ├┤ │ Red Door   │ ╠╣ │ Combat Door │▼ ▲ │ Elevator       │§ │ Spawn   │')
	mRs2.insert(1,"│''..│                │┴─┬─│            │╩═╦═│             │╫──╫│ Elevator Rails │⌂ │ End     │")
	mRs3.insert(1,'└────┴────────────────┴────┴────────────┴────┴─────────────┴────┴────────────────┴──┴─────────┘')

	rslt=''
	for i in range(len(mRs1)):
		rslt += mRs1[i]+'\n'+mRs2[i]+'\n'+mRs3[i]+'\n'

	progress('PREVIEW GENERATED!',True)

	return rslt

preview = prevMinimap(worldDict["SCREENS"], int(worldDict["GENERAL"]["world_w"]), int(worldDict["GENERAL"]["world_h"]), worldDict["ELEVATORS"], worldDict["ITEMS"], worldDict["GENERAL"]["spawns"])
print(preview)

if getYesNoDialog(
	'Save to text file?',
	['Will be saved as :\n'+prevFileOut],
	False
):

	progress('SAVING MINIMAP')

	writeTxt(prevFileOut, preview)

	progress('PREVIEW SAVED!',True)

pE2C()