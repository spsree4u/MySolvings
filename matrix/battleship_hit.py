
"""
Given grid of ships. 'S' represent portion of ship. '_' represent water.
If you hit a ship, you'll get the score = size of ship.
Size or length of the ship is defined based on the adjacent 'S'.

Hit the ships to get the maximum score. You need to select the largest ships 
to get more score.

Example:
g = 
[['_', '_', '_', '_', '_', 'S'],
 ['_', '_', '_', '_', '_', 'S'],
 ['S', 'S', 'S', '_', '_', 'S'],
 ['_', '_', '_', '_', '_', '_'],
 ['_', 'S', 'S', '_', '_', '_']]

n = 2 (target ships to hit)

Function best_score(g, n) should return [(0, 5),(2, 0)]
Explanation: We have three ships in the above example. Two with size 3 and one 
with size 2. So we should return the starting index of the ships of size 3

"""


def best_score_lib(ind_list):
    print(ind_list)
    hm = {}
    hs = set()

    for i, j in ind_list:
        print(i, j, hs)
        if (i-1, j) in hs:
            hm[(i-1, j)] += 1
        elif (i, j-1) in hs:
            hm[(i, j-1)] += 1
        else:
            hm[(i, j)] = 1
        hs.add((i, j))

    return hm


def best_score(grid, target):
    ind = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                ind.append((i, j))

    hm = best_score_lib(ind)
    return hm


g = [['_', '_', '_', '_', '_', 'S'],
     ['_', '_', '_', '_', '_', 'S'],
     ['S', 'S', 'S', '_', '_', 'S'],
     ['_', '_', '_', '_', '_', '_'],
     ['_', 'S', 'S', '_', '_', '_']]

n = 2

print(best_score(g, n))
