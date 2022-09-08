try:
	from prompt_toolkit import prompt
	from prompt_toolkit.completion import WordCompleter

	isPtk = True	#prompt_toolkit is installed
except:
	isPtk = False	#prompt_toolkit is not installed

	print('/!\\'+' Autocompletion features not available '.center(54,'_')+'/!\\')
	for tip in [
		'Refer to the README.md',
		'Normal execution should still work'
	]:
		print('(i) '+tip)

#============ Constants ================================================================================================

NAN = float('nan')

#============ General ==================================================================================================

def replaceAtIndex(text:str, rep:str, at:int=0, l:int=None) ->str:
	"""
Replace a segment of a string :text: from a given position :at: until the given replacement's :rep: length.
:param text: `<str>` text to be modified
:param rep: `<str>` replacement segment
:param at: `<int>` position from which the segment starts overwriting the text.
:param l: `<int>` length of the replacement, defaults to len(rep)
	"""
	if l is None: l = len(rep)
	return text[:at].ljust(at) + rep + text[at+l:]

#============ Input Dialog =============================================================================================
from os import path as osp

#------ Info / Debugging -------------------------------------------------------

def steptodo(step:str, newLine:bool=False):
	"""Instruct the user on what to do"""
	if newLine : print('')
	print(f' {step} '.center(60,'='))

def progress(step:str, done=False):
	"""Report the step progression"""
	if not done: step += '...'
	print('\033[95m'+f' {step} '.center(60,'▒') +'\033[97m')

def protip(tip:str):
	"""Print useful info"""
	print('\033[94m(i) '+ tip +'\033[97m')

def optiontip(id, tip:str, margin:int=3):
	"""Print an option with a description"""
	print(str(id).rjust(margin)+' : \033[94m'+ tip +'\033[97m')

def woops(wrn:str):
	"""Print a warning"""
	print('\033[4;33m/!\\'+f' {wrn} '.center(54,'_')+'/!\\', end='\n\033[0;97m')

def pE2C():
	"""'Press Enter to continue' Pauses the script until user interaction"""
	input('\033[4mPress Enter to continue...\033[0m')

#------ Dialog -----------------------------------------------------------------


def getYesNoDialog(question:str, tips:list=[], defau:bool|None=None) ->bool:
	"""
get a boolean from yes or no dialog option
:param question: The question to ask
:param tips: Optional list of strings to provide details
:param defaut: Optional default value (bool). If set to None, will ask the question again if the user doesn't type a string starting with "y" or "n" (ignore case)
	"""

	def readYN(yn:str):
		if yn.casefold().startswith('y'): return True
		elif yn.casefold().startswith('n'): return False
		elif not yn: return defau	#if question is skipped, set default answer
		else: return None	#if invalid
	
	steptodo(question,True)
	for tip in tips:
		protip(tip)
	answer = readYN(input('(y/n): '))

	while answer is None:	#if the answer is still invalid, ask again
		woops("I'll need you to type either y or n")
		steptodo(question)
		answer = readYN(input('(y/n): '))
	
	return answer


def getOptionDialog(question:str, options:list[str], others:dict[str,str]={}, defau:bool|None=None) ->str|int:
	"""
get an integer or other value from a list of choices
:param question: `<str>` The question to ask
:param options: `<list[str]>` list of options detailing the choices (in order)
:param others: `<dict[str,str]>` (Optional) Dictionary of string keys that detail additional options
:param defau: `<bool|None>` (Optional) Default value. If set to None, will ask the question again if the user doesn't type a given option
	"""

	def readOpt():
		if isPtk and not not others: opt = prompt(completer=WordCompleter(others))	#if prompt_toolkit is installed and has extra options, provide autocompletion
		else: opt=input()	#else ask normally

		other = [k for k in others.keys() if opt.casefold() == k.casefold()]

		if len(other) > 0: return other[0] 
		elif opt.isdigit(): return int(opt) 
		elif not opt: return defau	#if question is skipped, set default answer
		else: return None	#if invalid

	steptodo(question,True)

	if len(others) > 0: mrgn = max([len(max(others.keys(),key=len)), 3]) #if there are extra options, set margin to the maximum option length
	else: mrgn = 3
	for i, tip in enumerate(options): optiontip(i, tip, mrgn)
	for i, tip in others.items(): optiontip(i, tip, mrgn)

	answer = readOpt()

	while answer is None:	#if the answer is still invalid, ask again
		woops("I'll need you to type one of the given option")
		steptodo(question)
		answer = readOpt()

	return answer

#------ Specific ---------------------------------------------------------------


def getInOutFileDialog(fileTypeIn:str|list[str], fileTypeOut:str) ->tuple[str,str]:
	"""

	"""
	
	if isinstance(fileTypeIn, str):	#if single file type accepted
		steptodo(f'Drag & drop the {fileTypeIn} file')
		extIn = '.'+fileTypeIn
	else:														#if multiple file types accepted
		steptodo('Drag & drop the '+' or '.join(fileTypeIn)+' file')
		extIn = ['.'+f for f in fileTypeIn]
	extOut = '.'+fileTypeOut
	fileIn = ''
	invalidpath = True

	while invalidpath:
		fileIn = input().strip('"\'& ')	#strip drag&drop characters
		if isinstance(fileTypeIn, str):	#if not a list
			if not fileIn.endswith(extIn): fileIn += extIn	#add extension if missing
		elif fileIn.endswith(tuple(extIn)): extIn = osp.splitext(fileIn)[1]	#specify which extension matches
		else: fileIn += extIn[0]	#add first extension if missing from list

		if osp.exists(fileIn): invalidpath = False	#if valid
		else:	#if invalid
			print('\n'+fileIn)
			woops("Hmm, I can't find that file. Try again")
			protip("Maybe it's the wrong extension?")

	steptodo(f'Enter the name/path of the new {fileTypeOut} file', True)
	protip('Leave empty to match input file')
	protip('Drag & drop also works')

	fileOut = input().strip('"\'& ')
	if not fileOut: fileOut = osp.splitext(fileIn)[0]	#replace with fileIn's path until extension if empty string
	if not fileOut.endswith(extOut): fileOut += extOut	#add extension if missing

	if isinstance(fileTypeIn, str):	#if not a list
		return fileIn, fileOut	#return only necessary

	return fileIn, fileOut, extIn


def getNameIdDialog(curName:str='', curId:float=NAN) ->tuple[str,float]:
	"""

	"""
	steptodo('Enter a new name',True)
	if not not curName:
		protip('current is :'+curName)
		protip('Leave empty to keep it')
		if isPtk : newName = prompt(default=curName)
	else:
		protip('Leave empty to keep current')
		newName = input()

	steptodo('Enter a new ID',True)
	if curId is not NAN:
		protip('current is :'+str(curId))
		protip('Leave empty to keep it')
		if isPtk : newId = prompt(default=str(curId))
	else:
		protip('Leave empty to keep current')
		newId = input()
	
	if not newId: newId = NAN
	newId = float(newId)

	return newName, newId

#============ File Management ==========================================================================================
import json
import zlib
import base64
import os

def listFiles(dir:str, ext:str) ->list[str]:
	"""
returns every file in the specified directory
filtered by its extension 
	"""
	fileList = []
	for de in os.scandir(dir):
		if de.is_file() and de.name.endswith(ext):	#if is a file and ends with the extension
			fileList.append(de[-len(ext):])
	return fileList

#------ Importing --------------------------------------------------------------


def openWorld(path:str) ->dict:
	with open(path) as file:
		content = file.read()	#store file content in string
	worldjson = base64.b64decode(content.encode())	#get the compressed world by decoding the binary string
	worldjson = zlib.decompress(worldjson).decode()	#decompress into compact json binary string, then decode() turns binary string into string
	worldjson = worldjson.rstrip('\x00')	#removes the possible trailing NUL character
	return json.loads(worldjson)	#return json as python dictionary

def openRoom(path:str) ->dict:
	with open(path) as file:
		roomjson = file.read().rstrip('\x00')	#store file content in string without NULL characters
	roomjson = roomjson[1 : len(roomjson) - int(roomjson[0])]	#remove "salt" by reading the first character int(roomjson[0]) then remove this amount at the end
	roomjson = base64.b64decode(roomjson.encode())	#encode() turns string into binary string, decode base64 encoding
	return json.loads(roomjson)	#return json as python dictionary

def openSave(path:str) ->dict:
	with open(path) as file:
		savejson = file.read().rstrip('\x00')	#store file content in string without NULL characters
	savejson = savejson[1+int(savejson[0]):len(savejson)-int(savejson[0])]	#remove "salt" by reading the first character int(savejson[0]) then remove this amount at the start & end
	savejson = base64.b64decode(savejson.encode())	#encode() turns string into binary string, decode base64 encoding
	return json.loads(savejson)	#return json as python dictionary

def writeJson(path:str, obj:dict, ind:int=4):
	with open(path, 'wt') as file:
		file.write(json.dumps(obj, indent=ind))	#write formatted json string into new text file

#------ Exporting --------------------------------------------------------------


def openJson(path:str) ->dict:
	with open(path) as file:
		return json.loads(file.read())	#store file content in string

def writeTxt(path:str, text:str, openFile:bool=False):
	with open(path, 'wb') as file:
		file.write(text.encode())	#write string into new text file
	if openFile: os.system('notepad.exe '+ path)

def writeWorld(path:str, obj:dict):
	worldb64 = json.dumps(obj)
	worldb64 = zlib.compress(worldb64.encode())
	worldb64 = base64.b64encode(worldb64).decode()
	with open(path, 'wt') as file:
		file.write(worldb64)

def writeRoom(path:str, obj:dict):
	roomb64 = json.dumps(obj).encode()
	roomb64 = base64.b64encode(roomb64).decode()
	roomb64 = '0'+roomb64
	with open(path, 'wt') as file:
		file.write(roomb64)

def writeSave(path:str, obj:dict):
	writeRoom(path, obj)

#============ Sorting ==================================================================================================

def sortDictPriority(dict1:dict, prior:list[str|list[str]]=[]):
	"""
Orders dictionary by key in case-insensitive alphabetic order.
It will sort every key from the first row of :prior:, then the second, etc.
:param dict1: `<dict>`
:param prior: `<list>` example:
	[
	  ['x', 'y'],
	  'width',
	  'height',
	]
	"""
	items = dict1.items()

	if len(prior) == 0:	#if there are no priorities,
		return dict(sorted(items, key=lambda k:k[0].swapcase()))	#sort dictionary alphabetically, ignore case

	def sor(key):
		k = key[0]
		i = len(items)	#default order is last

		for pi, pn in enumerate(prior):
			if k == pn or k in pn: i = pi	#if key is or is in the priority name/names, set the order to the priority index
		
		return (i, k.swapcase())	#return the order as key, content as value

	return dict(sorted(items, key=sor))


def sortTiles(screen:dict, prefix:str='tm_', mode:int=0):
	"""
Orders every tile in by its coordinates.
Translates tile numbers if mode is greater
than 0.
	"""
	dico = {}
	for y in range(15):
		for x in range(20):

			name = prefix+f'{x}-{y}'
			tile = screen.get(name)

			if tile is not None:	#if there is a tile at that position
				match mode:
					case 0:	#raw mode
						dico[name] = tile
						break
					case 1:	#binary mode
						dico[name] = dec2bin(int(tile))
					case 2:	#simple mode
						if prefix == 'tl_':	#if liquid
							dico[name] = unpackLiquidSimple(int(tile))
						else:
							dico[name] = unpackTileSimple(int(tile))
		
		else: continue
		break
	return dico

#============ Readability ==============================================================================================
import re

def dec2bin(d:int):
	return ' '.join(re.findall('.{1,4}',bin(d)[2:].rjust(32,'0')))

def bin2dec(b:str):
	return int(b.replace(' ',''),2)

# def unpackBinTile(tile:int, bits:list=[12,16,17,20,22,28,29,30,31]):
# 	result = str(tile % 2**bits[0])
# 	for pos, bit in enumerate(bits[1:-1]):
# 		result += str((tile % 2**bits[pos+1])//bit)
# 	return result

def unpackTileSimple(tile: int):
	"""
Takes the packed tile number and returns a
readable string containing the tile id, palette
id, animated frame offset and transform id (the
transform id being as follows :
	0 : no transform
	1 : mirror
	2 : flip
	3 : mirror & flip
	4 : rotate
	5 : rotate & mirror
	6 : rotate & flip
	7 : rotate & mirror & flip)
	"""
	id = tile%4096	#tile id
	pal = (tile%131072)//4096	#palette id
	fra = (tile%268435456)//131072	#frame offset
	tra = tile//268435456	#transform
	return f"{id} {pal} {fra} {tra}"

def unpackLiquidSimple(tile: int):
	"""
takes the packed tile number and returns a
readable string containing the tile id offset by
x placement, type of liquid (maybe?), set (the 
set being as follows :
	0 : ?
	1 : drips
	2 : surface
	3 : edge
	4 : depth
	5 : ?
	6 : fall
	7 : fall surface) and transform id.
	"""
	id = tile%1024	#tile id + start offset
	typ = (tile%16384)//1024	#type of liquid?
	set = (tile%268435456)//16384	#set of liquid
	tra = tile//268435456	#transform
	return f"{id} {typ} {set} {tra}"

def packTileSimple(tile):
	"""
returns the tile number from the string, reverse
function of unpackTile()
	"""
	tile = [int(float(val)) for val in tile.split()]
	return (tile[3]*268435456)+(tile[2]*131072)+(tile[1]*4096)+tile[0]

def packLiquidSimple(tile):
	"""
returns the tile number from the string, reverse
function of unpackLiquid()
	"""
	tile = [int(float(val)) for val in tile.split()]
	return (tile[3]*268435456)+(tile[2]*16384)+(tile[1]*1024)+tile[0]

def gmdecc2Hexc(val):	#game maker decimal color to hexadecimal color
	"""
takes a gamemaker decimal color and returns a
'readable' (shut up it's my code) hex color
	"""
	val = hex(val)[2:].rjust(6,'0')
	return val[4:6]+val[2:4]+val[0:2]

def hexc2Gmdecc(val):	#hexadecimal color to game maker decimal color
	"""
takes a hex color and returns the gamemaker
decimal color equivalent
	"""
	val = val[4:6]+val[2:4]+val[0:2]
	return int(val,16)