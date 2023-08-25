import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

#dependency on CubeSolver.py (line ~26)
w = 'w'
g = 'g'
o = 'o'
b = 'b' 
r = 'r'
y = 'y'

'''
FF = [['r', 'b', 'o'], ['w', 'g', 'r'], ['g', 'y', 'o']]
DF = [['r', 'o', 'b'], ['w', 'w', 'y'], ['g', 'o', 'o']]
RF = [['w', 'g', 'g'], ['b', 'o', 'w'], ['y', 'r', 'g']]
LF = [['w', 'b', 'b'], ['r', 'r', 'o'], ['w', 'b', 'y']]
BF = [['r', 'g', 'b'], ['g', 'b', 'w'], ['y', 'g', 'o']]
TF = [['r', 'r', 'w'], ['o', 'y', 'y'], ['y', 'y', 'b']]
'''

ColorFaces = []
def GenerateColors():
    from CubeSolver import BF, LF, FF, RF, TF, DF
    global ColorFaces
    ColorFaces = []
    BFColors = BF
    LFColors = ''
    FFColors = ''
    RFColors = RF
    TFColors = ''
    DFColors = DF

    a1 = ''
    a2 = ''
    a3 = ''
    for i in range(3):
        for j in range(3):
            a1+=BFColors[i][2-j]
            a2+=RFColors[i][2-j]
            a3+=DFColors[2-i][j]
    BFColors = a1
    RFColors = a2
    DFColors = a3

    for i in range(3):
        for j in range(3):
            TFColors += TF[i][j]
            LFColors += LF[i][j]
            FFColors += FF[i][j]
    ColorFaces = [BFColors, LFColors, FFColors, RFColors, TFColors, DFColors]
    def ConvertColor():
        x = 0
        for ColorFace in ColorFaces:
            newList = []
            for j in range(9):
                CurrentColor = ColorFace[j]
                if CurrentColor == 'b':
                    newList.append((0,0,1))
                elif CurrentColor == 'r':
                    newList.append((0.88,0,0))
                elif CurrentColor == 'g':
                    newList.append((0.2,1,0))
                elif CurrentColor == 'o':
                    newList.append((1, 0.65, 0))
                elif CurrentColor == 'y':
                    newList.append((0.97,1,0))
                elif CurrentColor == 'w':
                    newList.append((1,1,1))
            ColorFace = newList
            ColorFaces[x] = ColorFace
            x+=1
    ConvertColor() 

GenerateColors()
# Done prev project and some new part

vertices = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1)
)

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,6),
    (5,1),
    (5,4),
    (5,6),
    (7,4),
    (7,6),
    (7,3)
)

surfaces = (
    (0,1,2,3),
    (3,2,6,7),
    (7,6,5,4),
    (4,5,1,0),
    (6,2,1,5),
    (0,4,7,3)
)

colors = (
    ('back'),
    ('left'),
    ('front'),
    ('right'),
    ('top'),
    ('down'),
)

def BackgroundCube():
    glBegin(GL_QUADS)
    BackgroundColor = (0.6,0.6,0.6)
    glColor3fv(BackgroundColor)
    rat = 25
    for surface in surfaces:
        for vertex in surface:
            glVertex3fv((rat*vertices[vertex][0], rat*vertices[vertex][1], rat*vertices[vertex][2]))
    glEnd()

positions = []
def positionGenerator():
    global positions
    minSpacingFactor = 2    #2
    EdgeSpaceFactor = 1.04  #1.04 
    for layer in range(3):
        for column in range(3):
            for row in range(3):
                s = minSpacingFactor*EdgeSpaceFactor
                positions.append(((row-1)*s,(1-layer)*s,(column-1)*s))
    positions = tuple(positions)
positionGenerator()

def Cube(piece):
    p = positions[piece]
    glPushMatrix()
    glTranslatef(p[0], p[1], p[2])
    CubePiece(piece)
    glPopMatrix()

Angle = 0
done, req = False, True
MoveSpeed = 1
move = []
x = 0
from CubeSolver import *
def MakeCube(Moves):
    global Angle, done, req, MoveSpeed, move, x
    if Angle >= 90:
        Angle = 0
        req = True
        move()
        GenerateColors()
    if req:
        if x < len(Moves): 
            move = Moves[x]
            x += 1
        else:
            move = ''
            done = True
        req = False
    if not done: 
        Angle += MoveSpeed
    for i in range(27):
        glPushMatrix()
        if move == U and i <= 8:
            glRotatef(Angle, 0, -1, 0)
        elif move == Ui and i <= 8:
            glRotatef(Angle, 0, 1, 0)
        elif move == R and (i-2)%3 == 0:
            glRotatef(Angle, -1, 0, 0)
        elif move == Ri and i%3 == 2:
            glRotatef(Angle, 1, 0, 0)
        elif move == L and i%3 == 0:
            glRotatef(Angle, 1, 0, 0)
        elif move == Li and i%3 == 0:
            glRotatef(Angle, -1, 0, 0)
        elif move == F and (i-6)%9 <= 2:
            glRotatef(Angle, 0, 0, -1)
        elif move == Fi and (i-6)%9 <= 2:
            glRotatef(Angle, 0, 0, 1)       
        elif move == D and i >= 18:
            glRotatef(Angle, 0, 1, 0)
        elif move == Di and i >= 18:
            glRotatef(Angle, 0, -1, 0)
        elif move == B and i%9 <= 2:
            glRotatef(Angle, 0, 0, 1)
        elif move == Bi and i%9 <= 2:
            glRotatef(Angle, 0, 0, -1)

        Cube(i)
        glPopMatrix()

def CubePiece(piece):
    glBegin(GL_QUADS)
    x = 0
    for surface in surfaces:
        glColor3fv((0,0,0))
        rem = piece%9
        if colors[x] == 'back' and (rem == 0 or rem ==1 or rem ==2):
            if piece<=2: glColor3fv(ColorFaces[0][piece])
            elif piece<=11: glColor3fv(ColorFaces[0][piece - 6])
            else: glColor3fv(ColorFaces[0][piece - 12])
        if colors[x] == 'left' and (rem == 0 or rem ==3 or rem ==6):
            glColor3fv(ColorFaces[1][int(piece/3)])
        if colors[x] == 'front' and (rem == 6 or rem ==7 or rem ==8):
            if piece<=8: glColor3fv(ColorFaces[2][piece-6])
            elif piece<=17: glColor3fv(ColorFaces[2][piece - 12])
            else: glColor3fv(ColorFaces[2][piece - 18])
        if colors[x] == 'right' and (rem == 2 or rem ==5 or rem ==8):
            glColor3fv(ColorFaces[3][int((piece-2)/3)])
        if colors[x] == 'top' and piece<=8:
            glColor3fv(ColorFaces[4][piece])
        if colors[x] == 'down' and piece>=18:
            glColor3fv(ColorFaces[5][piece - 18])
        x+=1
        for vertex in surface:
            glVertex3fv(vertices[vertex])
    glEnd()
    '''
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()
    '''
def VisualMod(Moves, Solve):
    global req, done
    doubleMoves = [U2, R2, F2, L2, D2, B2]
    ClockMoves = [U, R, F, L, D, B]
    AntiClockMoves = [Ui, Ri, Fi, Li, Di, Bi]
    newMoves = []
    for move in Moves:
        if move in doubleMoves:
            for i in range(2):
                newMoves.append(eval(str(move)[10]))
        else:
            newMoves.append(move)
    def ReverseAddition(newMoves):
        reverseMoves = []
        for move in newMoves[::-1]:
            if move in ClockMoves:
                reverseMoves.append(AntiClockMoves[ClockMoves.index(move)])
            else:
                reverseMoves.append(ClockMoves[AntiClockMoves.index(move)])
        newMoves += reverseMoves
    if Solve:
        ReverseAddition(newMoves)
        req = True
        done = False
    Moves[:] = newMoves

scramble()
MoveDecorator(ScramblingMoves)
VisualMod(ScramblingMoves, False)
def main():
    angleinc = 0
    relPosition = (0,0)
    initialPosition = (0,0)
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100)
    glTranslatef(0,0,-20)
    glRotatef(35,1,0,0); glRotatef(45,0,-1,0)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    VisualMod(ScramblingMoves, True)
            #elif event.type == MOUSEBUTTONDOWN:
            #    initialPosition = pygame.mouse.get_pos()
            elif pygame.mouse.get_pressed()[0]:
                relPosition = ((pygame.mouse.get_pos()[0] - initialPosition[0])*4, -(pygame.mouse.get_pos()[1] - initialPosition[1])*4)
                #relPosition = (initialPosition[0] - pygame.mouse.get_pos()[0], initialPosition[1] - pygame.mouse.get_pos()[1])
            '''
            elif event.type == MOUSEBUTTONUP:
                relPosition = (pygame.mouse.get_pos()[0] - initialPosition[0], pygame.mouse.get_pos()[1] - initialPosition[1])
                print(relPosition)
            '''
                
        #angleinc += 0.5
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
        BackgroundCube()
        glPushMatrix()
        glRotatef(relPosition[0]/8 , 0, 1, 0)
        glRotatef(relPosition[1]/8 , 1, 0, 0)

        MakeCube(ScramblingMoves)
        glPopMatrix()
        pygame.display.flip()
        pygame.time.wait(0)         
        
main()
