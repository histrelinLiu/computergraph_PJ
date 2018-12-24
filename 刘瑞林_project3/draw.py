from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import math

class real():
    pyramid = [[0.1, 0.1, 0],[0.2, 0.7, 0],[0.7, 0.2, 0],[0.3, 0.3, 0.9]]
    cube = [[-0.3, -0.6, 0],[-0.3, -0.9, 0],[-0.6, -0.9, 0],[-0.6, -0.6, 0],[-0.3, -0.6, 0.5],[-0.3, -0.9, 0.5],[-0.6, -0.9, 0.5],[-0.6, -0.6, 0.5]]

    def po(self, a, b, c, d):
        glVertex3f(self.cube[a][0],self.cube[a][1],self.cube[a][2])
        glVertex3f(self.cube[b][0],self.cube[b][1],self.cube[b][2])
        glVertex3f(self.cube[c][0],self.cube[c][1],self.cube[c][2])
        glVertex3f(self.cube[d][0],self.cube[d][1],self.cube[d][2])

    def Draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        sun_light_position = [-2, -0.5, 2, 1.0]
        sun_light_ambient  = [0.0, 0.0, 0.0, 1.0]
        sun_light_diffuse  = [1.0, 1.0, 1.0, 1.0]
        sun_light_specular = [1.0, 1.0, 1.0, 1.0]

        glLightfv(GL_LIGHT0, GL_POSITION, sun_light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT,  sun_light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  sun_light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, sun_light_specular)

        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        
        ambient = sun_light_ambient
        diffuse = [1,1,1,1]
        specular = [0.0, 0.0, 0.0, 1.0]
        emission = [0.0, 0.0, 0.0, 1.0]
        shininess   = 0
        glMaterialfv(GL_FRONT, GL_AMBIENT,    ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE,    diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR,   specular)
        glMaterialfv(GL_FRONT, GL_EMISSION,   emission)
        glMaterialf (GL_FRONT, GL_SHININESS,  shininess)

        glBegin(GL_POLYGON)     
        glVertex3f(-1,-1,0)
        glVertex3f(1,-1,0)
        glVertex3f(1,1,0)
        glVertex3f(-1,1,0)
        glEnd()

        ambient = sun_light_ambient
        diffuse = [0.5, 0.5, 0.9, 1]
        specular = [0.0, 0.0, 0.0, 1.0]
        emission = [0.0, 0.0, 0.0, 1.0]
        shininess   = 0
        glMaterialfv(GL_FRONT, GL_AMBIENT,    ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE,    diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR,   specular)
        glMaterialfv(GL_FRONT, GL_EMISSION,   emission)
        glMaterialf (GL_FRONT, GL_SHININESS,  shininess)
        glBegin(GL_LINES)

        for i in range(3):
            for j in range(i+1, 4):
                glVertex3f(self.pyramid[i][0],self.pyramid[i][1],self.pyramid[i][2])
                glVertex3f(self.pyramid[j][0],self.pyramid[j][1],self.pyramid[j][2])

        glEnd()

        glBegin(GL_TRIANGLES)
        glColor3f(0.5, 0.5, 0.5)
        for i in range(3):
            for j in range(i+1, 3):
                for k in range(j+1, 4):
                    glVertex3f(self.pyramid[i][0],self.pyramid[i][1],self.pyramid[i][2])
                    glVertex3f(self.pyramid[j][0],self.pyramid[j][1],self.pyramid[j][2])
                    glVertex3f(self.pyramid[k][0],self.pyramid[k][1],self.pyramid[k][2])
        glEnd()

        glBegin(GL_POLYGON)        
        glColor3f(0.5, 0.5, 0.5)
        for i in range(4):
            self.po(0,1,2,3)
            self.po(0,1,5,4)
            self.po(1,2,6,5)
            self.po(2,3,7,6)
            self.po(3,0,4,7)
            self.po(4,5,6,7)
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        for i in range(7):
            for j in range(i+1, 8):
                glVertex3f(self.cube[i][0],self.cube[i][1],self.cube[i][2])
                glVertex3f(self.cube[j][0],self.cube[j][1],self.cube[j][2])
        glEnd()


        glFlush()

    def Reshape(self, w, h):
        self.windowWidth = w
        self.windowHeight = h


if __name__ == "__main__":	

    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowPosition(100, 200)
    glutInitWindowSize(720, 720)
    glutCreateWindow("real")	
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    gluLookAt(0,0,0,1,0.2,1,0,0,1)
    ob = real()    
    
    glutDisplayFunc(ob.Draw)
    glutIdleFunc(ob.Draw)
    #glutReshapeFunc(ob.Reshape())
    glutMainLoop()