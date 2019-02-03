#!/usr/bin/env python

# pygame modules
import pygame, sys
from pygame.locals import *


class Player:
    '''object representing the player'''

    
    def __init__(self, image, grav, posx, posy):
        resized = pygame.image.load(image)
        self.__image = pygame.transform.scale(resized, ((width//16)*3, (height//12)*3))
        self.__rect = self.__image.get_rect()
        self.__rect.bottom = posy
        self.__rect.left = posx
        self.__grav = grav
        self.__posx = posx
        self.__posy = posy
        self.__speed_x = 0
        self.__speed_y = 0
        self.__direction = True
        self.__removable = False

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
        
    @property
    def direction(self):
        return self.__direction

    @property
    def removable(self):
        return self.__removable

    @property
    def speed_x(self):
        return self.__speed_x

    @speed_x.setter
    def speed_x(self, speed):
        if ((speed < 0 and self.__direction > 0) or (speed > 0 and self.__direction == 0)):
            self.__image = pygame.transform.flip(self.__image, True, False)
            if speed > 0:
                self.__direction = 1
            elif speed < 0:
                self.__direction = 0
        self.__speed_x = speed

    def jump(self, speed):
        if self.__rect.bottom >= height:
            self.__speed_y = speed

    def update_position(self):

        if (self.__rect.bottom > height):
            self.__speed_y = 0
            self.__rect.bottom = height
        else:
            self.__speed_y += self.__grav

        self.__rect = self.__rect.move(self.__speed_x, self.__speed_y)
        
class Projectile:
    
    def __init__(self, image, player, grav, speed_x, speed_y, direction):
        resized = pygame.image.load(image)
        self.__image = pygame.transform.scale(resized, (width//16, height//12))
        self.__rect = self.__image.get_rect()
        self.__rect.bottom = (player.rect.top+player.rect.bottom)//2
        self.__rect.left = player.rect.left
        self.__grav = grav
        self.__direction = direction
        self.__removable = False
        if (self.__direction == False):
            pygame.transform.flip(self.__image, True, False)
            self.__speed_x = speed_x * -1
        else:
            self.__speed_x = speed_x
        self.__speed_y = speed_y

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def removable(self):
        return self.__removable

    @property
    def speed_x(self):
        return self.__speed_x

    def update_position(self):

        if (self.__rect.bottom > height or self.__rect.left < 0 or self.__rect.right > width):
            self.__speed_y = 0
            self.__speed_x = 0
            self.__removable = True
        else:
            self.__speed_y += self.__grav

        self.__rect = self.__rect.move(self.__speed_x, self.__speed_y)

def quit(image, win_width, win_height):
    image = pygame.image.load(image)
    image = pygame.transform.scale(image, (win_width//4, win_height//4))
    imageRect = image.get_rect()
    imageRect.bottom = (win_height//2) + (imageRect.bottom - imageRect.top)//2
    imageRect.right = (win_width//2) + (imageRect.right - imageRect.left)//2

    screen.blit(image, imageRect)
    pygame.display.flip()

    leave = True
    while leave:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if (event.key == K_RETURN):
                    sys.exit()
                if (event.key == K_ESCAPE):
                    leave = False
    

if __name__ == '__main__':
    pygame.init()

    timer = pygame.time.Clock()

    size = width, height = 640, 480
    screen = pygame.display.set_mode(size)
    background_image = pygame.transform.scale(pygame.image.load("court.jpg"), (width, height))

    lebron = Player("lebron.png", 1, 10, height)

    elements = [lebron]

    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit("esc_screen.png", width, height)


        keystate = pygame.key.get_pressed()

        lebron.speed_x = keystate[K_d]*5 - keystate[K_a]*5

        if (keystate[K_SPACE]):
            lebron.jump(-25)
        if (keystate[K_o] and len(elements) < 2):
            ball = Projectile("ball.png", lebron, 1, 8, -25, lebron.direction)
            elements += [ball]
        if (keystate[K_i] and len(elements) < 2):
            ball = Projectile("ball.png", lebron, 0, 25, 0, lebron.direction)
            elements += [ball]
        
        timer.tick(60)
        screen.blit(background_image, [0, 0])
        
        for i in range(len(elements)):
                elements[i].update_position()
                screen.blit(elements[i].image, elements[i].rect)
                if elements[i].removable == True:
                    del elements[i]

        pygame.display.flip()


