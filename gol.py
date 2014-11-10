from collections import namedtuple
import time
from itertools import imap, ifilter, groupby, chain
from utils import display, len, tail_call


EXTINCTION_THRESHOLD = 1
OVERPOPULATION_THRESHOLD = 4
REPRODUCTION_CONDITION = 3


class Grid(object):

  Cell = namedtuple("Cell", "x y")
  neighbors_coords = (Cell(-1, 1), Cell(0, 1), Cell(1, 1),
                      Cell(-1, 0), Cell(1, 0),
                      Cell(-1, -1), Cell(0, -1), Cell(1, -1))

  def __init__(self, conf):
    self.live_cells = frozenset(imap(lambda c: self.Cell(*c), conf))

  def __iter__(self):
    return iter(self.live_cells)

  def _count_neighbors(self, cell):
    return len(ifilter(lambda c: c in self.live_cells, self._get_neighboring_cells(cell)))

  def _get_neighboring_cells(self, cell):
    return frozenset(imap(lambda n: self.Cell(cell.x + n.x, cell.y + n.y), self.neighbors_coords))

  def _get_survivors(self):
    return frozenset(ifilter(lambda c: EXTINCTION_THRESHOLD < self._count_neighbors(c) <
                             OVERPOPULATION_THRESHOLD, self))

  def _get_newborns(self):
    return frozenset(imap(lambda (key, cells): key,
                          ifilter(lambda (key, cells): len(cells) == REPRODUCTION_CONDITION,
                                  groupby(sorted(chain(*imap(
                                                        lambda c: self._get_neighboring_cells(c),
                                                        self)))))))

  def next_generation(self):
    return Grid(self._get_survivors().union(self._get_newborns()))


def run():
  @tail_call
  def _run(grid):
    if grid.live_cells:
      display(grid)
      time.sleep(0.5)
      return _run(grid.next_generation())

  block = [(1, 1), (1, 2), (2, 1), (2, 2)]
  blinker = [(-1, 1), (-1, 2), (-1, 3)]
  glider = [(5, 4), (6, 4), (7, 4), (7, 5), (6, 6)]
  conf = block + glider + blinker

  _run(Grid(conf))
  print "GAME OVER!"


if __name__ == "__main__":
  run()
