"""
personal continuation of the second practical of the "Python for Biology" course (MU4BM018)
"""

from math import sqrt
from GoL import *

def find_living(grid) :
    # get coordinates of all living cells
    dim = len(grid)
    return sorted([(x,y) for x in range(dim) for y in range(dim) if grid[x][y] == 1])

def distance(c1,c2) :
    # calculate distance between 2 cells
    x1, y1 = c1; x2, y2 = c2
    dX = abs(x2 - x1); dY = abs(y2 - y1)
    return round(sqrt(dX**2 + dY**2),3)

def calc_distances(coors) :
    """
    calculate distances between all coordinates
    dist_dict = {cell : [distances between other cells]}
    np_array = [distances between other cells]
    """
    dist_dict = dict()
    array = list()
    n = len(coors)

    for i in range(n) :
        aux = [distance(coors[i],coors[j]) for j in range(n)]
        dist_dict[coors[i]] = aux
        array.append(aux)
    return dist_dict, array

def group_by_distance(dist_array, threshold=3) :
    """
    returns groups of indexes (corresponding to coordinates' positions in key list)
    """
    n = len(dist_array)
    groups = list()

    for i in range(n) :
        group = list()
        
        if any(i in g for g in groups) : continue

        for j in range(i,n) :
            if 0 < dist_array[i][j] <= 3 :
                if i not in group : group.append(i)
                group.append(j)

        if len(group) == 0 : group = [dist_array[i][i]]

        groups.append(group)
    
    return groups

def convert_index_coor(groups, dist_dict) :
    # convert cell indexes to grid coordinates
    coors = list(dist_dict.keys())
    res = list()

    for g in groups :
        new = [coors[x] for x in g]
        res.append(new)
    
    return res

def group_living(grid) :
    """
    group living cells
    returns groups of grid coordinates
    """

    living_coors = find_living(grid)
    dist_dict, array = calc_distances(living_coors)
    idx_groups = group_by_distance(array)
    coor_groups = convert_index_coor(idx_groups, dist_dict)

    return coor_groups

def find_top_left(group) :
    # get the top left case coordinates in a grid configuration
    x = min([x for x,_ in group])
    y = min([y for _,y in group])
    return (x,y)

def translate_to_origin(group) :
    """
    translate the configuration so that the top left coordinates == (0,0)
    for future comparison, regardless of the configuration's position in the grid
    (simplified / "normalization")
    """
    dX, dY = find_top_left(group)
    return [(x - dX, y - dY) for x,y in group]

def configurations(grid) :
    # get all simplified configurations in a group
    coor_groups = group_living(grid)
    return [translate_to_origin(g) for g in coor_groups]

def config_to_grid(config) :
    # convert configuration to a grid for future comparison and display
    dimX = max([x for x,_ in config])
    dimY = max([y for _,y in config])

    g = list()
    for i in range(dimX + 1) : g.append([0] * (dimY + 1))
    for x,y in config : g[x][y] = 1
    
    return g

def grid_configs(grid, display=False) :
    # get all configuration grids for a grid
    configs = configurations(grid)
    return [config_to_grid(c) for c in configs]

def simulation(grid, generations, display=False) :
    # get grid history for a certain number of generations
    aux = grid.copy()
    grid_history = list()
    for i in range(generations) : 
        if display: display_grid(aux)
        grid_history.append(aux)
        aux = next_generation(aux)
    return grid_history

def identify_configs(grid_history, display=False) :
    # identify all existing configrations 
    configs = list()
    for grid in grid_history :
        for g in grid_configs(grid) :
            if g not in configs : configs.append(g)

    configs_dict = {chr(65 + i) : configs[i] for i in range(len(configs))}

    if display :
        for id, grid in configs_dict.items() :
            print(f"--- Config. {id} ---")
            display_grid(grid)
    
    return configs_dict

def get_config_id(dict, config) :
    # get configuration id
    keys = {i : list(dict.keys())[i] for i in range(len(dict))}
    configs = list(dict.values())

    for i in range(len(configs)) :
        if configs[i] == config : return keys[i]

def configs_over_gen(grid_history) :
    # get all configuration ids for each generation
    config_history = dict()
    configs_id = identify_configs(grid_history)

    for i in range(len(grid_history)) :
        grid = grid_history[i]
        configs = [get_config_id(configs_id, g) for g in grid_configs(grid)]
        config_history[i] = configs

    return config_history, configs_id            

