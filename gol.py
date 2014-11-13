from collections import namedtuple
import time
from itertools import imap, ifilter, groupby, chain, izip
from utils import display, len as count, tailrec


EXTINCTION_THRESHOLD = 1
OVERPOPULATION_THRESHOLD = 4
REPRODUCTION_CONDITION = 3


class Grid(object):

  Cell = namedtuple("Cell", "x y")
  delta_coords = (Cell(-1, 1), Cell(0, 1), Cell(1, 1),
                  Cell(-1, 0), Cell(0, 0), Cell(1, 0),
                  Cell(-1, -1), Cell(0, -1), Cell(1, -1))

  def __init__(self, conf):
    self.live_cells = frozenset(imap(lambda c: self.Cell(*c), conf))

  def __iter__(self):
    return iter(self.live_cells)

  def _get_live_and_neighboring_cells(self, cell):
    return imap(lambda n: self.Cell(cell.x + n.x, cell.y + n.y), self.delta_coords)

  def _is_newborn(self, cell, neighbors):
    return cell not in self.live_cells and count(neighbors) == REPRODUCTION_CONDITION

  def _is_survivor(self, cell, neighbors_and_me):
    return (cell in self.live_cells and
            EXTINCTION_THRESHOLD < count(neighbors_and_me) - 1 < OVERPOPULATION_THRESHOLD)

  def _get_next_generation_cells(self):
    def _groupby_cell_coords(cells):
      return groupby(sorted(chain(*cells)))

    return next(izip(*ifilter(lambda cell_state: (self._is_newborn(*cell_state) or
                                                  self._is_survivor(*cell_state)),
                              _groupby_cell_coords(
                                imap(lambda cell: self._get_live_and_neighboring_cells(cell),
                                     self)))),
                iter([]))

  def next_generation(self):
    return Grid(self._get_next_generation_cells())


@tailrec
def run(grid):
  if grid.live_cells:
    display(grid)
    time.sleep(0.5)
    return run(grid.next_generation())


if __name__ == "__main__":
  block = [(1, 1), (1, 2), (2, 1), (2, 2)]
  blinker = [(-1, 1), (-1, 2), (-1, 3)]
  glider = [(5, 4), (6, 4), (7, 4), (7, 5), (6, 6)]
  conf = block + glider + blinker

  run(Grid(conf))
  print "GAME OVER!"
