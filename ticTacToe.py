import math
import time
import random
import platform
import sys
import cursor
import os

gameOver = False

diff = "E"

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

def difficulty():
  dummyFlag = False
  global diff
  while True:
    clrScr()
    if dummyFlag:
      dummyFlag = False
      print("Invalid choice:")
    choice = input("Please enter 'e' to play easy mode, or 'h' for hard: ").upper()
    if choice in ["E", "H"]:
      if choice == "H":
        diff = "H"
      break
    else:
      dummyFlag = True

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

def winCheck(board, useCase):
  diagFall = [board[0][0], board[1][1], board[2][2]]
  diagRise = [board[2][0], board[1][1], board[0][2]]
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
      if winner == cVic:
        return 1
      else:
        return -1
  # checks for diagonal victories
  if all(x == userChar for x in diagFall) or all(x == userChar for x in diagRise):
      return result(uVic, useCase)
  if all(x == compChar for x in diagFall) or all(x == compChar for x in diagRise):
      return result(cVic, useCase)
  # checks for row victories
  for rows in board:
    if all(x == userChar for x in rows):
      return result(uVic, useCase)
    if all(x == compChar for x in rows):
      return result(cVic, useCase)
  # checks for column victories
  i = 0
  cols = len(board[0])
  while i < cols:
    if all(row[i] == userChar for row in board):
      return result(uVic, useCase)
    if all(row[i] == compChar for row in board):
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
      return 0
  return None

def comPlayer(board):
    randRow = random.randrange(len(board))
    randCol = random.randrange(len(board[randRow]))
    randPick = board[randRow][randCol]
    if randPick == "_":
      board[randRow][randCol] = compChar
      winCheck(board, 'norm')
      #miniMax(board, True)
    else:
      comPlayer(board)

def geniusComPlayer(board):
  emptyCheck = all(char == "_" for row in board for char in row)
  if emptyCheck:
    randRow = random.randrange(len(board))
    randCol = random.randrange(len(board[randRow]))
    board[randRow][randCol] = compChar
  else:
    best_score = -math.inf
    best_move = None
    for moves in get_moves(board):
      board[moves[0]][moves[1]] = compChar
      score = miniMax(board, False)
      board[moves[0]][moves[1]] = "_"
      if score > best_score:
        best_score = score
        best_move = [moves[0], moves[1]]
    board[best_move[0]][best_move[1]] = compChar
    winCheck(board, 'norm')
  
def get_moves(board):
  indexed_elements = [[i, j] for i in range(len(board)) for j in range(len(board[0])) if board[i][j] == '_']
  #print(f"potential moves: {indexed_elements}")
  return indexed_elements

def miniMax(board, isMax):
  terminal = winCheck(board, False)
  if terminal != None:
    return terminal
  
  if isMax:
    best_score = -math.inf
    for moves in get_moves(board):
      board[moves[0]][moves[1]] = compChar
      score = miniMax(board, False)
      board[moves[0]][moves[1]] = "_"
      best_score = max(best_score, score)
    return best_score
  
  else:
    best_score = math.inf
    for moves in get_moves(board):
      board[moves[0]][moves[1]] = userChar
      score = miniMax(board, True)
      board[moves[0]][moves[1]] = "_"
      best_score = min(best_score, score)
    return best_score

def inputLogic():
  clrScr()
  board = boardInit()
  instructions = "Choose a spot on the grid by row and column, seperated by a dash; for example, '1-1' for the center square or 0-2 for the top right (indexes start at 0, not 1)"
  difficulty()
  charChoice()
  order = coinFlip()
  bogey = False
  if order == False:
    if diff == "H":
      geniusComPlayer(board)
    else:
      comPlayer(board)
  while gameOver == False:
    clrScr()
    if bogey != False:
      print(bogey + "\n")
      bogey = False
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
        winCheck(board, 'norm')
        if gameOver == False:
          if diff == "H":
            geniusComPlayer(board)
          else:
            comPlayer(board)
      else:
        bogey = "Square already occupied, please choose another."
    elif validation == "F2":
      bogey = "Choice not in range: no row or column index is less than 0 or greater than 2. Please try again."
    else:
      bogey= "Invalid entry, please try again."

inputLogic()