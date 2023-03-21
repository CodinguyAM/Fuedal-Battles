import tkinter as tk
from tkinter import messagebox
import copy
from PIL import ImageTk, Image
#standard check-all-row code: range(mfx + int((mtx - mfx)/abs(mtx - mfx)), mtx, int((mtx-mfx)/abs(mtx-mfx)))
#standard check-all-column code: range(mfy + int((mty - mfy)/abs(mty - mfy)), mty, int((mty-mfy)/abs(mty-mfy)))

def olb(board):
  r = []
  for row in board:
    r.extend(row)
  return r

def dispBoard(board):
  global bunchobuttons
  print()
  bob = bunchobuttons
  ob = olb(board)
  for x in range(187):
    if x % 11 == 0:
      print()
    if ob[x] not in [".", "|"]:
      bob[x]["text"] = ob[x].upper()
      print(ob[x], end=" ")
      if ob[x] in list("dlbckf"):
        bob[x]["fg"] = "blue"
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
    #print("Reached Ckechpoint 2", x, " ABCDEFGHIJKLMNO"[x])

  for x in range(1, 10):
    bunchobuttons[x]["fg"] = "white"
    bunchobuttons[x]["text"] = " 123456789"[x]
    bunchobuttons[x + 176]["fg"] = "white"
    bunchobuttons[x + 176]["text"] = " 123456789"[x]
  print()
  print()


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
  mty = int(mt[0])
  mtx = int(mt[1])
  if mfx < 0 or mfy < 0 or mtx < 0 or mty < 0 or mfx >= len(board[0]) or mfy >= len(board) or mtx >= len(board[0]) or mty >= len(board):
    return 'Off the Board!'
  piece = board[mfy][mfx]
  dest_piece = board[mty][mtx]
  if piece in [".", "|"]:
    return "Moving a board square would be strange."
  adj_pcs = list(adj(board, mfx, mfy).values())
  if mfx < 0 or mfy < 0 or mtx < 0 or mty < 0 or mfx > len(board[0]) or mfy > len(board) or mtx > len(board[0]) or mty > len(board):
    return 'Off the Board!'
  if move == 0 and piece == piece.upper():
    return "Blue is trying to move a green piece"
  if move == 1 and piece == piece.lower():
    return "Green is trying to move a blue piece"
  if move == 1 and dest_piece == dest_piece.upper() and not dest_piece == ".":
    return "Green is taking their own piece"
  if move == 0 and dest_piece == dest_piece.lower() and not dest_piece == ".":
    return "Blue is taking their own piece"
  if piece.upper() == "D":
    #Duke code
    #If squre is not adjacent
    if (mtx, mty) not in adj(board, mfx, mfy).keys():
      #duke not allowed
      return "Dukes can only move to adjacent squares."
    
    if adj_pcs.count('K') + adj_pcs.count("k") >= 1:
      #duke can go any adj with king near
      board[mfy][mfx] = "."
      board[mty][mtx] = piece
      
      return board
    if adj_pcs.count('B') + adj_pcs.count('b') >= 1:
      #duke can go any diag adj with countess near
      if (mtx, mty) not in [(mfx + 1, mfy + 1), (mfx - 1, mfy + 1), (mfx + 1, mfy - 1), (mfx -1, mfy - 1)]:
        return "This duke has taken the power of a countess, and can only move to squares diagonally adjacent to it."
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
    if adj_pcs.count('C') + adj_pcs.count('c') >= 1:
      #duke can go any hv adj with count near
      if (mtx, mty) not in [(mfx, mfy + 1), (mfx - 1, mfy), (mfx, mfy - 1), (mfx + 1, mfy)]:
        return "This duke has taken a count's power, along with the limitations of the count. Thus, it can only move horizontally and vertically."
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
    if move == 1:
      #normal duke movement.
      if (mtx, mty) not in [(mfx + 1, mfy + 1), (mfx - 1, mfy + 1)]:
        return "This duke has no power, and as such, can only move to the squares diagonally in front of it."
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = "D"
        return board
    elif  move == 0:
      if (mtx, mty) not in [(mfx + 1, mfy - 1), (mfx - 1, mfy - 1)]:
        return "This duke has no power, and as such, can only move to the squares diagonally in front of it."
      else:
        board[mfy][mfx] = "."
        board[mty][mtx] = "d"
        return board
  
  elif piece.upper() == "L":
    if (mtx, mty) in adj(board, mfx, mfy):
      return "The lord must jump over some pieces."
    if (not ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0))) or (mtx, mty) in adj(board, mfx, mfy).keys():
      #if not hv
      return "The lord can only move horizontally and vertically."
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
        return "You can't drive over a broken bridge - this section of pieces is not continuous."
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
        return  "You can't drive over a broken bridge - this section of pieces is not continuous."
  elif piece.upper() == "C":
    if (not ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0))):
      #if not hv
      if abs(mtx - mfx) == 2 and abs(mty - mfy) == 2:
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      return "The count can only move horizontally and vertically."
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
          return "The count cannot jump."
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
          return "The count cannot jump."
  elif piece.upper() == "B":
    if not (abs(mfx - mtx) == abs(mfy - mty)):
      #if not diag
      if (abs(mtx - mfx) == 2 and abs(mty - mfy) == 0) or (abs(mtx - mfx) == 0 and abs(mty - mfy) == 2):
        board[mfy][mfx] = "."
        board[mty][mtx] = piece
        return board
      return "The countess can only move diagonally."
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
        return "The countess cannot jump"
  elif piece.upper() == "K":
    if not ((( ((abs(mfx - mtx) == 0) or (abs(mfy - mty) == 0)))) or ((abs(mfx - mtx) == abs(mfy - mty)))):
      return "A king is a powerful piece, but it has its limitations - namely, it can only move horizontally, vertically, and diagonally."
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
          return "Kings cant do acrobatics!"
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
          return "Kings cant do acrobatics!"
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
          return "Kings cant do acrobatics!"
  else:
    return "Invalid Move"

def notate(played, board, move, ambiCheck=True):
  mf = played[0]
  mt = played[1]
  bx = mt[1]
  by = mt[0]
  base = board[int(mf[0])][int(mf[1])].upper() + " abcdefghijklmno"[int(by)] + " 123456789"[int(bx)]
  nboard = performMove(mf, mt, board, move)
  if type(nboard) == type(""):
    return None
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
      if type(performMove((sy, sx), {0:(15,5),1:(1,5)}[move], nboard, (move+1)%2)) != type(""):
        kfs = False
  if not kfs:
    vulnflag = "<|"
  amb=""
  if ambiCheck:
    for sx in range(1, 10):
      for sy in range(1, 16):
        if (notate(((sy, sx), mt), board, move, ambiCheck=False) == base + capture + attack + captureflag) and (((sy, sx), mt) != played):
          amb = "(" + " abcdefghijklmno"[int(mf[0])] + " 123456789"[int(mf[1])] + ")"
    move_notation = base + amb + capture + attack + captureflag + vulnflag
  else:
    move_notation = base + capture + attack + captureflag
  return move_notation
def main1():
  global board, mf, mt, partway, move, winner, notation, moves
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
      tk.messagebox.showinfo("Piece Information", infos[board[int(by)][int(bx)].lower()])
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
      print(mf, mt)
      nboard = performMove(mf, mt, board, move)
      if type(nboard) != type(""):
        
        
        move_notation = notate((mf, mt), board, move)
        labeltoadd = tk.Label(root, text=move_notation, fg=("blue", "green")[move])
        labeltoadd.grid(column = (2*int(moves/20)+{1:0,0:1}[move])+18 , row = int(((moves % 20)-{1:0,0:1}[move])/2))
        notation = notation + move_notation + ","







        
        board = nboard
        dispBoard(board)
        partway = 0
        move = (move + 1) % 2
        moves = moves + 1
      else:
        if nboard[-25:] == "is taking their own piece":
          for x in range(187):
            bunchobuttons[x]["background"] = truecolors[x]
          tk.messagebox.showinfo("Piece Information", infos[board[int(by)][int(bx)].lower()])
          mf = (by, bx)
          for n in range(187):
            sx = n % 11
            sy = int(n/11)
            if type(performMove(mf, (sy, sx), board, move)) != type(""):
              bunchobuttons[n]["background"] = "white"
          partway = 1
        else:
          tk.messagebox.showerror("Invalid Move", nboard)
          partway = 0
      
    if move == 1:
      playerText['text'] = "Player 1's Turn"
    else:
      playerText["text"] = "Player 2's Turn"
      
  ob = olb(board)
  if ob.count('f') == 0:
    playerText["text"] = "Player 1 Wins!"
    tk.messagebox.showinfo("Game Won", "Green Wins!")
    print(notation)
    winner = 1
  elif ob.count('F') == 0:
    playerText["text"] = "Player 2 Wins!"
    tk.messagebox.showinfo("Game Won", "Blue Wins!")
    print(notation)
    winner = 2

def main2():
  global root, cwidth, cheight, selectedSquare, bunchobuttons, bol, truecolors, infos, playerText, pieceInfoText, board  
  root = tk.Tk()
  #photo = ImageTk.PhotoImage((Image.open("rd.gif")).resize((30,30)))
  #x into y
  cwidth = 6
  cheight = 3
  root.title("Fuedal Battles")
  root.geometry("1100x700")
  selectedSquare = "none"
  bunchobuttons = []
  bol = []
  boi = []
  truecolors = []
  infos = {".":"A board square", "|":"A border", "d":"A duke. A duke can only ever move to a square adjacent to it. Normally, this is further restricted to only the two squares diagonally in front of it, but the duke can take the power of any piece adjacent to it. The order of precedence for such power taking is king, countess, count. Note that lordly, flagly, boardsquarely, and borderly powers are excluded as they would freeze a duke. Dukes are worth 2 points.", "l":"A lord. The lord moves by jumping over pieces, it cannot cross an empty square. It also cannot move to squares directly adjacent to it. It is worth 5 points.", "k":"A king. It can move horizontally, vertically, and diagonally, but cannot jump over other pieces. It is worth 15 points.", "b":"A countess. A countess can move diagonally, but cannot jump over pieces. However, it can move exactly two spaces horizontally xor vertically, regardless of whether there is a piece on the skipped square or not. It is worth 7 points.", "c":"A count. A count can move horizontally and vertically, but cannot jump over pieces. However, it can move exactly two spaces diagonally, regardless of whether there is a piece on the skipped square or not. It is worth 8 points.", "f":"A flag. It cannot move. The objective is to protect this piece from capture. The ||(pro. fort) symbol means threat to flag, <|(pro. backflag) means threat ignored, and |>(flag)  means flag captured."}
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
    apbut = tk.Button(root, text="", background=abg, width = cwidth, height=cheight, command = eval('ril' + str(x)))#, image=photo)
    bunchobuttons.append(apbut)
    #ablab = tk.Label(root, image = photo)
    #bol.append(ablab)
    #boi.append(photo)

  for x in range(187):
    but = bunchobuttons[x]
    #lab = bol[x]
    but.grid(column=int((x - (x % 11))/11), row = x % 11, sticky="NESW")
    #lab.grid(in_ = but)
  print(bunchobuttons)
  print("Reached Checkpoiunt no 1")

    

  playerText = tk.Label(root, text="Player 1's Turn")
  playerText.grid(row = 11, column = 7, columnspan = 3)
  pieceInfoText = tk.Label(root, text="")
  pieceInfoText.grid(row=12, column = 0, columnspan=3, rowspan = 3)
  dispBoard(board)
  tk.mainloop()

def main():
  main1()
  main2()

if __name__ == "__main__":
  main()
