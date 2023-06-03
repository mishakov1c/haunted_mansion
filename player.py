from config import PLAYER_SPEED
from game_object import GameObject
from pygame.sprite import spritecollide
import pygame

class Player(GameObject):
    sprite_filename = 'player'


    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__(topleft_x, topleft_y)


    def make_move(self, context: dict):
        old_player_top_left = context['player'].rect.topleft
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.rect = self.rect.move(0, -1*PLAYER_SPEED)
        if keys[pygame.K_s]:
            self.rect = self.rect.move(0, PLAYER_SPEED)
        if keys[pygame.K_a]:
            self.rect = self.rect.move(-1*PLAYER_SPEED, 0)
        if keys[pygame.K_d]:
            self.rect = self.rect.move(PLAYER_SPEED, 0)

        if spritecollide(self, context['walls'], dokill=False):
            self.rect.topleft = old_player_top_left