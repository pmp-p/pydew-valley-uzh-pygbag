from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

import pygame

from src.npc.bases.cow_base import CowBase
from src.npc.behaviour.ai_behaviour_tree_base import (
    Action,
    Condition,
    Context,
    NodeWrapper,
    Selector,
    Sequence,
)
from src.npc.setup import AIData
from src.settings import SCALED_TILE_SIZE


@dataclass
class CowIndividualContext(Context):
    cow: CowBase


def wander(context: CowIndividualContext) -> bool:
    """
    Makes the Cow wander to a random location in a 5 tile radius.
    :return: True if path has successfully been created, otherwise False
    """
    # current position on the tilemap
    tile_coord = (
        pygame.Vector2(context.cow.rect.centerx, context.cow.rect.centery) / SCALED_TILE_SIZE
    )

    # To limit the required computing power, Cows currently only try to
    # navigate to 11 random points in their immediate vicinity
    # (5 tile radius)
    avail_x_coords = list(
        range(
            max(0, int(tile_coord.x) - 5),
            min(int(tile_coord.x) + 5, context.cow.pf_grid.width - 1) + 1,
        )
    )

    avail_y_coords = list(
        range(
            max(0, int(tile_coord.y) - 5),
            min(int(tile_coord.y) + 5, context.cow.pf_grid.height - 1) + 1,
        )
    )

    for _ in range(min(len(avail_x_coords), len(avail_y_coords))):
        pos = (random.choice(avail_x_coords), random.choice(avail_y_coords))
        avail_x_coords.remove(pos[0])
        avail_y_coords.remove(pos[1])

        if context.cow.create_path_to_tile(pos):
            break
    else:
        context.cow.abort_path()
        return False
    return True


# region flee behaviour
def player_nearby(context: CowIndividualContext) -> bool:
    distance_threshold = 2.5 * SCALED_TILE_SIZE
    current_distance = (
        (AIData.player.rect.center[0] - context.cow.rect.center[0]) ** 2
        + (AIData.player.rect.center[1] - context.cow.rect.center[1]) ** 2
    ) ** 0.5
    return current_distance < distance_threshold


def flee_from_player(context: CowIndividualContext) -> bool:
    return context.cow.flee_from_pos(
        (
            AIData.player.rect.centerx / SCALED_TILE_SIZE,
            AIData.player.rect.centery / SCALED_TILE_SIZE,
        )
    )


# endregion


class CowConditionalBehaviourTree(NodeWrapper, Enum):
    Wander = Selector(Action(wander))


class CowContinuousBehaviourTree(NodeWrapper, Enum):
    Flee = Selector(Sequence(Condition(player_nearby), Action(flee_from_player)))
