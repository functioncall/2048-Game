# 2048 Game

## Overview
- Python implementation of the classic 2048 puzzle built for the Coursera *Principles of Computing* coursework.
- Ships with the original Codeskulptor GUI hook via `poc_2048_gui` while exposing a lightweight API for experimenting with the game logic.
- The module is written for Python 2.7 (it relies on `xrange` and print statements without parentheses).

## Requirements
- Python 2.7 interpreter.
- The `poc_2048_gui` module supplied as part of the Coursera course materials (not bundled in this repository).
- Standard library only; no third-party dependencies besides the GUI helper.

## Running the GUI
- Ensure `poc_2048_gui.py` is available on your `PYTHONPATH`.
- Execute the module directly:
  ```
  python 2048.py
  ```
- A 4×6 game board launches by default thanks to the call to `poc_2048_gui.run_gui` at the end of the file.

> **Tip:** If you intend to import the module as a library, wrap the GUI launcher in an `if __name__ == "__main__":` guard or comment it out to prevent it from running on import.

## Public API Reference

### Module-Level Constants
- `UP`, `DOWN`, `LEFT`, `RIGHT` (`int`): Direction tokens consumed by the `move` API.
- `OFFSETS` (`dict[int, tuple[int, int]]`): Maps direction tokens to row/column deltas when traversing the grid.

### Helper Functions
- `merge(line) -> list[int]`  
  Compacts a row/column toward the front, merging identical adjacent values once per move. Returns a list of the same length containing the merged sequence. The helper uses a module-level dictionary (`Dictionary`) to track whether a tile already merged in the current pass.

- `traverse_grid(start_cell, direction, num_steps) -> list[tuple[int, int]]`  
  Produces an ordered list of grid coordinates starting at `start_cell` and advancing `num_steps` steps along `direction`. Utilized internally when sweeping the board during `move`.

- `check_merge(iterator) -> int`  
  Marks entries in the internal merge-tracking dictionary. Primarily for internal use by `merge`; returns `1` when a merge may proceed, `0` otherwise.

### Class `TwentyFortyEight`
Implements the 2048 game board and move logic.

- `TwentyFortyEight(grid_height, grid_width)`  
  Constructs a board of the requested size, seeds the `initial_tiles_dict` lookup used for directional traversal, and calls `reset()`.

- `reset() -> None`  
  Clears the board to all zeros and seeds two random tiles (value 2 with 90% probability, 4 otherwise).

- `__str__() -> str`  
  Emits a simple textual representation of the board to stdout and returns an empty string (handy for quick debugging).

- `get_grid_height() -> int` / `get_grid_width() -> int`  
  Accessors for board dimensions.

- `move(direction) -> str`  
  Slides and merges tiles toward the supplied direction constant. After processing every row/column, spawns a new tile via `new_tile()`. Returns an empty string; prints snapshots of the board before and after the move for debugging.

- `get_empties() -> list[tuple[int, int]]`  
  Enumerates the coordinates of zero-valued cells, supporting the random tile placement logic.

- `new_tile() -> None`  
  Randomly selects an empty cell and assigns it a new value (2 or 4) using the 90/10 distribution.

- `set_tile(row, col, value) -> None`  
  Directly mutates a cell; useful for crafting deterministic test setups.

- `get_tile(row, col) -> int`  
  Reads the value at a specific position.

## Usage Examples

### Programmatic Board Manipulation
```python
import importlib

game_module = importlib.import_module('2048')
TwentyFortyEight = game_module.TwentyFortyEight
UP = game_module.UP
RIGHT = game_module.RIGHT

game = TwentyFortyEight(4, 4)
print("Initial board:")
game.__str__()

game.move(UP)
game.move(RIGHT)

print("Value in the top-left cell:", game.get_tile(0, 0))
```

### Integrating With the GUI
```python
import importlib
import poc_2048_gui

game_module = importlib.import_module('2048')

if __name__ == "__main__":
    poc_2048_gui.run_gui(game_module.TwentyFortyEight(4, 6))
```

## Implementation Notes
- Randomness: `new_tile` leverages `random.choice(range(9))`, granting a 90% chance to spawn a 2. Seed Python’s `random` module for repeatable test runs.
- Grid Traversal: `initial_tiles_dict` caches the "first tiles" for each direction to avoid recalculating traversal paths during every `move`.
- Merge Semantics: Because of the `Dictionary` helper, every tile can merge at most once per move, mirroring the original game's rules.
- Module Naming: Because Python identifiers cannot begin with numerals, import the module via `importlib.import_module('2048')` or rename the file locally (for example, to `game_2048.py`) when integrating it into a larger codebase.
