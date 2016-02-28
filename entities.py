
import os
import math
import pygame
import random

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from components import *
from helpers import Vector2

class EntityManager(object):
    entities = pygame.sprite.Group()

    def __init__(self, game):
        self.game = game

    def __getattr__(self, name):
        method = getattr(self.entities, name)
        if method and callable(method):
            return method

    def update(self, delta):
        for entity in self.entities:
            entity.update(self.game)

    def fire_event(self, event):
        for entity in self.entities:
            entity.fire(self.game, event)


# Entities
class Entity(pygame.sprite.Sprite):
    rect = None
    image = None
    sprite = 'default.png'
    components = []

    _components = []

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.set_image(self.sprite, None)

        for component in self.components:
            cls = component(self)
            self._components.append(cls)

    @property
    def pos(self):
        return self.rect
    @pos.setter
    def pos(self, value):
        if isinstance(value, tuple):
            self.rect.update(*value)
        else:
            self.rect.update(value.x, value.y)


    def set_image(self, path, colorkey=None):
        fullname = os.path.join('data', path)
        try:
            self.image = pygame.image.load(fullname)
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

        if colorkey is not None:
            if colorkey is -1:
                colorkey = self.image.get_at((0,0))
            self.image.set_colorkey(colorkey, RLEACCEL)
        self.rect = self.image.get_rect()

    def update(self, game):
        pass

    def fire(self, game, event):
        pass

    def tick(self, game):
        for component in self._components:
            component.update(game)

        self.update(game)


# Entity List
class Zombie(Entity):
    sprite = 'zombie.png'
    move_to = None
    components = [Moveable, Debug]

    angle = 0

    def update(self, game):

        self.move_to = Vector2(0, 0)  # As a zombie we always have somewhere to move to.

        self.move_to.x = 100 * math.sin(self.angle) + 50
        self.move_to.y = 100 * math.cos(self.angle) + 50

        self.angle += 0.05

class Civilian(Entity):
    sprite = 'civilian.png'
    move_to = None
    components = [Moveable]


class Soldier(Entity):
    sprite = 'default.png'
    move_to = None
    components = [Moveable, Debug]
    def fire(self, game, event):
        if event.type == MOUSEBUTTONDOWN:
            self.move_to = Vector2(*pygame.mouse.get_pos())

            # Adjust based on the size of our rect.
            self.move_to.x -= self.pos.width / 2
            self.move_to.y -= self.pos.height / 2
            return


        # if event.type == KEYDOWN and event.key == K_w:
        #     self.interpolation += 0.1
        # if event.type == KEYDOWN and event.key == K_s:
        #     self.interpolation -= 0.1
        # if event.type == KEYDOWN and event.key == K_d:
        #     self.interpolation += 0.05
        # if event.type == KEYDOWN and event.key == K_a:
        #     self.interpolation -= 0.05
        # print(self.interpolation)   

