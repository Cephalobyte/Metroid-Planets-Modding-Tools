NAN = float('nan')
#============ Input Dialog ============
from os import path as osp

def steptodo(step:str, newLine:bool=False):
	if newLine : print('')
	print(f' {step} '.center(60,'='))

def protip(tip:str):
	print('(i) '+tip)

def woops(err:str):
	print('/!\\'+f' {err} '.center(54,'_')+'/!\\')

def getFilesDialog(fileTypeIn:str, fileTypeOut:str) ->tuple:
	extIn = '.'+fileTypeIn
	extOut = '.'+fileTypeOut
	
	steptodo(f'Drag & drop the {fileTypeIn} file to convert')

	fileIn = ''
	invalidpath = True

	while invalidpath:
		fileIn = input().strip('"\'& ')
		if not fileIn.endswith(extIn): fileIn += extIn #add extension if missing

		if osp.exists(fileIn): invalidpath = False #if valid
		else: #if invalid
			print('')
			woops("Hmm, I can't find that file. Try again")
			protip("Maybe it's the wrong extension?")
			print('I searched for :',fileIn)

	steptodo(f'Enter the name/path of the new {fileTypeOut} file', True)
	protip('Leave empty to match input file')
	protip('Drag & drop also works')

	fileOut = input().strip('"\'& ')
	if not fileOut: fileOut = fileIn[:-len(extIn)] #replace with fileIn if empty string
	if not fileOut.endswith(extOut): fileOut += extOut #add extension if missing

	# fIPath = osp.abspath(fileIn)
	# fOPath = osp.abspath(fileOut)
	# print(osp.dirname(fIPath))
	# print(osp.dirname(fOPath))
	# keepdir = input('Keep input file\'s directory? (y/n): ')
	return fileIn, fileOut

def getTweaksDialog(curName:str='', curID:float=NAN) ->tuple:
	steptodo('Enter a new name',True)
	if not not curName: protip('current is :'+curName)
	protip('Leave empty to keep it')
	newName = input()

	steptodo('Enter a new ID',True)
	if curID is not NAN: protip('current is :'+str(curID))
	protip('Leave empty to keep it')
	newID = input()
	if not newID: newID = NAN
	newID = float(newID)

	return newName, newID

def getYesNoDialog(question:str='', tips:list=[], defau:bool|None=None) ->bool|None:
	def readYN(yn:str):
		if yn.casefold().startswith('y'): return True
		elif yn.casefold().startswith('n'): return False
		elif not yn: return defau #if question is skipped, set default answer
		else: return None #if invalid
	
	steptodo(question,True)
	for tip in tips:
		protip(tip)
	answer = readYN(input('(y/n): '))

	while answer is None: #if the answer is still invalid, ask again
		woops("I'll need you to type either y or n")
		steptodo(question)
		answer = readYN(input('(y/n): '))
	
	return answer

#============ File Management ============
import json
import zlib
import base64

#------ Importing ------

def openWorld(path:str) ->dict:
	with open(path) as file:
		content = file.read() #store file content in string
	worldjson = base64.b64decode(content.encode()) #get the compressed world by decoding the binary string
	worldjson = zlib.decompress(worldjson).decode() #decompress into compact json binary string, then decode() turns binary string into string
	worldjson = worldjson.rstrip('\x00') #removes the possible trailing NUL character
	return json.loads(worldjson) #return json as python dictionary

def openRoom(path:str) ->dict:
	with open(path) as file:
		roomjson = file.read().rstrip('\x00') #store file content in string without NULL characters
	roomjson = roomjson[1 : len(roomjson) - int(roomjson[0])] #remove "salt" by reading the first character int(roomjson[0]) then remove this amount at the end
	roomjson = base64.b64decode(roomjson.encode()) #encode() turns string into binary string, decode base64 encoding
	return json.loads(roomjson) #return json as python dictionary

def openSave(path:str) ->dict:
	with open(path) as file:
		savejson = file.read().rstrip('\x00') #store file content in string without NULL characters
	savejson = savejson[1+int(savejson[0]):len(savejson)-int(savejson[0])] #remove "salt" by reading the first character int(savejson[0]) then remove this amount at the start & end
	savejson = base64.b64decode(savejson.encode()) #encode() turns string into binary string, decode base64 encoding
	return json.loads(savejson) #return json as python dictionary

def writeJson(path:str, obj:dict, ind:int=4):
	with open(path, 'wt') as file:
		temp = json.dumps(obj, indent=ind)
		file.write(temp) #write formatted json string into new text file

#------ Exporting ------

def openJson(path:str) ->dict:
	with open(path) as file:
		content = file.read() #store file content in string
		return json.loads(content)

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

#============ Sorting ============

def sortDictPriority(dict1: dict, prior: list=[]):
	"""
orders dictionary by key in case-insensitive 
alphabetic order. It will sort every key from
the first row of _prior_, then the second, etc.
prior (2D list) example :
[
	['x', 'y'],
	['width'],
	['height'], #height would be sorted before width otherwise
]
	"""
	items = dict1.items()
	if len(prior)==0: return dict(sorted(items, key=lambda k:k[0].swapcase()))
	def sor(key):
		k = key[0]
		i = len(items)
		for p,s in enumerate(prior):
			if k in s: i = p
		return (i,k.swapcase())
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
			if tile is not None: #if there is a tile at that position
				match mode:
					case 0: dico[name] = tile #raw mode
					case 1: dico[name] = dec2bin(int(tile)) #binary mode
					case 2: #simple mode
						if prefix == 'tl_': dico[name] = unpackLiquid(int(tile)) #if liquid
						else: dico[name] = unpackTile(int(tile))
	return dico

#============ Readability ============
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

def unpackTile(tile: int):
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
	id = tile%4096 #tile id
	pal = (tile%131072)//4096 #palette id
	fra = (tile%268435456)//131072 #frame offset
	tra = tile//268435456 #transform
	return f"{id} {pal} {fra} {tra}"

def unpackLiquid(tile: int):
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
	id = tile%1024 #tile id + start offset
	typ = (tile%16384)//1024 #type of liquid?
	set = (tile%268435456)//16384 #set of liquid
	tra = tile//268435456 #transform
	return f"{id} {typ} {set} {tra}"

def packTile(tile):
	"""
returns the tile number from the string, reverse
function of unpackTile()
	"""
	tile = [int(float(val)) for val in tile.split()]
	return (tile[3]*268435456)+(tile[2]*131072)+(tile[1]*4096)+tile[0]

def packLiquid(tile):
	"""
returns the tile number from the string, reverse
function of unpackLiquid()
	"""
	tile = [int(float(val)) for val in tile.split()]
	return (tile[3]*268435456)+(tile[2]*16384)+(tile[1]*1024)+tile[0]

def gmdecc2Hexc(val):
	"""
takes a gamemaker decimal color and returns a
'readable' (shut up it's my code) hex color
	"""
	val = hex(val)[2:].rjust(6,'0')
	return val[4:6]+val[2:4]+val[0:2]

def hexc2Gmdecc(val):
	"""
takes a hex color and returns the gamemaker
decimal color equivalent
	"""
	val = val[4:6]+val[2:4]+val[0:2]
	return int(val,16)