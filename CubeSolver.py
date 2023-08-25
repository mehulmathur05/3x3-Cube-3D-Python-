import random
w = 'w'
g = 'g'
o = 'o'
b = 'b' 
r = 'r'
y = 'y'
bufferPiece = 0
bufferArr = []
bufferFace = []
# Entries after inspection
FF = [[g,g,g],
      [g,g,g],
      [g,g,g]]
DF = [[w,w,w],
      [w,w,w],
      [w,w,w]]
RF = [[o,o,o],
      [o,o,o],
      [o,o,o]]
LF = [[r,r,r],
      [r,r,r],
      [r,r,r]]
BF = [[b,b,b],
      [b,b,b],
      [b,b,b]]
TF = [[y,y,y],
      [y,y,y],
      [y,y,y]]

def rft():  # rft --> rotate front to top
    global FF, TF, BF, LF, RF, DF, bufferFace
    
    BF = rotatedFaceClockwise(rotatedFaceClockwise(BF))         # to make the replacements work, reversing the colors of the Back face is required
    
    bufferFace = FF
    FF = DF
    DF = BF
    BF = TF
    TF = bufferFace
    
    BF = rotatedFaceClockwise(rotatedFaceClockwise(BF))         # reversing it again to follow our convention
    
    RF = rotatedFaceClockwise(RF)
    LF = rotatedFaceAntiClockwise(LF)

def rlt():  # rft --> rotate left to top
    global FF, TF, BF, LF, RF, DF, bufferFace
    bufferFace = rotatedFaceClockwise(TF)
    TF = rotatedFaceClockwise(LF)
    LF = rotatedFaceClockwise(DF)
    DF = rotatedFaceClockwise(RF)
    RF = bufferFace
    FF = rotatedFaceClockwise(FF)
    BF = rotatedFaceAntiClockwise(BF)

def rfl():  # rft --> rotate front to left
    global FF, TF, BF, LF, RF, DF, bufferFace
    bufferFace = FF
    FF = RF
    RF = BF
    BF = LF
    LF = bufferFace
    DF = rotatedFaceAntiClockwise(DF)
    TF = rotatedFaceClockwise(TF)

def rotatedFaceClockwise(Face):
    NewFace = [[0,0,0], [0,0,0], [0,0,0]]
    for j in range(3):
        for i in range(3):
            NewFace[j][i] = Face[2-i][j]
    return(NewFace)

def rotatedFaceAntiClockwise(Face):
    NewFace = [[0,0,0], [0,0,0], [0,0,0]]
    for j in range(3):
        for i in range(3):
            NewFace[j][i] = Face[i][2-j]
    return(NewFace)


def U():
    global FF, TF, BF, LF, RF, DF
    
    TF = rotatedFaceClockwise(TF)
    # Moving the side pieces which move with the top layer
    bufferArr = FF[0]
    FF[0] = RF[0]
    RF[0] = BF[0]
    BF[0] = LF[0]
    LF[0] = bufferArr

def Ui():
    for i in range(3):
        U()
        i += 1

def U2():
    for i in range(2):
        U()
        i += 1

def R():
    for i in range(3):
        rlt()
        i += 1
    U()
    rlt()

def Ri():
    for i in range(3):
        rlt()
        i += 1
    Ui()
    rlt()

def R2():
    for i in range(3):
        rlt()
    U2()
    rlt()

def L():
    rlt()
    U()
    for i in range(3):
        rlt()
        i += 1

def Li():
    rlt()
    Ui()
    for i in range(3):
        rlt()
        i += 1

def L2():
    rlt()
    U2()
    for i in range(3):
        rlt()

def F():
    rft()
    U()
    for i in range(3):
        rft()

def Fi():
    rft()
    Ui()
    for i in range(3):
        rft()

def F2():
    rft()
    U2()
    for i in range(3):
        rft()

def D():
    rft(); rft()
    U()
    rft(); rft() 

def Di():
    rft(); rft()
    Ui()
    rft(); rft() 

def D2():
    rft(); rft()
    U2()
    rft(); rft() 

def B():
    for i in range(3): rft()
    U(); rft()

def Bi():
    for i in range(3): rft()
    Ui(); rft()

def B2():
    for i in range(3): rft()
    U2(); rft()

def PrintCube() :
    for i in range(3): print(" "*16, TF[i])
    print()
    for i in range(3): print(LF[i],'', FF[i],'', RF[i],'', BF[i])
    print()
    for i in range(3): print(" "*16, DF[i])

def doMoves(arr):
    for i in range(len(arr)):
        arr[i]()

def MoveDecorator(moves):
    print('Scramble : |', end=" ")
    for i in range(len(moves)):
        print(str(moves[i])[10], end="")
        if str(moves[i])[11] != " ":
            print(str(moves[i])[11], end="")
        print(',', end=" ")
    print("|")

# Now just a random scrambler to scramble the cube
AvailableMoves = [R,R2,Ri,U,U2,Ui,F,F2,Fi,L,L2,Li,D,D2,Di,B,B2,Bi]

ScramblingMoves = []
def scramble():
    global ScramblingMoves
    ScrambleLength = random.randint(19,24)
    while len(ScramblingMoves) <= ScrambleLength:
        choice = random.choice(AvailableMoves)
        if len(ScramblingMoves) == 0 or str(choice)[10] != str(ScramblingMoves[len(ScramblingMoves) - 1])[10]:
            ScramblingMoves.append(choice)
        else: continue
    MoveDecorator(ScramblingMoves)

if __name__ == "__main__":
    scramble()
    doMoves(ScramblingMoves)
    print("FF =",FF,"DF =", DF,"RF =", RF,"LF =", LF,"BF =", BF,"TF =", TF)
    PrintCube()


''' Following part is incomplete (left for later)'''
# For the solver

# to find an edge
def EdgePieceLocator(Edge):
      EdgePieces = [[TF[0][1], BF[0][1]], [TF[1][2], RF[0][1]], [TF[2][1], FF[0][1]], [TF[1][0], LF[0][1]], [FF[1][0], LF[1][2]], [FF[1][2], RF[1][0]], [BF[1][0], RF[1][2]], [BF[1][2], LF[1][0]], [DF[0][1], FF[2][1]], [DF[1][2], RF[2][1]], [DF[2][1], BF[2][1]], [DF[1][0], LF[2][1]]]
      ReversedEdgePieces = []
      for i in range(len(EdgePieces)):
            ReversedEdgePieces.append(EdgePieces[i][::-1])
      try:
            return(EdgePieces.index(Edge))
      except:
            return(12 + (ReversedEdgePieces.index(Edge)))
      
# to find a corner
def CornerPieceLocator(Corner):
      CornerPieces = [[TF[0][0], LF[0][0], BF[0][2]], [TF[0][2], BF[0][0], RF[0][2]], [TF[2][2], RF[0][0], FF[0][2]], [TF[2][0], FF[0][0], LF[0][2]], [DF[0][0], LF[2][2], FF[2][0]], [DF[0][2], FF[2][2], RF[2][0]], [DF[2][2], RF[2][2], BF[2][0]], [DF[2][0], BF[2][2], LF[2][0]]]
      CornerPieces1 = []
      CornerPieces2 = []
      for i in range(len(CornerPieces)):
            CornerPieces1.append([CornerPieces[i][1], CornerPieces[i][2], CornerPieces[i][0]])
            CornerPieces2.append([CornerPieces[i][2], CornerPieces[i][0], CornerPieces[i][1]])
      try: 
            return(CornerPieces.index(Corner))
      except:
            try: return(8 + CornerPieces1.index(Corner))
            except: return(16 + CornerPieces2.index(Corner))

# Making the cross
'''
CrossSolution = []
def SolveCross():
    crossSolved = False
    gwe = False
    oye = False
    rwe = False
    bwe = False
    def do(Move):
        global CrossSolution
        if isinstance(Move, list): CrossSolution += Move
        else : CrossSolution.append(Move)
    while crossSolved == False:
        while gwe == False:
            edgeLocation = EdgePieceLocator([w,g])
            if edgeLocation == 8: gwe = True; print("Came")
            elif edgeLocation == 17 or 2 or 16: do(F)
            elif edgeLocation == 0 or 1 or 3: do(U)
            elif edgeLocation == 9 or 10 or 11: do(D)
            elif edgeLocation == 4 or 5 or 6 or 7 :
                if edgeLocation == 4: do(L, D)
                elif edgeLocation == 5: do([Ri, Di])
                elif edgeLocation == 6: do([R, Di])
                elif edgeLocation == 7: do([Li, D])
            elif edgeLocation == 18: do([R2, F])
            elif edgeLocation == 19: do([L2, Fi])
            elif edgeLocation == 12 or 22: do(B)
            elif edgeLocation == 14 or 20: do(F)
            elif edgeLocation == 13 or 21: do(R)
            elif edgeLocation == 15 or 23: do(L)
        crossSolved = True
print(EdgePieceLocator([w,g]))
SolveCross()
doMoves(CrossSolution)
PrintCube()
'''