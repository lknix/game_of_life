import unittest
from gol import Grid


class GolTestCase(unittest.TestCase):

  def setUp(self):
    self.conf = [(1, 1), (1, 2), (1, 3)]
    self.grid = Grid(self.conf)

  def test_should_create_grid_object(self):
    self.assertEquals(frozenset(self.conf), self.grid.live_cells)

  def test_should_count_neighbors(self):
    self.assertEquals(1, self.grid._count_neighbors(Grid.Cell(1, 1)))

  def test_should_get_no_survivors_due_to_extinction(self):
    conf = [(1, 1), (5, 5)]
    grid = Grid(conf)
    self.assertEquals(frozenset(), grid._get_survivors())

  def test_should_make_cell_die_due_to_overpopulation(self):
    conf = [(1, 1), (1, -1), (2, 1), (1, 0), (2, 0), (-1, -1)]
    grid = Grid(conf)
    self.assertFalse(Grid.Cell(1, 0) in grid._get_survivors())

  def test_should_get_one_survivor(self):
    conf = [(1, 1), (1, -1), (2, 0)]
    grid = Grid(conf)
    self.assertEquals(frozenset([Grid.Cell(2, 0)]), grid._get_survivors())

  def test_should_get_no_newborns(self):
    conf = [Grid.Cell(x=2, y=2), Grid.Cell(x=-8, y=-8)]
    grid = Grid(conf)
    self.assertEquals(frozenset(), grid._get_newborns())

  def test_should_get_one_newborn(self):
    conf = [Grid.Cell(x=1, y=1), Grid.Cell(x=2, y=0), Grid.Cell(0, -1)]
    grid = Grid(conf)
    self.assertEquals(frozenset([Grid.Cell(x=1, y=0)]), grid._get_newborns())


class GolBlinkerTestCase(unittest.TestCase):

  def setUp(self):
    self.conf = [(1, 1), (1, 2), (1, 3)]
    self.grid = Grid(self.conf)

  def test_should_get_blinker_survivors(self):
    self.assertEquals(frozenset([Grid.Cell(x=1, y=2)]), frozenset(self.grid._get_survivors()))

  def test_should_get_blinker_newborns(self):
    self.assertEquals(frozenset([Grid.Cell(x=2, y=2), Grid.Cell(x=0, y=2)]),
                      frozenset(self.grid._get_newborns()))

  def test_should_generate_new_blinker_grid_generation(self):
    new_grid = self.grid.next_generation()
    self.assertEquals(frozenset([Grid.Cell(x=0, y=2),
                                 Grid.Cell(x=1, y=2),
                                 Grid.Cell(x=2, y=2)]),
                      new_grid.live_cells)


class GolBlockTestCase(unittest.TestCase):

  def setUp(self):
    conf = [(1, 1), (1, 2), (2, 1), (2, 2)]
    self.grid = Grid(conf)

  def test_should_get_block_survivors(self):
    self.assertEquals(frozenset([Grid.Cell(x=1, y=1),
                                 Grid.Cell(x=1, y=2),
                                 Grid.Cell(x=2, y=1),
                                 Grid.Cell(x=2, y=2)]),
                      frozenset(self.grid._get_survivors()))

  def test_should_get_block_newborns(self):

    self.assertEquals(frozenset([Grid.Cell(x=1, y=1),
                                 Grid.Cell(x=1, y=2),
                                 Grid.Cell(x=2, y=1),
                                 Grid.Cell(x=2, y=2)]),
                      frozenset(self.grid._get_newborns()))

  def test_should_generate_new_block_grid_generation(self):
    self.grid.next_generation()
    self.assertEquals(frozenset([Grid.Cell(x=1, y=1),
                                 Grid.Cell(x=1, y=2),
                                 Grid.Cell(x=2, y=1),
                                 Grid.Cell(x=2, y=2)]),
                      self.grid.live_cells)


class GolGliderTestCase(unittest.TestCase):

  def setUp(self):
    conf = [(5, 4), (6, 4), (7, 4), (7, 5), (6, 6)]
    self.grid = Grid(conf)

  def test_should_get_glider_survivors(self):
    self.assertEquals(frozenset([Grid.Cell(x=7, y=4),
                                 Grid.Cell(x=6, y=4),
                                 Grid.Cell(x=7, y=5)]),
                      frozenset(self.grid._get_survivors()))

  def test_should_get_glider_newborns(self):
    self.assertEquals(frozenset([Grid.Cell(x=6, y=3),
                                 Grid.Cell(x=5, y=5),
                                 Grid.Cell(x=6, y=4),
                                 Grid.Cell(x=7, y=5)]),
                      frozenset(self.grid._get_newborns()))

  def test_should_generate_new_glider_grid_generation(self):
    new_grid = self.grid.next_generation()
    self.assertEquals(frozenset([Grid.Cell(x=7, y=4),
                                 Grid.Cell(x=6, y=4),
                                 Grid.Cell(x=7, y=5),
                                 Grid.Cell(x=5, y=5),
                                 Grid.Cell(x=6, y=3)]),
                      new_grid.live_cells)


if __name__ == "__main__":
  unittest.main()
