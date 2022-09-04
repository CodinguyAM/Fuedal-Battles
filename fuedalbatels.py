import tkinter as tk
from tkinter import messagebox
import copy
#standard check-all-row code: range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int((mtx-mfx)/abs(mtx-mfx)))
#standard check-all-column code: range(mfy + int((mty - mfy)/abs(mty - mfy)), mty, int((mty-mfy)/abs(mty-mfy)))

def olb(board):
  r = []
  for row in board:
    r.extend(row)
  return r

def dispBoard(board):
  global bunchobuttons
  bob = bunchobuttons
  ob = olb(board)
  for x in range(187):
    if x % 11 == 0:
      print()
    if ob[x] not in [".", "|"]:
      bob[x]["text"] = ob[x].upper()
      print(ob[x], end=" ")
      if ob[x] in list("dlbckf"):
        bob[x]["fg"] = "yellow"
      else:
        bob[x]["fg"] = "green"
    else:
      print(" ", end=" ")
      bob[x]["text"] = " "
  for x in range(1, 16):
    #bunchobuttons[x]["fg"] = "white"
    bunchobuttons[x * 11]["text"] = " ABCDEFGHIJKLMNO"[x]
    bunchobuttons[x * 11 + 10]["fg"] = "white"
    bunchobuttons[x * 11 + 10]["text"] = " ABCDEFGHIJKLMNO"[x]
    print("Reached Ckechpoint 2", x, " ABCDEFGHIJKLMNO"[x])

  for x in range(1, 10):
    bunchobuttons[x]["fg"] = "white"
    bunchobuttons[x]["text"] = " 123456789"[x]
    bunchobuttons[x + 176]["fg"] = "white"
    bunchobuttons[x + 176]["text"] = " 123456789"[x]


def adj(board, x, y):
  r = {}
  for dx in [-1, 0, 1]:
    for dy in [-1, 0, 1]:
      np = (x + dx, y + dy)
      if (dx, dy) == (0, 0):
        continue
      else:
        r[np] = board[np[1]][np[0]]
  return r
  

def performMove(mf, mt, boarda, move):
  ''' mf is a string/list/tuple of [y, x] form for where  the piece being moved is. mt is the same, but it describes the piece's destination. board is the current board. move is whose move it is 0 -> lowercase, 1 -> uppercase.'''
  board = []
  for x in range(len(boarda)):
    board.append(copy.copy(boarda[x]))
  mfy = int(mf[0])
  mfx = int(mf[1])
  piece = board[mfy][mfx]
  mty = int(mt[0])
  mtx = int(mt[1])
  dest_piece = board[mty][mtx]
  adj_pcs = list(adj(board, mfx, mfy).values())
  if piece in [".", "|"]:
    return "Moving a board square would be strange."
  if move == 0 and piece == piece.upper():
    return "Lower is trying to move an upper piece"
  if move == 1 and piece == piece.lower():
    return "Upper is trying to move a lower piece"
  if move == 1 and dest_piece == dest_piece.upper() and not dest_piece == ".":
    return "Upper is taking their own piece"
  if move == 0 and dest_piece == dest_piece.lower() and not dest_piece == ".":
    return "Lower is taking their own piece"
  if piece.upper() == "D":
    #Duke code
    #If squre is not adjacent
    if (mtx, mty) not in adj(board, mfx, mfy).keys():
      #duke not allowed
      return "Duke is trying to move to inadj square"
    
    if adj_pcs.count('K') + adj_pcs.count("k") >= 1:
      #duke can go any adj with king near
      board[mfy][mfx] = "."
      board[mty][mtx] = piece
      
      return board
    if adj_pcs.count('B') + adj_pcs.count('b') >= 1:
      #duke can go any diag adj with countess near
      if (mtx, mty) not in [(mfx + 1, mfy + 1), (mfx - 1, mfy + 1), (mfx + 1, mfy - 1), (mfx -1, mfy - 1)]:
        return "Duke with countess power is trying to move to indiag adj square"
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
    if adj_pcs.count('C') + adj_pcs.count('c') >= 1:
      #duke can go any hv adj with count near
      if (mtx, mty) not in [(mfx, mfy + 1), (mfx - 1, mfy), (mfx, mfy - 1), (mfx + 1, mfy)]:
        return "Duke with count power is trying to move to inhv adj square"
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
    if move == 1:
      #normal duke movement.
      if (mtx, mty) not in [(mfx + 1, mfy + 1), (mfx - 1, mfy + 1)]:
        return "Powerless duke cannot move much"
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = "D"
        return board
    elif  move == 0:
      if (mtx, mty) not in [(mfx + 1, mfy - 1), (mfx - 1, mfy - 1)]:
        return "Powerless due cannot move much"
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = "d"
        return board
  
  elif piece.upper() == "L":
    if (mtx, mty) in adj(board, mfx, mfy):
      return "Lord can not move to adj squares"
    if (not ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0))) or (mtx, mty) in adj(board, mfx, mfy).keys():
      #if not hv
      return "Lord can only move hv"
    #cant drive over a broken bridge. checks to see for gaps
    #vertically
    if abs(mfx - mtx) == 0:
      isl = True
      for y in range(mfy + int((mty - mfy)/abs(mty - mfy)), mty, int((mty-mfy)/abs(mty-mfy))):
        if board[y][mfx] == ".":
          isl = False
      if isl:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      else:
        return "Gaps in vertical bridge"
    #horizontally
    if abs(mfy - mty) == 0:
      isl = True
      for x in range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int((mtx-mfx)/abs(mtx-mfx))):
        if board[mfy][x] == ".":
          isl = False
      if isl:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      else:
        return "Gaps in horizontal bridge"
  elif piece.upper() == "C":
    if (not ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0))):
      #if not hv
      if abs(mtx - mfx) == 2 and abs(mty - mfy) == 2:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      return "Count can only move hv"
    else:
      if abs(mfy - mty) == 0:
        isl = True
        for x in range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int((mtx-mfx)/abs(mtx-mfx))):
          if board[mfy][x] != ".":
            isl = False
        if isl:
          board[mfy][mfx] = "."
          board[mty][mtx] = piece
          return board
        else:
          return "Count is tryingto jump vertically"
      if abs(mfx - mtx) == 0:
        isl = True
        for y in range(mfy + int((mty - mfy)/abs(mty - mfy)), mty, int((mty-mfy)/abs(mty-mfy))):
          if board[y][mfx] != ".":
            isl = False
        if isl:
          board[mfy][mfx] = "."
          board[mty][mtx] = piece
          return board
        else:
          return "Count is tryingto jump horizontally"
  elif piece.upper() == "B":
    if not (abs(mfx - mtx) == abs(mfy - mty)):
      #if not diag
      if (abs(mtx - mfx) == 2 and abs(mty - mfy) == 0) or (abs(mtx - mfx) == 0 and abs(mty - mfy) == 2):
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      return "Countess can only move diagonally"
    else:
      isl = True
      dy = int( (mty - mfy)/abs(mty - mfy) )
      for x in range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int( (mtx-mfx)/abs(mtx-mfx) )):
        if board[mfy + dy][x] != ".":
          isl = False
        dy = dy + int((mty-mfy)/abs(mty-mfy))
      if isl:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      else:
        return "Countess cannot jump"
  elif piece.upper() == "K":
    if not ((( ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0)))) or ((abs(mfx - mtx) == abs(mfy - mty)))):
      return "Even a king can only move hvd."
    else:
      if abs(mfy - mty) == 0:
        isl = True
        for x in range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int((mtx-mfx)/abs(mtx-mfx))):
          if board[mfy][x] != ".":
            isl = False
        if isl:
          board[mfy][mfx] = "."
          board[mty][mtx] = piece
          return board
        else:
          return "Kings cant do acrobatics! h"
      if abs(mfx - mtx) == 0:
        isl = True
        for y in range(mfy + int((mty - mfy)/abs(mty - mfy)), mty, int((mty-mfy)/abs(mty-mfy))):
          if board[y][mfx] != ".":
            isl = False
        if isl:
          board[mfy][mfx] = "."
          board[mty][mtx] = piece
          return board
        else:
          return "Kings cant do acrobatics! v"
      else:
        isl = True
        dy = int( (mty - mfy)/abs(mty - mfy) )
        for x in range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int( (mtx-mfx)/abs(mtx-mfx) )):
          if board[mfy + dy][x] != ".":
            isl = False
          dy = dy + int((mty-mfy)/abs(mty-mfy))
        if isl:
          board[mfy][mfx] = "."
          board[mty][mtx] = piece
          return board
        else:
          return "Kings cant do acrobatics! d"
  else:
    return "Upper, its a BOARD SQUARE, not a piece!"
      
      
board = [["|", "|", "|", "|", "|", "|", "|", "|", "|", "|", "|"],
         ["|", "D", "L", "C", "B", "F", "B", "C", "L", "D", "|"],
         ["|", "D", "L", "C", "B", "K", "B", "C", "L", "D", "|"],
         ["|", "D", "D", "D", "D", "D", "D", "D", "D", "D", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
         ["|", "d", "d", "d", "d", "d", "d", "d", "d", "d", "|"],
         ["|", "d", "l", "c", "b", "k", "b", "c", "l", "d", "|"],
         ["|", "d", "l", "c", "b", "f", "b", "c", "l", "d", "|"],
         ["|", "|", "|", "|", "|", "|", "|", "|", "|", "|", "|"]]

mf = (0, 0)
mt = (0, 0)
partway = 0
move = 1
winner = 3
notation = ""
moves= 0
def whenclicked(bx, by):
  global mf, mt, partway, move, board, playerText, winner, bunchobuttons, truecolors, infos, pieceInfoText, notation, moves, root
  if winner == 3:
    if move == 1:
      playerText['text'] = "Player 1's Turn"
    else:
      playerText["text"] = "Player 2's Turn"
    if partway == 0:
      for x in range(187):
        bunchobuttons[x]["background"] = truecolors[x]
      pieceInfoText["text"] = infos[board[int(by)][int(bx)].lower()]
      mf = (by, bx)
      for n in range(187):
        sx = n % 11
        sy = int(n/11)
        if type(performMove(mf, (sy, sx), board, move)) != type(""):
          bunchobuttons[n]["background"] = "white"
      partway = 1
    if partway == 1 and mf != (by, bx):
      for x in range(187):
        bunchobuttons[x]["background"] = truecolors[x]
      mt = (by, bx)
      nboard = performMove(mf, mt, board, move)
      if type(nboard) != type(""):
        base = board[int(mf[0])][int(mf[1])].upper() + " abcdefghijklmno"[int(by)] + " 123456789"[int(bx)]
        
        capture = ""
        if board[int(mt[0])][int(mt[1])] != ".":
          capture = "x" + board[int(mt[0])][int(mt[1])].upper()
          
        attack = ""
        if type(performMove((int(mt[0]), int(mt[1])), {0:(1,5),1:(15,5)}[move], nboard, move)) != type(""):
          attack = "||"
          
        captureflag = ""
        if board[int(mt[0])][int(mt[1])] in list("fF"):
          capture = ""
          captureflag = "|>"

        vulnflag = ""
        kfs = True
        for sx in range(1, 10):
          for sy in range(1, 16):
            if type(performMove((sy, sx), {0:(1,5),1:(15,5)}[move], nboard, (move+1)%2)) != type(""):
              kfs = False
        if not kfs:
          vulnflag = "<|"
        
        move_notation = base + capture + attack + captureflag
        labeltoadd = tk.Label(root, text=move_notation)
        labeltoadd.grid(column = (2*int(moves/10)+{1:0,0:1}[move])+18 , row = int(((moves % 10)-{1:0,0:1}[move])/2))







        
        board = nboard
        dispBoard(board)
        
        move = (move + 1) % 2
        moves = moves + 1
      else:
        tk.messagebox.showerror("Invalid Move", nboard)
      partway=0
    if move == 1:
      playerText['text'] = "Player 1's Turn"
    else:
      playerText["text"] = "Player 2's Turn"
      
  ob = olb(board)
  if ob.count('f') == 0:
    playerText["text"] = "Player 1 Wins!"
    winner = 1
  elif ob.count('F') == 0:
    playerText["text"] = "Player 2 Wins!"
    winner = 2
  
root = tk.Tk()
#x into y
cwidth = 6
cheight = 3
root.title("Fuedal Battles")
root.geometry("1100x700")
selectedSquare = "none"
bunchobuttons = []
bol = []
truecolors = []
infos = {".":"A board square", "|":"A border", "d":"A duke", "l":"A lord", "k":"A king", "b":"A countess", "c":"A count", "f":"A flag"}
for x in range(187):
  exec('def ril' + str(x) + '(): \n  whenclicked(' + str(x % 11) + ', ' + str((x - (x % 11))/11) + ')')
  if x % 11 in [0, 10]:
    
    abg = 'black'
  elif (x - (x % 11))/11 in [0, 16]:
    
    abg = 'black'
  elif (x % 2 == 0):
    
    abg='pink'
  else:
    
    abg = 'brown'
  truecolors.append(abg)
  apbut = tk.Button(root, text="", background=abg, width = cwidth, height=cheight, command = eval('ril' + str(x)))
  bunchobuttons.append(apbut)
  ablab = tk.Label(root, text="", background=abg, width = 1, height = 1)
  bol.append(ablab)

for x in range(187):
  but = bunchobuttons[x]
  lab = bol[x]
  but.grid(column=int((x - (x % 11))/11), row = x % 11, sticky="NESW")
  #lab.grid(in_ = but)
print(bunchobuttons)
print("Reached Checkpoiunt no 1")

  

playerText = tk.Label(root, text="Player 1's Turn")
playerText.grid(row = 11, column = 7, columnspan = 3)
pieceInfoText = tk.Label(root, text="")
pieceInfoText.grid(row=12, column = 0, columnspan=17, rowspan = 3)
dispBoard(board)
tk.mainloop()

