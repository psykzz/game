
import os
import math
import pygame
import random

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from entities import *

class EventManager(object):
    events = []
    last_event = 0
    cooldown = 3

    def trigger(self, game):
        if (self.last_event) < self.cooldown:
            self.last_event += float(game.delta) / 1000
            return
        self.last_event = 0
        total = sum(event.weight for event in self.events) 
        rand_weight = random.uniform(0, total)
        weight_so_far = 0
        for event in self.events:
            if weight_so_far + event.weight >= rand_weight:
                miss_fire = random.random() > (float(event.trigger_chance) / 100)
                if miss_fire:
                    return True
                return event.fire(game)
            weight_so_far += event.weight
        assert False, "Shouldn't get here"


class Event(object):
    weight = 1
    trigger_chance = 100


class SpawnZombie(Event):
    def fire(self, game):
        zombie = Zombie()
        x = random.randrange(game.screen.get_size()[0])
        y = random.randrange(game.screen.get_size()[1])
        zombie.move_to = Vector2(x, y)
        game.entity_manager.add(zombie)
