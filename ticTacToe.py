import math
import time
import random
import platform
import os

gameOver = False

uFirst = True

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

def coinFlip():
  global uFirst
  flip = random.random()
  flipper = ['|', '/', '-', '\\']
  flipTimes = 6
  flipTicker = 0
  while flipTicker < flipTimes:
    for flips in flipper:
      clrScr()
      print(f'flipping a coin to determine who goes first: {flips}')
      time.sleep(0.08)
    flipTicker = flipTicker + 1
  if flip < 0.5:
    uFirst = False
    print("Computer has first move.")
    return False
  else:
    print("You have first move.")
    return True

def winCheck(board):
  global gameOver
  diagFall = [board[0][0], board[1][1], board[2][2]]
  diagRise = [board[2][0], board[1][1], board[0][2]]
  # checks for diagonal victories
  if all(x == userChar for x in diagFall) or all(x == userChar for x in diagRise):
    printBoard(board)
    print("Game over! You win!")
    gameOver = True
    return
  elif all(x == compChar for x in diagFall) or all(x == compChar for x in diagRise):
    printBoard(board)
    print("Game over! Computer wins!")
    gameOver = True
    return
  # checks for row victories
  for rows in board:
    if all(x == userChar for x in rows):
      printBoard(board)
      print("Game over! You win!")
      gameOver = True
      return
    elif all(x == compChar for x in rows):
      printBoard(board)
      print("Game over! Computer wins!")
      gameOver = True
      return
  # checks for column victories
  i = 0
  cols = len(board[0])
  while i < cols:
    if all(row[i] == userChar for row in board):
      printBoard(board)
      print("Game over! You win!")
      gameOver = True
      return
    elif all(row[i] == compChar for row in board):
      printBoard(board)
      print("Game over! Computer wins!")
      gameOver = True
      return
    i = i + 1
  #checks for a tie game
  all_match = all(char != "_" for row in board for char in row)
  if all_match == True:
    printBoard(board)
    print("Tie game!")
    gameOver = True
    return

def comPlayer(board):
    randRow = random.randrange(len(board))
    randCol = random.randrange(len(board[randRow]))
    randPick = board[randRow][randCol]
    if randPick == "_":
      board[randRow][randCol] = compChar
      winCheck(board)
    else:
      comPlayer(board)

def inputLogic():
  clrScr()
  board = boardInit()
  instructions = "Choose a spot on the grid by row and column, seperated by a dash; for example, '1-1' for the center square or 0-2 for the top right (indexes start at 0, not 1)"
  charChoice()
  order = coinFlip()
  if order == False:
    comPlayer(board)
  while gameOver == False:
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
        winCheck(board)
        if gameOver == False:
          comPlayer(board)
      else:
        print("Square already occupied, please choose another.")
    elif validation == "F2":
      print("Choice not in range: no row or column index is less than 0 or greater than 2. Please try again.")
    else:
      print("Invalid entry, please try again.")

inputLogic()