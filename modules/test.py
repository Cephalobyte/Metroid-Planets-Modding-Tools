import os
import sys     

from utils import *


if __name__ == '__main__':
	os.system('cls')	#clear, allow ANSI escape sequence on windows

	if len(sys.argv) > 1: #if opened with a file
		print(sys.argv[1])
		with open(sys.argv[1], 'rb') as f:	#read that file's buffer
			print(f.read().decode())
	else: print('no')


	# if getYesNoDialog(
	# 	'Are you doing fine today?',
	# 	['y means yes',
	# 	'n means no']
	# ): print('Yay!')
	# else: print('Aww...')

	# match getOptionDialog(
	# 	'What do you choose?',
	# 	[
	# 		'option 1',
	# 		'option something',
	# 		'oh another option'
	# 	], 
	# 	{
	# 		'banana':'mmhh food',
	# 		'Oxydized APPLE':"don't eat that",	#case insensitive
	# 		'10':'hey, another number!'
	# 	}
	# ):
	# 	case 0:
	# 		print('you got option 1')
	# 	case 1:
	# 		print('you got option 2')
	# 	case 2:
	# 		print('you got option 3')
	# 	case 'banana':
	# 		print('you got option 4')
	# 	case 'Oxydized APPLE':
	# 		print('you got option 5')
	# 	case '10':
	# 		print('you got option 5')

	# str1 = 'Hello World!'
	# print(replaceAtIndex(str1, 'WOW', 14))

	# int1 = 1234567890
	# bin1 = dec2bin(int1)
	# bin1 = "0000 0000 0000 0000 0000 0000 0110 1000"
	# print(int1)
	# print(bin1)
	# print(bin2dec(bin1))

	# def num2alph(n:int, maj:bool=True):
	# 	asciibase = (97, 65)[maj]
	# 	ltr1num = n%26
	# 	ltr2num = ((n//26-1)%26,' ')[n//26<1]
	# 	ltr3num = ((n//26//26)%26,' ')[n//27//26<1]
	# 	ltr1 = chr(asciibase+n%26)

	# 	print(n,ltr3num,ltr2num,ltr1num)
		# ltr2 = (chr(),)
		# return chr(asciibase+ltr2)+chr(asciibase+ltr1)

	# for i in range(26**2+27):
		# print(num2alph(i))
		# num2alph(i)

	# import prompt_toolkit
	# from prompt_toolkit import prompt
	# from prompt_toolkit import PromptSession
	# from prompt_toolkit.completion import WordCompleter
	# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
		
	# prompt('What is your name: ')

	# prompt('What is your name: ', default='macsjfvnl')

	# session = PromptSession()
	# while True:
	# 	text = session.prompt('> ', auto_suggest=AutoSuggestFromHistory())
	# 	print('You said: %s' % text)

	# random_completer = WordCompleter([f'apple{i}' for i in [(j,f'_banan{j}')[j > 4] for j in range(10)]])
	# html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
	# prompt('Enter HTML: ', completer=random_completer)
	# msg = ''
	# for i in range(20):
	# 	# msg += str(i)
	# 	msg += ' '
	# 	for j in range(9):
	# 		msg += str(j+1)
	# print(msg)

	# os.system('mode 50')
	# os.system('color 8f')

	# print("\x1b[8;40;80t")
	# print('\x1b[5;31;43m',os.get_terminal_size(),'\x1b[0;0m')
	# print(os.get_terminal_size())

	def coltable():
		print("\\033[XXm")

		for i in range(30,37+1):
				print("\033[%dm%d\t\033[%dm%d\t\033[%dm  \033[0m%d\t\033[%dm  \033[0m%d" % (i,i,i+60,i+60,i+10,i+10,i+70,i+70))

		print("\033[39m\\033[49m - Reset colour")
		print("\\033[2K - Clear Line")
		print("\\033[<L>;<C>H OR \\033[<L>;<C>f puts the cursor at line L and column C.")
		print("\\033[<N>A Move the cursor up N lines")
		print("\\033[<N>B Move the cursor down N lines")
		print("\\033[<N>C Move the cursor forward N columns")
		print("\\033[<N>D Move the cursor backward N columns")
		print("\\033[2J Clear the screen, move to (0,0)")
		print("\\033[K Erase to end of line")
		print("\\033[s Save cursor position")
		print("\\033[u Restore cursor position")
		print(" ")
		print("\\033[4m  Underline on")
		print("\\033[24m Underline off")
		print("\\033[1m  Bold on")
		print("\\033[21m Bold off")

	coltable()

	print((
	b'\xe2\x96\x80'+\
	b'\xe2\x96\x81'+\
	b'\xe2\x96\x82'+\
	b'\xe2\x96\x83'+\
	b'\xe2\x96\x84'+\
	b'\xe2\x96\x85'+\
	b'\xe2\x96\x86'+\
	b'\xe2\x96\x87'+\
	b'\xe2\x96\x88'+\
	b'\xe2\x96\x89'+\
	b'\xe2\x96\x8a'+\
	b'\xe2\x96\x8b'+\
	b'\xe2\x96\x8c'+\
	b'\xe2\x96\x8d'+\
	b'\xe2\x96\x8e'+\
	b'\xe2\x96\x8f'+\
	b'\xe2\x96\x90'+\
	b'\xe2\x96\x91'+\
	b'\xe2\x96\x92'+\
	b'\xe2\x96\x93'+\
	b'\xe2\x96\x94'+\
	b'\xe2\x96\x95'+\
	b'\xe2\x96\x96'+\
	b'\xe2\x96\x97'+\
	b'\xe2\x96\x98'+\
	b'\xe2\x96\x99'+\
	b'\xe2\x96\x9a'+\
	b'\xe2\x96\x9b'+\
	b'\xe2\x96\x9c'+\
	b'\xe2\x96\x9d'+\
	b'\xe2\x96\x9e'+\
	b'\xe2\x96\x9f'+\
	b'\xe2\x96\xa0'+\
	b'\xe2\x96\xa1'+\
	b'\xe2\x96\xa2'+\
	b'\xe2\x96\xa3'+\
	b'\xe2\x96\xa4'+\
	b'\xe2\x96\xa5'+\
	b'\xe2\x96\xa6'+\
	b'\xe2\x96\xa7'+\
	b'\xe2\x96\xa8'+\
	b'\xe2\x96\xa9'+\
	b'\xe2\x96\xaa'+\
	b'\xe2\x96\xab'+\
	b'\xe2\x96\xac'+\
	b'\xe2\x96\xad'+\
	b'\xe2\x96\xae'+\
	b'\xe2\x96\xaf'+\
	b'\xe2\x96\xb0'+\
	b'\xe2\x96\xb1'+\
	b'\xe2\x96\xb2'+\
	b'\xe2\x96\xb3'+\
	b'\xe2\x96\xb4'+\
	b'\xe2\x96\xb5'+\
	b'\xe2\x96\xb6'+\
	b'\xe2\x96\xb7'+\
	b'\xe2\x96\xb8'+\
	b'\xe2\x96\xb9'+\
	b'\xe2\x96\xba'+\
	b'\xe2\x96\xbb'+\
	b'\xe2\x96\xbc'+\
	b'\xe2\x96\xbd'+\
	b'\xe2\x96\xbe'+\
	b'\xe2\x96\xbf'+\
	b'\xe2\x97\x80'+\
	b'\xe2\x97\x81'+\
	b'\xe2\x97\x82'+\
	b'\xe2\x97\x83'+\
	b'\xe2\x97\x84'+\
	b'\xe2\x97\x85'+\
	b'\xe2\x97\x86'+\
	b'\xe2\x97\x87'+\
	b'\xe2\x97\x88'+\
	b'\xe2\x97\x89'+\
	b'\xe2\x97\x8a'+\
	b'\xe2\x97\x8b'+\
	b'\xe2\x97\x8c'+\
	b'\xe2\x97\x8d'+\
	b'\xe2\x97\x8e'+\
	b'\xe2\x97\x8f'+\
	b'\xe2\x97\x90'+\
	b'\xe2\x97\x91'+\
	b'\xe2\x97\x92'+\
	b'\xe2\x97\x93'+\
	b'\xe2\x97\x94'+\
	b'\xe2\x97\x95'+\
	b'\xe2\x97\x96'+\
	b'\xe2\x97\x97'+\
	b'\xe2\x97\x98'+\
	b'\xe2\x97\x99'+\
	b'\xe2\x97\x9a'+\
	b'\xe2\x97\x9b'+\
	b'\xe2\x97\x9c'+\
	b'\xe2\x97\x9d'+\
	b'\xe2\x97\x9e'+\
	b'\xe2\x97\x9f'+\
	b'\xe2\x97\xa0'+\
	b'\xe2\x97\xa1'+\
	b'\xe2\x97\xa2'+\
	b'\xe2\x97\xa3'+\
	b'\xe2\x97\xa4'+\
	b'\xe2\x97\xa5'+\
	b'\xe2\x97\xa6'+\
	b'\xe2\x97\xa7'+\
	b'\xe2\x97\xa8'+\
	b'\xe2\x97\xa9'+\
	b'\xe2\x97\xaa'+\
	b'\xe2\x97\xab'+\
	b'\xe2\x97\xac'+\
	b'\xe2\x97\xad'+\
	b'\xe2\x97\xae'+\
	b'\xe2\x97\xaf'+\
	b'\xe2\x97\xb0'+\
	b'\xe2\x97\xb1'+\
	b'\xe2\x97\xb2'+\
	b'\xe2\x97\xb3'+\
	b'\xe2\x97\xb4'+\
	b'\xe2\x97\xb5'+\
	b'\xe2\x97\xb6'+\
	b'\xe2\x97\xb7'+\
	b'\xe2\x97\xb8'+\
	b'\xe2\x97\xb9'+\
	b'\xe2\x97\xba'+\
	b'\xe2\x97\xbb'+\
	b'\xe2\x97\xbc'+\
	b'\xe2\x97\xbd'+\
	b'\xe2\x97\xbe'+\
	b'\xe2\x97\xbf').decode())

	pE2C()