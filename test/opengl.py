import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    w, h = 2560, 1440
    pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL | FULLSCREEN, vsync=1)

    glutInit()

    gluPerspective(45, (w//2)/h, 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    last = time.time()

    sample = 100
    i = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(0.1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, w // 2, h)
        Cube()
        glutWireTeapot(1)

        #glTranslatef(1, 0.0, 0)
        glViewport(w//2, 0, w//2, h)
        Cube()
        glutWireTeapot(1)
        #glTranslatef(-1, 0.0, 0)

        pygame.display.flip()
        pygame.time.wait(1)

        if i % sample == 0:
            now = time.time()
            print('FPS:', sample/(now - last))
            last = now
        i += 1


main()
