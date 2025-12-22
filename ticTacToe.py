import math
import random
import platform
import os

gameOver = False

userChar = ""
compChar = ""

UNDERLINE = '\x1b[4m'
UNDEREND = '\x1b[0m'

def clrScr():
  if platform.system() == "Windows":
    os.system('cls')
  else:
    os.system('clear')

def boardInit():
  rows = 3
  cols = 3
  board = [['_' for _ in range(cols)] for _ in range(rows)]
  return board

def printBoard(board):
  top = "  _   _   _"
  print(top)
  for rows in board:
    row = '|'
    for columns in rows:
      row = row + f' {columns}' + ' |'
    print(row)

def validate(entry):
  if type(entry[0]) == int and entry[1] == '-' and type(entry[2]) == int:
    if entry[0] in range(0, 3) and entry[2] in range(0, 3):
      return True
    else:
      return 'F2'
  else:
    return False

def charChoice():
  global userChar
  global compChar
  dummyFlag = False
  while True:
    clrScr()
    if dummyFlag:
      dummyFlag = False
      print("Invalid choice: please select X or O.")
    choice = input("Would you like to play as X or O? ").upper()
    if choice in ["X", "O"]:
      break
    else:
      dummyFlag = True
  if choice == "X":
    userChar = UNDERLINE + "X" + UNDEREND
    compChar = UNDERLINE + "O" + UNDEREND
  else:
    userChar = UNDERLINE + "O" + UNDEREND
    compChar = UNDERLINE + "X" + UNDEREND

def inputLogic():
  clrScr()
  board = boardInit()
  instructions = "Choose a spot on the grid by row and column, seperated by a dash; for example, '1-1' for the center square or 0-2 for the top right (indexes start at 0, not 1)"
  charChoice()
  while gameOver == False:
    clrScr()
    printBoard(board)
    print("\n" + instructions + "\n")
    user_choice = input("Enter your choice: ")
    # spreads user entry into a list, keeping strings as strings but casting them to int if they are numbers
    entry = [int(char) if char.isdigit() else char for char in user_choice]
    # instead of running validation for both of the conditions below, run it once then evaluate the output
    validation = validate(entry)
    if validation == True:
      if board[entry[0]][entry[2]] == "_":
        board[entry[0]][entry[2]] = userChar
      else:
        print("Square already occupied, please choose another.")
        return
    elif validation == "F2":
        print("Choice not in range: no row or column index is less than 0 or greater than 2. Please try again.")
        return
    else:
      print("Invalid entry, please try again.")
      return
inputLogic()