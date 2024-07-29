import numpy as np
import pygame
from pygame.locals import *
from evie.objloader import OBJ

from OpenGL.GL import *
from OpenGL.GLU import *

import time


def main():
    pygame.init()
    print('Display Initialised:', pygame.display.get_init())
    print('Display Driver:', pygame.display.get_driver())
    w, h = 2560, 1440
    pygame.display.set_mode((w, h), DOUBLEBUF | OPENGL | FULLSCREEN, vsync=1)
    ipd = 63e-3

    model = OBJ('../assets/models/untitled.obj')

    last = time.time()
    sample = 100
    speed = 5
    i = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(67, (w // 2) / h, 0.1, 50.0)
        glTranslatef(np.cos(i*speed/360)-ipd/2, 0.0, -6)

        glMatrixMode(GL_MODELVIEW)
        glViewport(0, 0, w // 2, h)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        model.render()
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(67, (w // 2) / h, 0.1, 50.0)
        glTranslatef(np.cos(i*speed/360) + ipd/2, 0.0, -6)

        glViewport(w//2, 0, w//2, h)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        model.render()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(1)

        if i % sample == 0:
            now = time.time()
            print('FPS:', sample/(now - last))
            last = now
        i += 1


main()
