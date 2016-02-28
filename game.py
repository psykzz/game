
import os
import math
import pygame
import random

from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

from events import *
from entities import *
from helpers import Vector2


class Game(object):
    def __init__(self, title="default title"):
        color = (255,255,255)
        self.screen = pygame.display.set_mode((1680, 1024))
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(color)

        self.entity_manager = EntityManager(self)
        self.event_manager = EventManager()

        self.clock = pygame.time.Clock()

        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("", 14)
        self._update_title(title)
        # pygame.mouse.set_visible(0)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.entity_manager.entities.draw(self.screen)
        pygame.display.flip()

    def _update_title(self, title):
        pygame.display.set_caption(title)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            self.entity_manager.fire_event(event)

        return True

    def handle_events(self):
        self.event_manager.trigger(self)

    def update_entities(self):
        for entity in self.entity_manager.entities:
            entity.tick(self)

    def run_forever(self):
        while True:
            self.delta = self.clock.tick(144)
            self._update_title("FPS: %s" % (self.clock.get_fps()))

            if not self.handle_input():
                break
            self.handle_events()
            self.update_entities()
            self.render()
        pygame.quit()



def main():
    game = Game()

    # Events
    zombie_spawner = SpawnZombie()
    game.event_manager.events.append(zombie_spawner)

    # Entities
    player = Soldier()
    game.entity_manager.add(player)

    game.run_forever()

if __name__ == '__main__':
    main()