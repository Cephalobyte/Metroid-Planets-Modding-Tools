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
# 		'Oxydized APPLE':"don't eat that", #case insensitive
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

# int1 = 1234567890
# bin1 = dec2bin(int1)
# bin1 = "0000 0000 0000 0000 0000 0000 0110 1000"
# print(int1)
# print(bin1)
# print(bin2dec(bin1))

import prompt_toolkit
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
	
# prompt('What is your name: ')

# prompt('What is your name: ', default='macsjfvnl')

# session = PromptSession()
# while True:
# 	text = session.prompt('> ', auto_suggest=AutoSuggestFromHistory())
# 	print('You said: %s' % text)

# random_completer = WordCompleter([f'apple{i}' for i in [(j,f'_banan{j}')[j > 4] for j in range(10)]])
# html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
# prompt('Enter HTML: ', completer=random_completer)


pE2C()