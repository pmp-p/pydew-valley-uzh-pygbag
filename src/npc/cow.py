import math

import pygame

from src.enums import Layer
from src.npc.bases.cow_base import CowBase
from src.npc.behaviour.cow_behaviour_tree import CowIndividualContext
from src.settings import Coordinate
from src.sprites.setup import EntityAsset
from src.support import get_flight_matrix, near_tiles


class Cow(CowBase):
    def __init__(
        self,
        pos: Coordinate,
        assets: EntityAsset,
        groups: tuple[pygame.sprite.Group, ...],
        collision_sprites: pygame.sprite.Group,
    ):
        super().__init__(
            pos=pos,
            assets=assets,
            groups=groups,
            collision_sprites=collision_sprites,
            behaviour_tree_context=CowIndividualContext(self),
            z=Layer.MAIN,
        )

        self.fleeing = False

    def stop_moving(self):
        super().stop_moving()

        self.speed = 150
        self.fleeing = False

    def flee_from_pos(self, pos: tuple[int, int]) -> bool:
        """
        Aborts the current path of the cow and makes it flee into the opposite
        direction of the given position.
        :param pos: Position on the Tilemap that should be fled from
        """
        if not self.fleeing:
            self.abort_path()

            self.speed = 350
            self.fleeing = True

            # current NPC position on the tilemap
            tile_coord = self.get_tile_pos()

            flight_radius = 5

            flight_matrix = get_flight_matrix(
                pos=(tile_coord[0] - pos[0], tile_coord[1] - pos[1]),
                radius=5,
                # Further decreasing the angle value might make the cow's
                #  behaviour more predictable, but puts it at a higher risk of
                #  not finding any walkable area in the given angle, and thus
                #  leading to the cow fleeing in a random direction instead
                angle=math.pi / 4,
            )

            for x, y in near_tiles((flight_radius, flight_radius), flight_radius, shuffle=True):
                x_pos = x - flight_radius
                y_pos = y - flight_radius
                if not flight_matrix[y_pos][x_pos]:
                    continue
                x_coord = tile_coord[0] + x_pos
                y_coord = tile_coord[1] + y_pos
                if self.pf_grid.walkable(x_coord, y_coord):
                    if self.create_path_to_tile((x_coord, y_coord)):
                        return True

            for x, y in near_tiles((tile_coord[0], tile_coord[1]), flight_radius, shuffle=True):
                if self.pf_grid.walkable(x, y):
                    if self.create_path_to_tile((x, y)):
                        return True
        return False
