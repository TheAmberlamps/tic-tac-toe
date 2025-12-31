import math
import time
import random
import platform
import sys
import cursor
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
  print(f"\nYou have chosen {userChar}.\n")

def coinFlip():
  global uFirst
  flip = random.random()
  flipper = ['|', '/', '-', '\\']
  flipTimes = 6
  flipTicker = 0
  cursor.hide()
  while flipTicker < flipTimes:
    for flips in flipper:
      # write gives you far more control over writing to console than a normal print statement
      # for example this is printing the text below, immediately displaying it, then returning the cursor to the beginning of the line and then over-writing the text with the updated text
      # this is possible because write doesn't automatically inject a new line at the end of the text it displays, allowing for multiple updates on the same line
      sys.stdout.write('\r')
      sys.stdout.write(f"Flipping a coin to determine who has the first move: {flips}")
      sys.stdout.flush()
      time.sleep(0.08)
    flipTicker = flipTicker + 1
  sys.stdout.write("\b")
  cursor.show()
  if flip < 0.5:
    sys.stdout.write(compChar + '\n\n')
    sys.stdout.flush()
    print("Computer has first move.")
    time.sleep(2.5)
    return False
  else:
    sys.stdout.write(userChar + "\n\n")
    sys.stdout.flush()
    print("You have first move.")
    time.sleep(2.5)
    return True

def winCheck(board, player, useCase):
  diagFall = [board[0][0], board[1][1], board[2][2]]
  diagRise = [board[2][0], board[1][1], board[0][2]]
  pChar = player
  uVic = "You win!"
  cVic = "Computer wins!"
  def result(winner, useCase):
    if useCase == 'norm':
      global gameOver
      clrScr()
      printBoard(board)
      print(f"Game over! {winner}")
      gameOver = True
    else:
      if winner == compChar:
        return 1
      else:
        return -1
  # checks for diagonal victories
  if all(x == pChar for x in diagFall) or all(x == pChar for x in diagRise):
    if pChar == userChar:
      return result(uVic, useCase)
    else:
      return result(cVic, useCase)
  # checks for row victories
  for rows in board:
    if all(x == pChar for x in rows):
      if pChar == userChar:
        return result(uVic, useCase)
      else:
        return result(cVic, useCase)
  # checks for column victories
  i = 0
  cols = len(board[0])
  while i < cols:
    if all(row[i] == pChar for row in board):
      if pChar == userChar:
        return result(uVic, useCase)
      else:
        return result(cVic, useCase)
    i = i + 1
  #checks for a tie game
  if all(char != "_" for row in board for char in row):
    if useCase == 'norm':
      global gameOver
      clrScr()
      printBoard(board)
      print("Tie game!")
      gameOver = True
      return
    else:
      return 3
  return 0

def comPlayer(board):
    randRow = random.randrange(len(board))
    randCol = random.randrange(len(board[randRow]))
    randPick = board[randRow][randCol]
    if randPick == "_":
      board[randRow][randCol] = compChar
      winCheck(board, compChar, 'norm')
    else:
      comPlayer(board)

def geniusComPlayer(board):
  emptyCheck = all(char == "_" for row in board for char in row)
  if emptyCheck:
    randRow = random.randrange(len(board))
    randCol = random.randrange(len(board[randRow]))
    board[randRow][randCol] = compChar
  else:
    print("just holding space")

def get_moves(board):
  indexed_elements = [(i, j, board[i][j]) for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == '_']
  print(f"potential moves: {indexed_elements}")
  return len(indexed_elements)

def miniMax(state):
  print("study the minimax that google spits out and implement it here")

def inputLogic():
  clrScr()
  board = boardInit()
  instructions = "Choose a spot on the grid by row and column, seperated by a dash; for example, '1-1' for the center square or 0-2 for the top right (indexes start at 0, not 1)"
  charChoice()
  order = coinFlip()
  bogey = False
  if order == False:
    comPlayer(board)
  while gameOver == False:
    clrScr()
    if bogey != False:
      print(bogey + "\n")
      bogey = False
    printBoard(board)
    print("\n" + instructions + "\n")
    print(get_moves(board))
    user_choice = input("Enter your choice: ")
    # spreads user entry into a list, keeping strings as strings but casting them to int if they are numbers
    entry = [int(char) if char.isdigit() else char for char in user_choice]
    # instead of running validation for both of the conditions below, run it once then evaluate the output
    validation = validate(entry)
    if validation == True:
      if board[entry[0]][entry[2]] == "_":
        board[entry[0]][entry[2]] = userChar
        winCheck(board, userChar, 'norm')
        if gameOver == False:
          comPlayer(board)
      else:
        bogey = "Square already occupied, please choose another."
    elif validation == "F2":
      bogey = "Choice not in range: no row or column index is less than 0 or greater than 2. Please try again."
    else:
      bogey= "Invalid entry, please try again."

inputLogic()