#!/usr/bin/env python
#
# motoman3d
#
# Olivier Francillon <olivier.francillon@nimag.net>
#
# License GPLv2+ applies
# -*- coding: utf-8 -*-

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from PIL import Image
import argparse
import sys
import csv

name = 'Motoman 3D'
minRotS = -180
maxRotS = 180
rotS = 0
rotL = 0
rotU = 0
rotR = 0
rotB = 0
rotT = 0
data = []
pngNumb = 0
save = False
###Variables d'animation
run = False
step = 0
turn = 0



def main(args):
    global save
    if args.file:
        loadAngles(args.file)
    save = args.save


    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800,800)
    glutCreateWindow(name)

    glClearColor(0.,0.,0.,1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [600.,3000,0.,1.]
    lightZeroColor = [250,250,250,1.0] #green tinged
    lightAmbiant = [250,250,250,1]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbiant)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,10000.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(2000,3000,5000,
              0,400,0,
              0,1,0)
    glPushMatrix()
    glutIdleFunc(anim)
    #loadAngles()
    glutMainLoop()
    return

def material(r, b, g):
    mat_diffuse=[r,b,g,1.0]
    mat_specular=[1,1,1,1]
    surf_shininess=[30]
    glMaterialfv(GL_FRONT,GL_DIFFUSE, mat_diffuse);
    glMaterialfv(GL_FRONT,GL_SPECULAR, mat_specular);
    glMaterialfv(GL_FRONT,GL_SHININESS, surf_shininess);

def loadAngles(file):

    with open(file) as f:
        global data
        data=[tuple(line) for line in csv.reader(f)]


    pass

def display():
    global pngNumb
    global save
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    #axes()
    elementS(rotS)
    elementL(rotL)
    elementU(rotU)
    elementR(rotR)
    elementB(rotB)
    elementT(rotT)
    glPopMatrix()
    if save and turn < 2:
        saveStuff()

    glutSwapBuffers()
    return

def saveStuff():
    global pngNumb

    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    data = glReadPixels(0, 0, 800, 800, GL_RGBA, GL_UNSIGNED_BYTE)


    image = Image.frombytes("RGBA", (800, 800), data)
    image2 = image.transpose(Image.FLIP_TOP_BOTTOM)
    #image.show()
    name = 'out_%s.png' %(pngNumb)
    image2.save(name, 'PNG')

    pngNumb += 1


def anim():
    global rotS
    global rotL
    global rotU
    global rotR
    global rotB
    global rotT

    global data
    global step
    global run
    global turn
    run = False

    rotS = animToGo(rotS, 0)
    rotL = animToGo(rotL, 1)
    rotU = animToGo(rotU, 2)
    rotR = animToGo(rotR, 3)
    rotB = animToGo(rotB, 4)
    rotT = animToGo(rotT, 5)

    if run == False:
        if step == len(data) -1:
            step = 0
            turn += 1

        else:
            step += 1

    glutPostRedisplay()

def animToGo(angle, numAngle):
    global run
    global data

    tmp = data[step]

    if angle != int(tmp[numAngle]):
        run = True
        if int(tmp[numAngle]) > angle:
            angle += 1
        else:
            angle -= 1
    return angle


def elementS(rotation):
    sizeX=300.
    sizeY=535.
    sizeZ=300.
    material(255,0,0)

    glPushMatrix()
    glRotate(rotation,0,1,0)
    glTranslatef(0,sizeY/2,0.)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()


def elementL(rotation):
    sizeX=140.
    sizeY=730.
    sizeZ=140.
    material(0,255,0)

    glPushMatrix()
    glRotate(rotS,0,1,0)

    glPushMatrix()
    glTranslatef(150.,  535.,0.)
    glRotate(rotation,0,0,1)
    glTranslate(0,sizeY/2,0)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def elementU(rotation):
    sizeX=200.
    sizeY=280.
    sizeZ=200.
    material(0,0,255)

    glPushMatrix()
    glRotate(rotS,0,1,0)

    glPushMatrix()
    glTranslate(150.,535.,0.)

    ## Rotation L
    glRotate(rotL,0,0,1)
    glTranslatef(0, 730.,0.)

    glRotate(rotation,0,0,1)
    glTranslate(sizeX/2,sizeY/2,0)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()



def elementR(rotation):
    sizeX=765.
    sizeY=120.
    sizeZ=120.
    material(255,255,0)
    glPushMatrix()
    glRotate(rotS,0,1,0)
    glPushMatrix()
    glTranslate(150.,535.,0.)


    ## Rotation L
    glRotate(rotL,0,0,1)
    glTranslatef(0, 730.   ,0.)

    ## Rotation U
    glRotate(rotU,0,0,1)
    glTranslatef(0,140,0)

    glRotate(rotation,1,0,0)
    glTranslate(sizeX/2,0,0)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def elementB(rotation):
    sizeX=105.
    sizeY=130.
    sizeZ=130.
    material(0,255,255)
    glPushMatrix()
    glRotate(rotS,0,1,0)

    glPushMatrix()
    glTranslate(150.,535.,0.)


    ## Rotation L
    glRotate(rotL,0,0,1)
    glTranslatef( 0,  730.  ,0.)

    ## Rotation U
    glRotate(rotU,0,0,1)
    glTranslatef(765.,140,0)

    ## Rotation R
    glRotate(rotR,1,0,0)
    #glTranslatef(0,140,0)

    glRotate(rotation,0,0,1)
    glTranslate(sizeX/2,0,0)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def elementT(rotation):
    sizeX=20.
    sizeY=100.
    sizeZ=100.
    material(255,0,255)
    glPushMatrix()
    glRotate(rotS,0,1,0)
    glPushMatrix()
    glTranslate(150.,535.,0.)


    ## Rotation L
    glRotate(rotL,0,0,1)
    glTranslatef( 0,   730.  ,0.)

    ## Rotation U
    glRotate(rotU,0,0,1)
    glTranslatef(765,140,0)

    ## Rotation R
    glRotate(rotR,1,0,0)
    #glTranslatef(0,140,0)

    ## Rotation B
    glRotate(rotB,0,0,1)
    glTranslatef(105.,0,0)

    glRotate(rotation,1,0,0)
    glTranslate(sizeX/2,0,0)
    glScalef(sizeX,sizeY,sizeZ)
    glutSolidCube(1)
    glPopMatrix()
    glPopMatrix()

def element(x,y,z,l,h,p):
    glPushMatrix()
    glTranslatef(x,y,z)
    glScalef(l,h,p)
    glutSolidCube(1)
    glPopMatrix()

def axes():
    #Ox rouge
    glPushMatrix()
    glColor3ub (255, 0, 0)
    glRotate(90,0,1,0)
    glScaled(100,100,1000)
    glTranslatef(0.5,0.0,0.0)
    #glutSolidCube (1.0)
    glutSolidCylinder(1,1,10,1)

    glPopMatrix()
    #Oy vert
    glPushMatrix()
    glColor3ub (0, 255, 0)
    glScaled(100,1000.0,100)
    glTranslatef(0.0,0.5,0.0)
    glutSolidCube (1.0)
    glPopMatrix()
    #Oz bleu
    glPushMatrix()
    glColor3ub (0, 0, 255)
    glScaled(100,100,1000.0)
    glTranslatef(0.0,0.0,0.5)
    glutSolidCube (1.0)
    glPopMatrix()



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='3D animation of Motoman robot with joint coordinates ')
  parser.add_argument('--save', '-s', action='store_true', help='enable png output of the animation')
  parser.add_argument('file', nargs='?', default=False, help='file csv with joint coordinates')
  args = parser.parse_args()

  main(args)


