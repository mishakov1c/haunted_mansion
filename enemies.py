from config import ENEMY_SPEED
from enums import Move_direction
from game_object import GameObject
from pygame.sprite import spritecollide
from random import choice
from walls import Wall


class Ghost(GameObject):
    sprite_filename = 'ghost'
    move_direction = Move_direction.D


    def __init__(self, topleft_x: int, topleft_y: int):
        super().__init__(topleft_x, topleft_y)


    def make_move(self, walls: Wall) -> None:
        old_enemy_top_left = self.rect.topleft

        if self.move_direction == Move_direction.W:
            self.rect = self.rect.move(0, -1*ENEMY_SPEED)
        if self.move_direction == Move_direction.A:
            self.rect = self.rect.move(0, ENEMY_SPEED)
        if self.move_direction == Move_direction.S:
            self.rect = self.rect.move(-1*ENEMY_SPEED, 0)
        if self.move_direction == Move_direction.D:
            self.rect = self.rect.move(ENEMY_SPEED, 0)        

        if spritecollide(self, walls, dokill=False):
            self.rect.topleft = old_enemy_top_left
            self.move_direction = choice([direction for direction in Move_direction])
            