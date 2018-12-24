from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math

class interact():
    centre = np.array([[0],[0],[1]])
    points = np.array([[0.5,-0.5,-0.5,0.5],[0.5,0.5,-0.5,-0.5],[1,1,1,1]])
    OperatorRec = np.array([[0.5,-0.5,-0.5,0.5],[0.5,0.5,-0.5,-0.5],[1,1,1,1]])
    MouseDown = 0
    MouseX = 0
    MouseY = 0
    MouseXnow = 0
    MouseYnow = 0
    interactType = 0
    shear_direction = 0
    InteractMatrix = []
    windowWidth = 720
    windowHeight = 720
    def __init__(self):
        self.InteractMatrix = [self.shift, self.zoom, self.rotate, self.shear]

    # get matrix
    def shift(self, x, y):
        dx = x - self.MouseX
        dy = y - self.MouseY
        return np.array([[1, 0, dx],
                         [0, 1, dy],
                         [0, 0, 1]])
    def zoom(self, x, y):
        sx = (x - self.centre[0][0]) / (self.MouseX - self.centre[0][0]) 
        sy = (y - self.centre[1][0]) / (self.MouseY - self.centre[1][0]) 
        return np.array([[sx, 0, 0],
                         [0, sy, 0],
                         [0, 0, 1]])
    def rotate(self, x, y):
        theta = math.atan2(y-self.centre[1][0], x-self.centre[0][0]) - math.atan2(self.MouseY-self.centre[1][0], self.MouseX-self.centre[0][0])
        return np.array([[math.cos(theta),-math.sin(theta), 0],
                         [math.sin(theta), math.cos(theta), 0],
                         [0,                0,               1]])        
    def shear(self, x, y):
        dx = (x - self.MouseX) * self.shear_direction[0]
        dy = (y - self.MouseY) * self.shear_direction[1]
        
        return np.array([[1, dx, 0],
                         [dy, 1, 0],
                         [0, 0, 1]])
    
    def GetOperatorRec(self, points):
        minx = np.min(points[0])
        miny = np.min(points[1])
        maxx = np.max(points[0])
        maxy = np.max(points[1])
        return np.array([[maxx,minx,minx,maxx],[maxy,maxy,miny,miny],[1,1,1,1]])

    def Draw(self, points):
        glClear(GL_COLOR_BUFFER_BIT)
        #glColor3f(1, 0, 0)
        glBegin(GL_POLYGON)
        for i in range(4):
            glVertex2f(points[0][i], points[1][i])
        glEnd()

        rec = self.GetOperatorRec(points)
        glBegin(GL_LINE_LOOP)
        for i in range(4):
            glVertex2f(rec[0][i], rec[1][i])
        glEnd()

        centre = np.average(rec, axis = 1).reshape(3,1)

        R = pow(pow(rec[0][0]-centre[0][0], 2)+pow(rec[1][0]-centre[1][0], 2), 0.5)
        glBegin(GL_LINE_LOOP)
        for i in range(100):
            glVertex2f(centre[0][0] + R*math.sin(i/50*math.pi), centre[1][0] + R*math.cos(i/50*math.pi))
        glEnd()
        glFlush()

    def ActiveMotion(self, x, y):
        x = -1 + x / self.windowWidth * 2
        y = 1 - y / self.windowHeight * 2
        self.MouseXnow = x
        self.MouseYnow = y        
        points = self.points

        if self.MouseDown == 1 and self.interactType != -1:
            points = np.dot(self.shift(self.MouseX - self.centre[0][0], self.MouseY - self.centre[1][0]), points)
            points = np.dot(self.InteractMatrix[self.interactType](x, y), points)
            points = np.dot(self.shift(self.MouseX + self.centre[0][0], self.MouseY + self.centre[1][0]), points)
        self.Draw(points)

    def Display(self):
        points = []
        if self.MouseDown == 1:
            points = np.dot(self.shift(self.MouseX - self.centre[0][0], self.MouseY - self.centre[1][0]), self.points)
            points = np.dot(self.InteractMatrix[self.interactType](self.MouseXnow, self.MouseYnow), points)
            points = np.dot(self.shift(self.MouseX + self.centre[0][0], self.MouseY + self.centre[1][0]), points)
        else :
            points = self.points
        self.Draw(points)

    def MouseClick(self, button, state, x, y):
        x = -1 + x / self.windowWidth * 2
        y = 1 - y / self.windowHeight * 2        
        self.MouseXnow = x
        self.MouseYnow = y        
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                print("mouse down, ",x,y)
                self.MouseX = x
                self.MouseY = y
                self.MouseDown = 1
                # interact type 
                self.interactType = -1
                maxx = self.OperatorRec[0][0]
                minx = self.OperatorRec[0][1]
                miny = self.OperatorRec[1][3]
                maxy = self.OperatorRec[1][0]
                width = maxx - minx
                height = maxy - miny
                # near point
                for i in range(4):
                    if pow(x - self.OperatorRec[0][i], 2) + pow(y - self.OperatorRec[1][i], 2) < pow(min(width, height) * 0.1, 2):
                        self.interactType = 1
                        print("zoom")
                        return
                # near edge
                self.shear_direction = (0,0)
                if (abs(x - maxx) < width * 0.1 and y < maxy and y > miny):
                    self.shear_direction = (0, 1)
                if (abs(x - minx) < width * 0.1 and y < maxy and y > miny):
                    self.shear_direction = (0, -1)
                if (abs(y - maxy) < width * 0.1 and x < maxx and x > minx):
                    self.shear_direction = (1, 0)
                if (abs(y - miny) < width * 0.1 and x < maxx and x > minx):
                    self.shear_direction = (-1, 0)
                if (self.shear_direction != (0,0)):
                    self.interactType = 3
                    print("shear")
                    return
                # rotate
                if (abs(pow(x-self.centre[0][0], 2) + pow(y-self.centre[1][0], 2) - \
                        pow(maxx-self.centre[0][0], 2) - pow(maxy-self.centre[1][0], 2))) < \
                        pow(min(width, height) * 0.1, 2):
                    self.interactType = 2
                    print("rotate")
                    return
                # shift
                if (x < maxx - width*0.1 and x > minx + width*0.1 and y < maxy - height*0.1 and y > miny + height*0.1):
                    self.interactType = 0
                    print("shift")
                    return
                print("self.interactType = ", self.interactType)

            elif state == GLUT_UP:
                self.MouseDown = 0           
                self.points = np.dot(self.shift(self.MouseX - self.centre[0][0], self.MouseY - self.centre[1][0]), self.points)
                self.points = np.dot(self.InteractMatrix[self.interactType](x, y), self.points)
                self.points = np.dot(self.shift(self.MouseX + self.centre[0][0], self.MouseY + self.centre[1][0]), self.points)
                self.centre = np.average(self.points, axis = 1).reshape(3,1)
                self.OperatorRec = self.GetOperatorRec(self.points)

    def Reshape(self, w, h):
        self.windowWidth = w
        self.windowHeight = h


if __name__ == "__main__":	

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(720, 720)
    glutCreateWindow("interact")	
    ob = interact()
    ob.Draw(ob.points)
    glutMouseFunc(ob.MouseClick)    
    glutMotionFunc(ob.ActiveMotion)
    glutDisplayFunc(ob.Display)
    glutIdleFunc(ob.Display)
    #glutReshapeFunc(ob.Reshape())
    glutMainLoop()