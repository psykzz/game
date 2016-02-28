
import os
import math
import pygame
import random

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from helpers import Vector2

# Components
class Component(object):
    def __init__(self, entity):
        self.entity = entity

    def update(self, game):
        pass

class Debug(Component):
    draw_position = True
    draw_speed = True

    def update(self, game):
        black = (0, 0, 0)
        message = self.get_string()
        text = game.font.render(message, True, black)
        game.background.blit(text, 
            (self.entity.pos.x + self.entity.pos.width*1.1, 
            self.entity.pos.y - self.entity.pos.height*1.1))

    def get_string(self):
        output = ""
        args = []

        if self.draw_position:
            output += "Pos:(%s, %s)"
            args += [self.entity.pos.x, self.entity.pos.y]
        return output % tuple(args)


class InterpolateMoveable(Component):
    interpolation = 0.65
    move_speed = 5

    def update(self, game):
        self.process_movement(game)

    def process_movement(self, game):
        if self.entity.move_to:
            if self.entity.rect != self.entity.move_to:
                speed = 1 / float(delta)
                current = Vector2.from_rect(self.entity.pos)
                new_pos = current.interpolate(self.entity.move_to, self.interpolation * speed)
                self.entity.pos.x = new_pos.x
                self.entity.pos.y = new_pos.y 

class Moveable(Component):
    move_speed = 5
    def update(self, game):
        self.process_movement(game)

    def process_movement(self, game):
        if self.entity.move_to:
            delta = game.delta
            delta /= 1000.0
            
            current = Vector2.from_rect(self.entity.pos)
            dist = self.entity.move_to - current
            dist.normalize()
            if not dist:
                return

            self.entity.pos.x += (dist.x * self.move_speed)
            self.entity.pos.y += (dist.y * self.move_speed)

            if self.entity.pos.collidepoint(self.entity.move_to):
                self.entity.move_to = None
        

# class Collidable(object):
#     def collide(self, other):
#         if not isinstance(other, Collidable):
#             return
#         if not self.rect or not other.rect:
#             return
