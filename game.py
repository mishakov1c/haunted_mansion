import pygame
from config import ENEMIES_AMOUNT, ENEMY_SPEED, PLAYER_SPEED
from enums import Move_direction
from game_object import GameObject
from pygame.mixer import Sound
from pygame.sprite import Group, spritecollide
from random import randint, choice
from text import Text


class Player(GameObject):
    sprite_filename = 'player'


class Wall(GameObject):
    sprite_filename = 'wall'


class Coin(GameObject):
    sprite_filename = 'coin'


class Ghost(GameObject):
    sprite_filename = 'ghost'
    move_direction = Move_direction.D
      

def draw_whole_screen(screen, context):
    screen.fill((100, 240, 230))
    context['player'].draw(screen)
    context['walls'].draw(screen)
    context['coin'].draw(screen)
    Text(f'SCORE: {context["score"]}').draw(screen, (10, 10))

    for i in range(ENEMIES_AMOUNT):
        context[f'ghost{i}'].draw(screen)

def all_coordinates(screen_width, screen_heigth, wall_block_width, wall_block_heigth):
    all_block_coordinates = []
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_heigth // wall_block_heigth    

    for horiz_block_num in range(horizontal_wall_blocks_amount):
        for vert_block_num in range(vertical_wall_blocks_amount):
            all_block_coordinates.append(
                (horiz_block_num * wall_block_width, vert_block_num * wall_block_heigth)
            )

    return all_block_coordinates


def calculate_walls_coordinates(screen_width, screen_heigth, wall_block_width, wall_block_heigth):
    walls_coordinates = []
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_heigth // wall_block_heigth

    for block_num in range(horizontal_wall_blocks_amount):
        
        walls_coordinates.extend([
            (block_num * wall_block_width, 0), 
            (block_num * wall_block_width, screen_heigth - wall_block_heigth)
        ])

    for block_num in range(1, vertical_wall_blocks_amount - 1):
        walls_coordinates.extend([
            (0, (block_num * wall_block_heigth)),
            (screen_width - wall_block_width, block_num * wall_block_heigth)
        ])
        
        gate_position = randint(1, horizontal_wall_blocks_amount - 3)
        if block_num % 3 == 0:
            for hor_num_block in range(horizontal_wall_blocks_amount):
                if hor_num_block != gate_position and hor_num_block != gate_position + 1:
                    walls_coordinates.append(
                        (hor_num_block * wall_block_width, block_num * wall_block_heigth)    
                    )    

    return walls_coordinates


def compose_context(screen):
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    all_block_coordinates = all_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    empty_cells_coordinates = list(set(all_block_coordinates) - set(walls_coordinates))

    context = {
        'player': Player(screen.get_width() - Wall.width * 2, Wall.height),
        'walls': Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        'empty_cells_coordinates': empty_cells_coordinates,
        'coin': Coin(200, 200),
        'score': 0,
        'game_over': "",        
    }

    for i in range(ENEMIES_AMOUNT):
        empty_cell_top_left = get_empty_cell_coordinate(context)
        context[f'ghost{i}'] = Ghost(empty_cell_top_left[0], empty_cell_top_left[1])
   
    return context


def get_empty_cell_coordinate(context):
    return choice(context['empty_cells_coordinates'])


def player_make_move(context, keys):
    old_player_top_left = context['player'].rect.topleft

    if keys[pygame.K_w]:
        context['player'].rect = context['player'].rect.move(0, -1*PLAYER_SPEED)
    if keys[pygame.K_s]:
        context['player'].rect = context['player'].rect.move(0, PLAYER_SPEED)
    if keys[pygame.K_a]:
        context['player'].rect = context['player'].rect.move(-1*PLAYER_SPEED, 0)
    if keys[pygame.K_d]:
        context['player'].rect = context['player'].rect.move(PLAYER_SPEED, 0)

    if spritecollide(context['player'], context['walls'], dokill=False):
        context['player'].rect.topleft = old_player_top_left


def make_enemy_move(enemy, walls):
    old_enemy_top_left = enemy.rect.topleft

    if enemy.move_direction == Move_direction.W:
        enemy.rect = enemy.rect.move(0, -1*ENEMY_SPEED)
    if enemy.move_direction == Move_direction.A:
        enemy.rect = enemy.rect.move(0, ENEMY_SPEED)
    if enemy.move_direction == Move_direction.S:
        enemy.rect = enemy.rect.move(-1*ENEMY_SPEED, 0)
    if enemy.move_direction == Move_direction.D:
        enemy.rect = enemy.rect.move(ENEMY_SPEED, 0)        

    if spritecollide(enemy, walls, dokill=False):
        enemy.rect.topleft = old_enemy_top_left
        enemy.move_direction = choice([direction for direction in Move_direction])


def game_over(screen):
    game_over_sound = Sound('resources/game_over.wav')
    game_over_sound.play()
    Text('GAME OVER').draw(screen, None)
    pygame.display.update()
    pygame.time.wait(5000)


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("haunted mansion")
    clock = pygame.time.Clock()
    running = True
    
    context = compose_context(screen)
    coin_sound = Sound('resources/coin_1.ogg')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)

        pygame.display.flip()         

        keys = pygame.key.get_pressed()

        player_make_move(context, keys)
        
        if context['player'].is_collided_with(context['coin']):
            keep_coin(context, coin_sound)

        for i in range(ENEMIES_AMOUNT):
            make_enemy_move(context[f'ghost{i}'], context['walls'])

            if context['player'].is_collided_with(context[f'ghost{i}']):
                game_over(screen)
                running = False

        clock.tick(60) / 1000

    pygame.quit()

def keep_coin(context, coin_sound):
    context['score'] += 1
    coin_sound.play()
    context['coin'].rect.topleft = get_empty_cell_coordinate(context)


if __name__ == '__main__':
    main()
