from Inner.fuedalbatels import performMove, olb
import math
import copy
import tkinter as tk

##King      - 15 pts
##Count     - 8 pts
##Countess  - 7 pts
##Lord      - 5 pts
##Duke      - 2 pts



emhnd = open('emcache.txt')
ephnd = open('epcache.txt')
bmhnd = open('bmcache.txt')
emcache = eval(emhnd.read())
epcache = eval(ephnd.read())
bmcache = eval(bmhnd.read())
emhnd.close()
ephnd.close()
bmhnd.close()
del emhnd
del ephnd
del bmhnd

def genposspairs(board, move):
    possPairs = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == {1:board[y][x].upper(), 0:board[y][x].lower()}[move]:
                piece = board[y][x].upper()
                if piece == 'K':
                  for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                      if (dx, dy) != (0, 0):
                        sx = x + dx
                        sy = x + dy
                        while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                          possPairs.append(((y, x), (sy, sx)))
                          sy = sy + dy
                          sx = sx + dx
                if piece == 'B':
                  possPairs.extend([((y, x), (y + 2, x)), ((y, x), (y - 2, x)), ((y, x), (y, x + 2)), ((y, x), (y, x - 2))])
                  for dx in [-1, 1]:
                    for dy in [-1, 1]:
                      if (dx, dy) != (0, 0):
                        sx = x + dx
                        sy = x + dy
                        while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                          possPairs.append(((y, x), (sy, sx)))
                          sy = sy + dy
                          sx = sx + dx
                if piece == 'C':
                  possPairs.extend([((y, x), (y + 2, x + 2)), ((y, x), (y - 2, x + 2)), ((y, x), (y + 2, x - 2)), ((y, x), (y - 2, x - 2))])
                  for dx in [0]:
                      for dy in [-1, 1]:
                        if (dx, dy) != (0, 0):
                          sx = x + dx
                          sy = x + dy
                          while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                            possPairs.append(((y, x), (sy, sx)))
                            sy = sy + dy
                            sx = sx + dx
                  for dx in [-1, 1]:
                      for dy in [0]:
                        if (dx, dy) != (0, 0):
                          sx = x + dx
                          sy = x + dy
                          while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                            possPairs.append(((y, x), (sy, sx)))
                            sy = sy + dy
                            sx = sx + dx
                if piece == 'L':
                  for dx in [0]:
                      for dy in [-1, 1]:
                        if (dx, dy) != (0, 0):
                          sx = x + dx
                          sy = x + dy
                          while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                            possPairs.append(((y, x), (sy, sx)))
                            sy = sy + dy
                            sx = sx + dx
                  for dx in [-1, 1]:
                      for dy in [0]:
                        if (dx, dy) != (0, 0):
                          sx = x + dx
                          sy = x + dy
                          while type(performMove((y, x), (sy, sx), board, move)) != type(''):
                            possPairs.append(((y, x), (sy, sx)))
                            sy = sy + dy
                            sx = sx + dx
                if piece == 'D':
                  for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                      sx = x + dx
                      sy = y + dy
                      if type(performMove((y, x), (sy, sx), board, move)) != type(''):
                        possPairs.append(((y, x), (sy, sx)))
    return possPairs
def tuplize(board):
  r = ()
  for row in board:
    r = r + tuple(row)
  return r
tz = tuplize
cnsdr = 0
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


##possPairs = []
##for x in range(11):
##    for y in range(17):
##        for sx in range(11):
##            for sy in range(17):
##                possPairs.append(((y,x),(sy,sx)))
def evalPos(board, wmat=0.981, wmob=0.018):
    global epcache
    if tz(board) in epcache.keys():
      return epcache[tz(board)]
    #print(len(board))
    #print(len(board[0]))
    if olb(board).count('f') == 0:
        epcache[tz(board)] = 100000
        return 1000
    elif olb(board).count('F') == 0:
        epcache[tz(board)] = -1 * 100000
        return -1000
    r = 0
    u = 0
    umat = 0
    umobs = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            mob = 0
            if board[y][x] == board[y][x].upper() and board[y][x] not in ['.','|']:
                umat = umat + {'f':0, 'k':15, 'c':8, 'b':7, 'l':5, 'd':2}[board[y][x].lower()]
    
    umob = len(genposspairs(board, 1))
    u = wmat * umat + wmob * umob
    
    l = 0
    lmat = 0
    lmobs = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            mob = 0
            if board[y][x] == board[y][x].lower() and board[y][x] not in ['.','|']:
                lmat = lmat + {'f':0, 'k':15, 'c':8, 'b':7, 'l':5, 'd':2}[board[y][x].lower()]
    lmob = len(genposspairs(board, 0))
    l = wmat * lmat + wmob * lmob
    #print(u, l, umat, umob, lmat, lmob, wmat, wmob)
    WQ = u - l
    epcache[tz(board)] = WQ
    return WQ
#                0    1    2    3    4    5    6    7    8    9    10
sb = [["|", "|", "|", "|", "|", "|", "|", "|", "|", "|", "|"],
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
print(evalPos(sb))
def evalMove(mf, mt, board, move):
    global cnsdr, emcache
    if (mf, mt, tz(board), move) in emcache.keys():
      return emcache[(mf, mt, tz(board), move)]
    cnsdr = cnsdr + 1
    print(cnsdr, 'moves evaluated')
    m=  {1:1, 0:-1}[move]
    #print(mf, mt)
    if type(performMove(mf, mt, board, move)) == type(''):
        emcache[(mf, mt, tz(board), move)] = -1 * 100000 
        return -1*math.inf
    else:
        s = evalPos(board)
        f = evalPos(performMove(mf, mt, board, move))
        emcache[(mf, mt, tz(board), move)] = m * (f-s)
        return m * (f-s)


def hem(board, move):
    possPairs = genposspairs(board, move)
                      
      
                  
                  
    return max(possPairs, key=lambda ty:{True: emb(ty,board,move), False: -1000}[notate(ty, board, move)[-2 * int(len(notate(ty, board, move)) >= 2)] != "<"])
def emb(t, b, m):
    return evalMove(t[0], t[1], b, m) 

def bestmove(board, move):
  global bmcache
  if (tz(board), move) in bmcache.keys():
    return bmcache[(tz(board), move)]
  possPairs = genposspairs(board, move)
  bm = max(possPairs, key=lambda ty:evalMove(ty[0],ty[1],board,move) - emb(hem(performMove(ty[0],ty[1],board,move), (move + 1) % 2), performMove(ty[0],ty[1],board,move), (move + 1) % 2))
  bmcache[(tz(board), move)] = bm
  return bm
      

mf = (0,0)
mt = (0,0)
winner = 3
partway = 0
move = 1
board = copy.deepcopy(sb)
notation = ''
moves = 0

def notate(played, board, move, ambiCheck=True):
  mf = played[0]
  mt = played[1]
  bx = mt[1]
  by = mt[0]
  base = board[int(mf[0])][int(mf[1])].upper() + " abcdefghijklmnopqrstuvwxyz"[int(by)] + " 123456789WXYZPQRS "[int(bx)]
  nboard = performMove(mf, mt, board, move)
  if type(nboard) == type(""):
    return 'blahblah!halbhalb'
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

def whenclicked(bx, by):
  global mf, mt, partway, move, board, playerText, winner, bunchobuttons, truecolors, infos, pieceInfoText, notation, moves, root, emcache, epcache
  if winner == 3:
    if move == 1:
      playerText['text'] = "Player 's Turn"
    else:
      playerText["text"] = "AI's Turn"
      m = hem(board, 0)
      nboard = performMove(m[0], m[1], board, 0)
      move_notation = notate((m[0], m[1]), board, move)
      print("MN: ", move_notation)
      labeltoadd = tk.Label(root, text=move_notation, fg='blue')
      labeltoadd.grid(column = (2*int(moves/20)+{1:0,0:1}[move])+18 , row = int(((moves % 20)-{1:0,0:1}[move])/2))
      notation = notation + move_notation + ","
      partway = 0
      moves = moves + 1
      move = 1
      board = nboard
      emwh = open('emcache.txt', 'w')
      epwh = open('epcache.txt', 'w')
      bmwh = open('bmcache.txt', 'w')
      emwh.write(str(emcache))
      epwh.write(str(epcache))
      bmwh.write(str(bmcache))
      emwh.close()
      epwh.close()
      bmwh.close()
      del emwh
      del epwh
      del bmwh
      dispBoard(board)
      playerText['text'] = "Player's Turn"
      return None
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
      playerText['text'] = "Player's Turn"
    else:
      playerText["text"] = "AI's Turn"
      
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



playerText = tk.Label(root, text="Player's Turn")
playerText.grid(row = 11, column = 7, columnspan = 3)
pieceInfoText = tk.Label(root, text="")
pieceInfoText.grid(row=12, column = 0, columnspan=3, rowspan = 3)
dispBoard(board)

def spct(txt, lng=75):
    r = ''
    for x in range(len(txt)):
        r = r + txt[x]
        if (x + 1) % lng == 0:
            r = r  + '\n'
    return r
piw = tk.Toplevel()
Qwert = 0
for qwr in infos.keys():
    ttxxtt = infos[qwr] + ". Its symbol is " + qwr.upper()
    lbl = tk.Label(piw, text=spct(ttxxtt), background={'B':'red', 'C':'green', 'K':'yellow', 'F':'blue', 'D':'cyan', 'L':'orange', '.':'white', '|':'white'}[qwr.upper()])
    lbl.grid(row = Qwert, column = 0)
    Qwert = Qwert + 1
    
    
tk.mainloop()
print(hem(sb, 1))
print(evalMove((2,3),(4,1),sb,1))
