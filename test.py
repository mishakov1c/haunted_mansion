import pygame
from coin import Coin
from constants import ENEMIES_AMOUNT
from enemies import Ghost
from game_context import GameContext
from player import Player
from pygame.mixer import Sound
from pygame.sprite import Group
from random import choice
from text import Text
from walls import Wall, calculate_walls_coordinates


def draw_whole_screen(screen: pygame.Surface, context: GameContext) -> None:
    screen.fill((100, 240, 230))
    context.walls.draw(screen)
    context.player.draw(screen)
    context.coin.draw(screen)
    Text(f'SCORE: {context.score}').draw(screen, (10, 10))

    for ghost in context.ghosts:
        ghost.draw(screen)


def get_all_cells_coordinates(
    screen_width: int,
    screen_height: int,
    wall_block_width: int,
    wall_block_height: int,
) -> list[tuple[int, int]]:
    all_block_coordinates = []
    horizontal_wall_blocks_amount = screen_width // wall_block_width
    vertical_wall_blocks_amount = screen_height // wall_block_height

    for horizontal_block_num in range(horizontal_wall_blocks_amount):
        for vert_block_num in range(vertical_wall_blocks_amount):
            all_block_coordinates.append(
                (horizontal_block_num * wall_block_width, vert_block_num * wall_block_height),
            )

    return all_block_coordinates


def compose_context(screen_width: int, screen_height: int) -> GameContext:
    walls_coordinates = calculate_walls_coordinates(
        screen_width, screen_height,
        Wall.width,
        Wall.height,
    )
    all_cells_coordinates = get_all_cells_coordinates(
        screen_width,
        screen_height,
        Wall.width,
        Wall.height
    )
    walls = Group(*[Wall(x, y) for (x, y) in walls_coordinates])
    coin = Coin(200, 200)
    player = Player(screen_width - Wall.width * 2, Wall.height)
    ghosts = []

    empty_cells_coordinates = list(set(all_cells_coordinates) - set(walls_coordinates))

    for _ in range(ENEMIES_AMOUNT):
        empty_cell_top_left = choice(empty_cells_coordinates)
        empty_cells_coordinates.remove(empty_cell_top_left)
        ghosts.append(Ghost(empty_cell_top_left[0], empty_cell_top_left[1]))

    context = GameContext(
        walls=walls,
        coin=coin,
        player=player,
        score=0,
        ghosts=ghosts,
    )
    return context


def show_game_over(screen: pygame.Surface) -> None:
    game_over_sound = Sound('resources/game_over.wav')
    game_over_sound.play()
    Text('GAME OVER').draw(screen, None)
    pygame.display.update()
    pygame.time.wait(5000)


def keep_coin(context: GameContext, coin_sound: Sound) -> None:
    context.score += 1
    coin_sound.play()
    empty_cells_coordinates = list(set(context.empty_cells_coordinates) - set(context.walls_coordinates))
    context.coin.rect.topleft = choice(empty_cells_coordinates)


def main() -> None:
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("haunted mansion")
    clock = pygame.time.Clock()
    running = True

    context = compose_context(screen.get_width(), screen.get_height())
    coin_sound = Sound('resources/coin_1.ogg')

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_whole_screen(screen, context)

        pygame.display.flip()

        context.player.make_move(context.player.rect.topleft, context.walls)

        if context.player.is_collided_with(context.coin):
            keep_coin(context, coin_sound)

        for ghost in context.ghosts:
            ghost.make_move(context.walls)

            if context.player.is_collided_with(ghost):
                show_game_over(screen)
                running = False

        clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
