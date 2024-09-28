from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

from src.npc.bases.chicken_base import ChickenBase
from src.npc.bases.cow_base import CowBase
from src.npc.bases.npc_base import NPCBase
from src.sprites.entities.player import Player


class AIData:
    Matrix: list[list[int]] = None
    Grid: Grid = None

    player: Player = None

    setup: bool = False

    @classmethod
    def update(cls, pathfinding_matrix: list[list[int]], player: Player) -> None:
        if not cls.setup:
            NPCBase.pf_finder = AStarFinder()
            ChickenBase.pf_finder = AStarFinder(
                diagonal_movement=DiagonalMovement.only_when_no_obstacle
            )
            CowBase.pf_finder = AStarFinder(
                diagonal_movement=DiagonalMovement.only_when_no_obstacle
            )

            cls.setup = True

        cls.Matrix = pathfinding_matrix
        cls.Grid = Grid(matrix=cls.Matrix)

        for ai in (NPCBase, ChickenBase, CowBase):
            ai.pf_matrix = cls.Matrix
            ai.pf_grid = cls.Grid

        cls.player = player
