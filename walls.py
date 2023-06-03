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
        
        gate_position = randint(1, horizontal_wall_blocks_amount - 3)
        if block_num % 3 == 0:
            for hor_num_block in range(horizontal_wall_blocks_amount):
                if hor_num_block != gate_position and hor_num_block != gate_position + 1:
                    walls_coordinates.append(
                        (hor_num_block * wall_block_width, block_num * wall_block_heigth)    
                    )    

    return walls_coordinates