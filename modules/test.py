from utils import *

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

# import os
# os.system('mode 50')
# cmd = 'color 5E'
# os.system(cmd)

# print("\x1b[8;40;80t")
# print('\x1b[5;31;43m',os.get_terminal_size(),'\x1b[0;0m')
# print(os.get_terminal_size())

pE2C()