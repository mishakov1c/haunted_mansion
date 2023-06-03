import pygame
from coin import Coin
from config import ENEMIES_AMOUNT
from enemies import Ghost
from player import Player
from pygame.mixer import Sound
from pygame.sprite import Group
from random import choice
from text import Text
from typing import Any
from walls import Wall, calculate_walls_coordinates


def draw_whole_screen(screen: pygame.Surface, context: dict[str, Any]) -> None:
    screen.fill((100, 240, 230))
    context['walls'].draw(screen)
    context['player'].draw(screen)
    context['coin'].draw(screen)
    Text(f'SCORE: {context["score"]}').draw(screen, (10, 10))

    for i in range(ENEMIES_AMOUNT):
        context[f'ghost{i}'].draw(screen)


def all_coordinates(
        screen_width: int,
        screen_heigth: int,
        wall_block_width: int,
        wall_block_heigth: int
) -> list[tuple[int, int]]:
    all_block_coordinates = []
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_heigth // wall_block_heigth    

    for horiz_block_num in range(horizontal_wall_blocks_amount):
        for vert_block_num in range(vertical_wall_blocks_amount):
            all_block_coordinates.append(
                (horiz_block_num * wall_block_width, vert_block_num * wall_block_heigth)
            )

    return all_block_coordinates


def compose_context(screen: pygame.Surface) -> dict[str, Any]:
    walls_coordinates = calculate_walls_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    all_block_coordinates = all_coordinates(screen.get_width(), screen.get_height(), Wall.width, Wall.height)
    empty_cells_coordinates = list(set(all_block_coordinates) - set(walls_coordinates))

    context = {
        'walls': Group(*[Wall(x, y) for (x, y) in walls_coordinates]),
        'coin': Coin(200, 200),
        'player': Player(screen.get_width() - Wall.width * 2, Wall.height),
        'empty_cells_coordinates': empty_cells_coordinates,
        'score': 0,
        'game_over': "",        
    }

    for i in range(ENEMIES_AMOUNT):
        empty_cell_top_left = get_empty_cell_coordinate(context)
        context[f'ghost{i}'] = Ghost(empty_cell_top_left[0], empty_cell_top_left[1])
   
    return context


def get_empty_cell_coordinate(context: dict[str, Any]) -> tuple[int, int]:
    return choice(context['empty_cells_coordinates'])


def game_over(screen: pygame.Surface) -> None:
    game_over_sound = Sound('resources/game_over.wav')
    game_over_sound.play()
    Text('GAME OVER').draw(screen, None)
    pygame.display.update()
    pygame.time.wait(5000)


def keep_coin(context: dict[str, Any], coin_sound: Sound) -> None:
    context['score'] += 1
    coin_sound.play()
    context['coin'].rect.topleft = get_empty_cell_coordinate(context)

    
def main() -> None:
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

        context['player'].make_move(context)
        
        if context['player'].is_collided_with(context['coin']):
            keep_coin(context, coin_sound)

        for i in range(ENEMIES_AMOUNT):
            context[f'ghost{i}'].make_move(context['walls'])

            if context['player'].is_collided_with(context[f'ghost{i}']):
                game_over(screen)
                running = False

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()