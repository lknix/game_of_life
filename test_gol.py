import unittest
from gol import Grid


class GolTestCase(unittest.TestCase):

  def test_should_create_grid_object(self):
    conf = [(1, 1), (1, 2), (1, 3)]
    grid = Grid(conf)
    self.assertEquals(frozenset(conf), grid.live_cells)

  def test_should_get_live_and_neighoring_cells(self):
    conf = [(1, 1)]
    grid = Grid(conf)
    self.assertEquals(set([Grid.Cell(x=1, y=2),
                           Grid.Cell(x=0, y=1),
                           Grid.Cell(x=0, y=0),
                           Grid.Cell(x=2, y=1),
                           Grid.Cell(x=0, y=2),
                           Grid.Cell(x=2, y=0),
                           Grid.Cell(x=2, y=2),
                           Grid.Cell(x=1, y=0),
                           Grid.Cell(x=1, y=1)]),
                      set(grid._get_live_and_neighboring_cells(Grid.Cell(1, 1))))

  def test_should_validate_newborn_cell(self):
    conf = [(1, 1), (1, 0), (3, 0)]
    grid = Grid(conf)
    self.assertTrue(grid._is_newborn(Grid.Cell(2, 0), conf))

  def test_should_invalidate_newborn_if_reproduction_conditions_not_met(self):
    conf = [(1, 1), (1, 0)]
    grid = Grid(conf)
    self.assertFalse(grid._is_newborn(Grid.Cell(2, 0), conf))

  def test_should_validate_survivor_cell_with_two_neighbors(self):
    conf = [(1, 1), (1, 0), (2, 0)]
    grid = Grid(conf)
    self.assertTrue(grid._is_survivor(Grid.Cell(1, 0), conf))

  def test_should_validate_survivor_cell_with_three_neighbors(self):
    conf = [(1, 1), (1, 0), (2, 0), (1, -1)]
    grid = Grid(conf)
    self.assertTrue(grid._is_survivor(Grid.Cell(1, 0), conf))

  def test_should_mark_cell_dead_due_to_overpopulation(self):
    conf = [(1, 1), (1, 0), (2, 0), (1, -1), (0, 0)]
    grid = Grid(conf)
    self.assertFalse(grid._is_survivor(Grid.Cell(1, 0), conf))

  def test_should_mark_cell_dead_due_to_extinction(self):
    conf = [(1, 1), (2, 0)]
    grid = Grid(conf)
    self.assertFalse(grid._is_survivor(Grid.Cell(1, 0), conf))

  def test_should_get_next_generation(self):
    conf = [(1, 1), (1, 0), (2, 0)]
    grid = Grid(conf)
    self.assertLess(0, len(grid.next_generation().live_cells))

  def test_should_stop_if_generation_dies_out(self):
    conf = [(1, 1), (2, 0)]
    grid = Grid(conf)
    self.assertEquals(0, len(grid.next_generation().live_cells))


class GolBlinkerTestCase(unittest.TestCase):

  def setUp(self):
    self.conf = [(1, 1), (1, 2), (1, 3)]
    self.grid = Grid(self.conf)

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
