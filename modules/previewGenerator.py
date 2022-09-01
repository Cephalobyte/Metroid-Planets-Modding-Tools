
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
		case 2:							#secret
			match pos:
				case 1: return ' ▀'
				case 2: return ' ▀'
				case 3: return '▄ '
				case 4: return '▄ '
		case 3: return '░░'	#dunno

def getMMCornerChar(scl:str, scu:str, scr:str, scd:str):
	# clu = ('██','░░')[scl.isspace() and scu.isspace()]
	# cru = ('██','░░')[scr.isspace() and scu.isspace()]
	# crd = ('██','░░')[scr.isspace() and scd.isspace()]
	# cld = ('██','░░')[scl.isspace() and scd.isspace()]
	# clu = ('██','─┘')[scl.isspace() and scu.isspace()]
	# cru = ('██','└─')[scr.isspace() and scu.isspace()]
	# crd = ('██','┌─')[scr.isspace() and scd.isspace()]
	# cld = ('██','─┐')[scl.isspace() and scd.isspace()]
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

def cleanMM(mRs1:list[str], mRs2:list[str], mRs3:list[str]):
	for r in range(len(mRs1)):
		mRs1[r] = re.sub('(?<=[^\s]{2}) ▄|▄ (?=[^\s]{2})', '██', mRs1[r], 0, re.MULTILINE).replace('▄  ▄','    ')
		mRs3[r] = re.sub('(?<=[^\s]{2}) ▀|▀ (?=[^\s]{2})', '██', mRs3[r], 0, re.MULTILINE).replace('▀  ▀','    ')
		
		# print([m.start() for m in re.finditer(' ▀▀ ', mR1)])
	# return mRs1, mRs2, mRs3

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
	
	cleanMM(mRs1, mRs2, mRs3)
	
	for i in range(len(mRs1)):
		print(mRs1[i])
		print(mRs2[i])
		print(mRs3[i])