#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools

def binary_ne_grid(kenken_grid):
    ##IMPLEMENT
	model = CSP("binary_ne_grid")
	grid = []
	grid_size = kenken_grid[0][0]
	domain = list(range(1, grid_size + 1))
	binary_ne_tups = []

	for row in range(grid_size):
		grid.append([])
		for col in range(grid_size):
			var = Variable(str(row + 1) + str(col + 1), domain)
			model.add_var(var)
			grid[row].append(var)

			if row != col:
				binary_ne_tups.append((row + 1, col + 1))

	for row in range(grid_size):
		for col in range(grid_size):
			for row_gap in range(row + 1, grid_size):
				name = str(row) + str(col) + ' vs ' + str(row_gap) + str(col)
				constraint = Constraint(name, [grid[row][col], grid[row_gap][col]])
				constraint.add_satisfying_tuples(binary_ne_tups)
				model.add_constraint(constraint)

			for col_gap in range(col + 1, grid_size):
				name = str(row) + str(col) + ' vs ' + str(row) + str(col_gap)
				constraint = Constraint(name, [grid[row][col], grid[row][col_gap]])
				constraint.add_satisfying_tuples(binary_ne_tups)
				model.add_constraint(constraint)

	return model, grid

def nary_ad_grid(kenken_grid):
    ##IMPLEMENT
	model = CSP("nary_ad_grid")
	grid = []
	grid_size = kenken_grid[0][0]
	domain = list(range(1, grid_size + 1))

	nary_ad_tups = list(itertools.permutations(domain))

	for row in range(grid_size):
		grid.append([])
		for col in range(grid_size):
			var = Variable(str(row + 1) + str(col + 1), domain)
			model.add_var(var)
			grid[row].append(var)
	
	for ind in range(grid_size):
		name = "row " + str(ind)
		row_scope = grid[ind]

		constraint = Constraint(name, row_scope)
		constraint.add_satisfying_tuples(nary_ad_grid)
		model.add_constraint(constraint)

		name = "col " + str(ind)
		col_scope = [row[ind] for row in grid]

		constraint = Constraint(name, col_scope)
		constraint.add_satisfying_tuples(nary_ad_grid)
		model.add_constraint(constraint)
	
	return model, grid

    

def kenken_csp_model(kenken_grid):
    ##IMPLEMENT
