"""Directional utilities for problems that involve walking a 2-D grid."""

from enum import IntEnum

XYPos = tuple[int, int]


class Direction(IntEnum):
    """
    Helps with directionality in a 2-d grid. Examples:
    d = Direction.RIGHT
    d_vec = d.vector          # (1,0)
    pos = (0,0)
    pos = d.advance( pos, 3 ) # (3,0)
    d = d.turn( 1 )           # Direction.DOWN
    pos = d.advance( pos )    # (3,1)
    d = d.turn( -1 )          # Direction.RIGHT
    d = d.turn( 2 )           # Direction.LEFT
    d = Direction.from_line( (3,2), (1, 2) ) # Direction.LEFT
    """

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    __vectors = ((0, -1), (1, 0), (0, 1), (-1, 0))

    # Turns right by a number of right-angle turns. Pass negative to turn left.
    # Multiples of 2 are of course 180 degrees.
    # Example: Direction.RIGHT.turn( -1 ) => Direction.UP
    def turn(self, cw_count: int) -> "Direction":
        return self.__class__((self.value + cw_count) % len(Direction.__members__))  # type: ignore

    # Gets the unit vector associated with this direction
    # Example: Direction.DOWN => (0,1)
    @property
    def vector(self) -> XYPos:
        return self.__class__.__vectors[self.value]  # type: ignore

    # Advances the given position by [count] steps in this direction.
    # Example: Direction.RIGHT.advance( (0,0), 2 ) => (2,0)
    def advance(self, coord: XYPos, count: int = 1) -> XYPos:
        vec = self.vector
        return coord[0] + vec[0] * count, coord[1] + vec[1] * count

    # Given two points on a horizontal or vertical line
    # segment, returns the direction from the first to the second.
    # Example: Direction.from_line( (6,1), (6,3) ) => Direction.DOWN
    @classmethod
    def from_line(cls, p1: XYPos, p2: XYPos):
        vec = p2[0] - p1[0], p2[1] - p1[1]
        if mag := max(abs(vec[0]), abs(vec[1])):
            vec = vec[0] / mag, vec[1] / mag
        return Direction(cls.__vectors.index(vec))  # type: ignore
