from constants import GATE_EXPANSION_VALUE, INTERVAL_BETWEEN_WALLS
from game_object import GameObject
from random import randint


class Wall(GameObject):
    sprite_filename = 'wall'


def calculate_walls_coordinates(
        screen_width: int,
        screen_heigth: int,
        wall_block_width: int,
        wall_block_heigth: int
) -> list[tuple[int, int]]:

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

        if block_num % INTERVAL_BETWEEN_WALLS == 0:
            build_labirint_block(
                wall_block_width,
                wall_block_heigth,
                walls_coordinates,
                horizontal_wall_blocks_amount,
                block_num
            )

    return walls_coordinates


def build_labirint_block(
    wall_block_width: int,
    wall_block_heigth: int,
    walls_coordinates: list[tuple[int, int]],
    horizontal_wall_blocks_amount: int,
    block_num: int
) -> None:

    gate_position_limiter = 3
    gate_position = randint(1, horizontal_wall_blocks_amount - gate_position_limiter)

    for hor_num_block in range(horizontal_wall_blocks_amount):
        if (hor_num_block != gate_position
                and hor_num_block != gate_position + GATE_EXPANSION_VALUE):

            walls_coordinates.append(
                (hor_num_block * wall_block_width, block_num * wall_block_heigth)
            )
