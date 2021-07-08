# TODO import the necessary classes and methods
import sys
from random import choice

sys.path.append('./aimapython')
from aimapython.utils import *
from aimapython.logic import *
from aimapython.notebook import psource


# init the global var for x axis(c) and y axis(d)
c, d = (3, 3)

# init the empty array
board = []

# init the empty list for both the rules and queries
rulesList, queriesList = ([], [])

# function that init the board based on the occurance of 0 and 1 randomly
def init_board():
	
	global Mxy, Bxy
	Mxy, Bxy = ([], [])

	for i in range(c):
		col = []
		MineCol = []
		BeepCol = []
		for j in range(d):
			# select the frequency either on 0 or 1
			frequency = choice([0, 1])
			# check if the frequency is 0 no mine or 1 mine
			if frequency == 1:
				col.append('M')
			else:
				col.append('-')
			
			# init the expressions with the same iteration 
			MineCol.append(expr('M'+str(i)+str(j)))
			BeepCol.append(expr('B'+str(i)+str(j)))

		board.append(col)
		Mxy.append(MineCol)
		Bxy.append(BeepCol)

# function that display the board
def displayBoard():
	print("++++++++++++++++++++++++++++++")
	for i in range(c):
		for j in range(d):
			print((board[i][j]), end=', ')
		print()
	print('++++++++++++++++++++++++++++++')	

# function that reads the data from the file 
def readFile(fileName):

	# open the file to read
	file_read = open(fileName, 'r')
	
	# linear transition in file 
	for line in file_read:
		# applying the condition to elininate the checks of thec comments
		if(line[0] != "#"):
			if ": R" in line:
				rulesList.append(line.split(' : R')[0])
			elif ": Q" in line:
				queriesList.append(line.split(' : Q')[0])
	
	# close the file
	file_read.close()


if __name__ == '__main__':
	
	input_file = sys.argv[1]

	# TODO 

	# read from the file
	readFile(input_file)
	# init the board
	init_board()

	# # init the object for the minesweap to create the initial KB using the Propositional Knowledge Base
	minesweap = PropKB()

	# Define Rules (dynamic logic required)
	# Defined for each square
	# By uncommenting you can add more rules
	
	# dynamic logic at O(n**2)
	for row in range(c):
		for col in range(d):
			# if the row is 0th and col is 0th
			if (row == 0 and col == 0):
				minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row][col+1] | Mxy[row+1][col] ))
			elif (row == 0 and col == d-1):
				minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row][col-1] | Mxy[row+1][col] ))
			elif (row == c-1 and col == 0 ):
				minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row-1][col] | Mxy[row][col+1]))
			elif (row == c-1 and col == d-1):
				minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row-1][col] | Mxy[row][col-1]))
			else:
				if (row == 0 and (col > 0 and col < d-1)):
					minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row][col-1] | Mxy[row][col+1] | Mxy[row+1][col] ))
				elif (row == c-1 and (col >= 0 and col <= d-1)):
					minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row][col-1] | Mxy[row][col+1] | Mxy[row-1][col] ))
				elif ( (row > 0 and row < d-1) and (col > 0 and col < d-1) ):
					minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row][col-1] | Mxy[row][col+1] | Mxy[row+1][col] | Mxy[row-1][col] ))
				elif (col == 0 and (row > 0 and row < c-1)):
					minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row+1][col] | Mxy[row-1][col] | Mxy[row][col+1] ))
				elif (col == d-1 and (row > 0 and row < c-1)):
					minesweap.tell(Bxy[row][col] | '<=>' | ( Mxy[row-1][col] | Mxy[row+1][col] | Mxy[row][col-1] ))

	# static defined rules
	# minesweap.tell(Bxy[0][0] | '<=>' | (Mxy[0][1] | Mxy[1][0]))
	# minesweap.tell(Bxy[0][1] | '<=>' | (Mxy[0][0] | Mxy[0][2] | Mxy[1][1]))
	# minesweap.tell(Bxy[0][2] | '<=>' | (Mxy[0][1] | Mxy[1][2]))
	# minesweap.tell(Bxy[1][0] | '<=>' | (Mxy[0][0] | Mxy[2][0] | Mxy[1][1]))
	# minesweap.tell(Bxy[1][1] | '<=>' | (Mxy[1][0] | Mxy[1][2] | Mxy[0][1] | Mxy[2][1]))
	# minesweap.tell(Bxy[1][2] | '<=>' | (Mxy[0][2] | Mxy[2][2] | Mxy[1][1]))
	# minesweap.tell(Bxy[2][0] | '<=>' | (Mxy[2][1] | Mxy[1][0]))
	# minesweap.tell(Bxy[2][1] | '<=>' | (Mxy[2][0] | Mxy[2][2]) | Mxy[1][1])
	# minesweap.tell(Bxy[2][2] | '<=>' | (Mxy[2][1] | Mxy[1][2]))

	# Adding the preceptions taken from the file to the knowledge base agent of minesweap
	for percept in rulesList:
		minesweap.tell(expr(percept))
	
	KBAgentProgram(minesweap)

	# # using the ask if method that will be do all the necessary conversions based on KB and entails to true or false, 
	# # instead of the tt_entails 
	for query in queriesList:
		# init the variables for the assumptions of the console board
		row = int(query[len(query) - 2])
		col = int(query[len(query) - 1])
		obj = ''
		if(query[0] == 'M' or query[0] == 'B'):
			obj = query[0]
		else:
			obj = query[1]
		
		# changing the value on the board
		board[row][col] = obj+str(row)+str(col)

		# uncomment the displayboard function to see the display board at rough assumptions.
		# print(displayBoard())

		# checking the index
		# using the ask_if_true function, as both tt_enails and ask_if_true takes same amount of time to execute
		if(tt_entails(Expr('&', *minesweap.clauses), expr(query))):
			print("Yes")
		else:
			print("No")

	# print(tt_entails(Expr('&', *minesweap.clauses), expr(queriesList[0])))

	
	