"""
selected functions from the second practical of the "Python for Biology" course (MU4BM018)
"""

def init_grid(n=10) :
    # initialize empty n x n grid
    grid = []
    for i in range(n) : grid.append([0] * n) # new table created + appended 
    return grid

def grid_TME_start(n, glider=True, slider=True) :
    # initalize grid and add cell colonies with pre-determined configurations
    g = init_grid(n)

    if glider : g[0][1] = 1; g[1][2] = 1

    for i in range(3) :
        if glider : g[2][i] = 1
        if slider : g[10][6 + i] = 1

    return g

def display_grid(grid) :
    dim = len(grid)

    for i in range(dim) :
        for x in grid[i] :
            if x == 0 : print(".", end=" ")
            if x == 1 : print("0", end=" ")
        print()
    print()


def neighbor_coor(cell, dim, toroidal=True) :
    # get the coordinates of neighboring cells
    x, y = cell
    delta = [0, -1, 1]
    if toroidal : return sorted([((x + j) % dim, (y + i) % dim) for i in delta for j in delta 
                      if not(i == 0 and j == 0)])
        
    return sorted([(x + j, y + i) for i in delta for j in delta 
                   if (not((i == 0 and j == 0) or 
                           x + j < 0 or x + j >= dim or 
                           y + i < 0 or y + i >= dim))])

def count_neighbors(grid, cell, toroidal=True) :
    # count living neighboring cells
    coor = neighbor_coor(cell, len(grid), toroidal)
    return sum([1 for (x,y) in coor if grid[x][y] == 1])

def next_state(grid, cell) :
    # get a cell's next state 
    x, y = cell
    nb_neighbors = count_neighbors(grid, cell)

    # cell = alive
    if grid[x][y] == 1 :
        if nb_neighbors < 2 or nb_neighbors > 3 : return 0 # dies from underpopulation / overpopulation, respectively
        return 1 # otherwise, stays alive
    
    # cell = dead
    if nb_neighbors == 3 : return 1 # revives
    return 0 # stays dead

def next_generation(grid) :
    # apply next_state() to all cells in grid to get the next generation
    dim = len(grid)
    next = init_grid(dim)
    for i in range(dim) :
        for j in range(dim) :
            next[i][j] = next_state(grid,(i,j))
    return next