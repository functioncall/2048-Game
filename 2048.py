"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

Dictionary = {}
def check_merge(iterator):
    """
    Check whether the merge has happen at a particular
    index or not, and returns the appropriate boolean value
    for the same.
    """
    if Dictionary[iterator] == 0:
        Dictionary[iterator] = 1
        for item in xrange(iterator+1):
            Dictionary[item] = 1
        return 1
    else:
        return 0
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # Start with a result list that contains the same number of 0's as the length of the line argument. 
    result = [0]*len(line)
    # Initialize the dictionary with default value 0
    for index in xrange(len(line)):
        Dictionary[index] = 0
    
    # Iterate over every value in the list
    for index,item in enumerate(line):
        # Iterate over the line input looking for non-zero entries
        if item != 0:
            # Put the first index element directly in the result list
            if index == 0:
                result[index] = item
                # For the rest of the elements, iterate towards the front of the list and start merging
            else:
                set_flag = 0
                for iterator in xrange(index,0,-1):
                    # For 0 elements
                    if result[iterator-1] == 0:
                        result[iterator-1] = item
                        result[iterator] = 0
                        set_flag=1
                    # For elements which are same and merge can be applied
                    elif result[iterator-1] == item and check_merge(iterator-1):
                        result[iterator-1] = item + item
                        result[iterator] = 0
                        break
                    elif result[iterator-1] != item and set_flag == 1:
                        break
                    elif result[iterator-1] != item and set_flag == 0:
                        result[index] = item
                        break

    return result

def traverse_grid(start_cell, direction, num_steps):
    """
    This function iterates through the cells in grid in linear fashion
    """
    result = []
    for step in range(num_steps):
        row = start_cell[0] + step*direction[0]
        col = start_cell[1] + step*direction[1]
        result.append((row,col))
    return result

initial_tiles_dict = {}

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
                
        # initial_indices_up
        initial_indices_up = traverse_grid((0,0),(0,1),self._width)
        initial_tiles_dict[1] = initial_indices_up

        # initial_indices_down
        initial_indices_down = traverse_grid((self._height-1,0),(0,1),self._width)
        initial_tiles_dict[2] = initial_indices_down

        # initial_indices_left
        initial_indices_left = traverse_grid((0,0),(1,0),self._height)
        initial_tiles_dict[3] = initial_indices_left

        # initial_indices_right
        initial_indices_right = traverse_grid((0,self._width-1),(1,0),self._height)
        initial_tiles_dict[4] = initial_indices_right
        
        self.reset()

        #self.__str__()
        pass

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # create a grid of height×width zeros
        self._board = [[0 for dummy_col in xrange(self._width)]
                      for dummy_row in xrange(self._height)]
        self.new_tile()
        self.new_tile()
        # Before move
        # print self.__str__()
        # self.move(RIGHT)
        # After move
        # print self.__str__()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        for cells in self._board:
            print cells
        return ""
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        old_board = [x[:] for x in self._board]
        print old_board
        
        #print self.__str__()
        initial_tiles = initial_tiles_dict[direction]
        
        for indices in initial_tiles:
            if direction == 1 or direction == 2:
                # this list contains the indices of initial tiles for the up or down direction
                before_merge_list = traverse_grid(indices,OFFSETS[direction],self.get_grid_height())
  
            elif direction == 3 or direction == 4:
                # this list contains the indices of initial tiles for the up or down direction
                before_merge_list = traverse_grid(indices,OFFSETS[direction],self.get_grid_width())
            # before_merge list would contain the value for each of the column list for 
            # each initial tile before merge is called   
            before_merge = []
            for item in before_merge_list:
                before_merge.append(self._board[item[0]][item[1]])
            # after_merge list would contain the value for each of the column list for 
            # each initial tile after merge is called
            after_merge = merge(before_merge)
            # this will set the values of the cell after getting the new tile values
            for i,indexes in enumerate(before_merge_list):
                self.set_tile(indexes[0], indexes[1], after_merge[i])
        print old_board
        print 
        print self._board
        self.new_tile()
        return ""

    def get_empties(self):
        """
        Return the row and col indices of the cells whose values are empty
        """
        return [(r,c) for r,row in enumerate(self._board) \
                for c,col in enumerate(row) if col == 0]
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # Create a local variable random_num
        random_num = random.choice(range(9))
        
        if random_num != 8:
            new_tile = 2
        else:
            new_tile = 4
        # Get all the empty tiles as (row,col) indices and pick one at random
        empties = self.get_empties()
        # Separating row and col in different variable
        row,col = random.choice(empties)
        self.set_tile(row, col, new_tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._board[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._board[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 6))
TwentyFortyEight(4, 6)