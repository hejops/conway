#!/usr/bin/env python3
"""
A simple Python implementation Conway's Game of Life I whipped up in a few
hours. Not intended to be memory efficient.

https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

"""
from copy import deepcopy
from random import randint
import os
import sys
import time

ALIVE = "O"
DEAD = " "
DENSITY = 25


class Cell:
    """Cell object, defined only by its coordinates"""

    def __init__(
        self,
        xpos: int,
        ypos: int,
        chance: int,
    ):
        self.alive = 0 if randint(0, 100) > chance else 1
        self.xpos = xpos
        self.ypos = ypos

    def die(self):
        """set alive to 0"""
        if self.alive:
            self.alive = 0

    def regen(self):
        """set alive to 1"""
        if not self.alive:
            self.alive = 1


class Board:
    """Board object, defined only by its dimensions"""

    def __init__(
        self,
        width: int,
        height: int,
        density: int = DENSITY,
    ):
        assert width > 0
        assert height > 0
        self.width = width
        self.height = height
        self.board = [
            [
                Cell(x, y, density)
                #
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    @staticmethod
    def print_row(row) -> str:
        """convenience function for __str__"""
        return "".join(ALIVE if cell.alive else DEAD for cell in row)

    def __str__(self) -> str:
        return "\n".join(self.print_row(row) for row in self.board)

    def neighbours(self, cell: Cell) -> int:
        """determine number of neighbours of <cell>"""
        nei = 0

        # get the 3x3 surrounding cells
        #
        #   0 1 2 3 4
        # 0 . . . . .
        # 1 . . . . .
        # 2 . X . . .	x=1,y=2
        # 3 . . . . .
        # 4 . . . . .
        #
        # the cell with coords 1,2 is accessed via board[2][1]
        # surely there is a better way to do this

        if cell.ypos > 0:
            # row above cell
            row_above = self.board[cell.ypos - 1]
            for ncell in row_above[cell.xpos - 1 : cell.xpos + 1]:
                if ncell.alive:
                    nei += 1

        row = self.board[cell.ypos]
        if cell.xpos > 0 and row[cell.xpos - 1].alive:
            nei += 1
        if cell.xpos < board.width - 1 and row[cell.xpos + 1].alive:
            nei += 1

        if cell.ypos < board.height - 1:
            # row below cell
            row_below = self.board[cell.ypos + 1]
            for ncell in row_below[cell.xpos - 1 : cell.xpos + 1]:
                if ncell.alive:
                    nei += 1

        return nei

    def advance(self):
        """
        Any live cell with two or three live neighbours survives.
        Any dead cell with three live neighbours becomes a live cell.
        All other live cells die in the next generation. Similarly, all other dead cells stay dead.
        """

        new_board = deepcopy(self.board)

        for row in self.board:
            # print(self.print_row(row))
            for cell in row:
                # print("x", cell.xpos, "y", cell.ypos, self.print_row(row))

                if cell.alive:
                    if self.neighbours(cell) in [2, 3]:
                        ...  # remain alive
                    else:
                        new_board[cell.ypos][cell.xpos].die()

                else:
                    if self.neighbours(cell) == 3:
                        new_board[cell.ypos][cell.xpos].regen()
                    else:
                        ...  # remain dead

        self.board = new_board
        del new_board


if __name__ == "__main__":
    size = os.get_terminal_size()

    if len(sys.argv) == 2:
        USER_DENSITY = sys.argv[1]
        if not (USER_DENSITY.isnumeric() and 0 < int(USER_DENSITY) < 100):
            raise ValueError("Density must be between 0 and 100 (exclusive)")
        DENSITY = int(USER_DENSITY)

    board = Board(
        width=size.columns,
        height=size.lines - 3,  # allow 3 lines for help + exit msgs + new shell prompt
        density=DENSITY,
    )

    try:
        while True:
            os.system("clear")  # sorry, windows users
            print(board)
            print("(exit: ctrl-c)")
            time.sleep(0.05)
            board.advance()
    except KeyboardInterrupt:
        OUTNAME = os.path.join(
            os.path.dirname(__file__),
            "conway.txt",
        )
        with open(OUTNAME, "w", encoding="utf-8") as f:
            f.writelines(str(board))
        print(f"The end; wrote to {OUTNAME}.")
        sys.exit()
