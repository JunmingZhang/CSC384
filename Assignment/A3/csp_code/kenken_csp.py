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
	'''
	build a csp model for kenlen grid which has only binary not-equal constraints
	'''
    ##IMPLEMENT

	# initialize a model and grid for all variables
	model = CSP("binary_ne_grid")
	grid = []
	# get the length of row/column for the kenken-grid
	grid_size = kenken_grid[0][0]
	# get the domain of assignment for each variable
	domain = list(range(1, grid_size + 1))
	# used for adding satisfying tuples for the constraint
	binary_ne_tups = []

	# iterate througn number of rows
	for row in range(grid_size):
		# initialize each row for the grid
		grid.append([])
		# iterate througn number of cols
		for col in range(grid_size):
			# initialize a variable, and add the variable to the csp model and grid
			var = Variable(str(row + 1) + str(col + 1), domain)
			model.add_var(var)
			grid[row].append(var)

			# add tuple of unequal variables to the binary-ne-tups list
			if row != col:
				binary_ne_tups.append((row + 1, col + 1))

	# iterate through each row
	for row in range(grid_size):
		# iterate through each column
		for col in range(grid_size):
			# set a gap in the row to guarantee assign a pair of variables in different cells in the grid
			for row_gap in range(row + 1, grid_size):
				# initialize a constraint and add the constraint to the csp model
				name = str(row) + str(col) + ' vs ' + str(row_gap) + str(col)
				constraint = Constraint(name, [grid[row][col], grid[row_gap][col]])
				constraint.add_satisfying_tuples(binary_ne_tups)
				model.add_constraint(constraint)

			# set a gap in the column to guarantee assign a pair of variables in different cells in the grid
			for col_gap in range(col + 1, grid_size):
				# initialize a constraint and add the constraint to the csp model
				name = str(row) + str(col) + ' vs ' + str(row) + str(col_gap)
				constraint = Constraint(name, [grid[row][col], grid[row][col_gap]])
				constraint.add_satisfying_tuples(binary_ne_tups)
				model.add_constraint(constraint)

	return model, grid

def nary_ad_grid(kenken_grid):
	'''
	build a csp model for kenlen grid which has only n-ary all-differnet constraints
	'''
    ##IMPLEMENT

	# initialize a model and grid for all variables
	model = CSP("nary_ad_grid")
	grid = []
	# get the length of row/column for the kenken-grid
	grid_size = kenken_grid[0][0]
	# get the domain of assignment for each variable
	domain = list(range(1, grid_size + 1))

	# used for adding satisfying tuples for the constraint
	# constructed by different permutations of values in the domain
	nary_ad_tups = list(itertools.permutations(domain))

	# iterate through each row
	for row in range(grid_size):
		# initialize the grid
		grid.append([])

		# iterate through each column
		for col in range(grid_size):
			# initialize a variable and add it to the model and grid
			var = Variable(str(row + 1) + str(col + 1), domain)
			model.add_var(var)
			grid[row].append(var)
	
	# iterate by times of length of the row/column of the grid
	for ind in range(grid_size):
		# initilize a constraint on the row and add it to the model
		name = "row " + str(ind)
		row_scope = grid[ind]

		constraint = Constraint(name, row_scope)
		constraint.add_satisfying_tuples(nary_ad_tups)
		model.add_constraint(constraint)

		# initilize a constraint on the column and add it to the model
		name = "col " + str(ind)
		col_scope = [row[ind] for row in grid]

		constraint = Constraint(name, col_scope)
		constraint.add_satisfying_tuples(nary_ad_tups)
		model.add_constraint(constraint)
	
	return model, grid  

def kenken_cage(cage_repr, grid):
	'''
	build a cage of variables based on the basic cage representation
	of ken-ken cage
	'''
	cage = []

	for loc in cage_repr:
		row = int(str(loc)[0]) - 1
		col = int(str(loc)[1]) - 1
		cage.append(grid[row][col])
	
	return cage

def add_check(assgns, target):
	'''
	check if the assignment satisfies the kenken cage constraint
	for addition operation
	'''
	summation = 0
	for assgn in assgns:
		summation += assgn
	return summation == target

def sub_check(assgns, target):
	'''
	check if the assignment satisfies the kenken cage constraint
	for subtraction operation
	'''

	# check all permuatations indeed of assignments, since
	# for suntraction, there is no commutative property
	# and the assignmnents satisfies the kenken constraint
	# if one permutation satisfies the kenken constraint
	all_perms = itertools.permutations(assgns)
	for perm in all_perms:
		difference = perm[0]
		for ind in range(1, len(assgns)):
			difference -= perm[ind]
		if difference == target:
			return True
	return False

def div_check(assgns, target):
	'''
	check if the assignment satisfies the kenken cage constraint
	for division operation
	'''

	# check all permuatations indeed of assignments, since
	# for division, there is no commutative property
	# and the assignmnents satisfies the kenken constraint
	# if one permutation satisfies the kenken constraint
	all_perms = itertools.permutations(assgns)
	for perm in all_perms:
		quotient = perm[0]
		for ind in range(1, len(assgns)):
			quotient //= perm[ind]
		if quotient == target:
			return True
	return False

def mul_check(assgns, target):
	'''
	check if the assignment satisfies the kenken cage constraint
	for multiplication operation
	'''
	product = 1
	for assgn in assgns:
		product *= assgn
	return product == target

def kenken_csp_model(kenken_grid):
    ##IMPLEMENT

	# initialize the model by binary_ne_grid
	model, grid = binary_ne_grid(kenken_grid)
	# model, grid = nary_ad_grid(kenken_grid) # Do not use nary_ad_grid for modelling, too slow!

	# get the length of row/column
	grid_size = kenken_grid[0][0]

	# iterate through each kenken constraint of the kenken grid
	ind = 1
	while ind < len(kenken_grid):
		# get the kenken cage, tuples for getting satisfying constraint and
		# initialize a constraint
		cage_base = kenken_grid[ind]
		kenken_csp_tups = []
		constraint = None

		# initialize kenken constraint if there are only one variable in the cage
		if len(cage_base) == 2:
			constraint = Constraint("kenken " + str(ind), [grid[int(str(cage_base[0])[0]) - 1][int(str(cage_base[0])[1]) - 1]])
			constraint.add_satisfying_tuples([[cage_base[1]]])
		
		# if there are more than one variable
		else:
			# get a formal kenken cage with variables in it
			# also the taget for the corresponding operation
			cage = kenken_cage(cage_base[:-2], grid)
			target = kenken_grid[ind][-2]
			op = kenken_grid[ind][-1]

			# get the all possible assignments with the domain
			virtual_assignments = list(itertools.product(range(grid_size), repeat=len(cage)))

			for assgns in virtual_assignments:
				# change to real assignment
				actual_assgns = [assgn + 1 for assgn in assgns]

				# check for corresponding operation for the target
				# if applicable, add the assignments for satisfying tuples
				if op == 0 and add_check(actual_assgns, target):
					kenken_csp_tups.append(actual_assgns)
				elif op == 1 and sub_check(actual_assgns, target):
					kenken_csp_tups.append(actual_assgns)
				elif op == 2 and div_check(actual_assgns, target):
					kenken_csp_tups.append(actual_assgns)
				elif op == 3 and mul_check(actual_assgns, target):
					kenken_csp_tups.append(actual_assgns)
			
			# initialize the constraint and add satisfying tuples to the constraint
			constraint = Constraint("kenken " + str(ind), cage)
			constraint.add_satisfying_tuples(kenken_csp_tups)

		# add the constraint to the model
		model.add_constraint(constraint)
		ind += 1
	
	return model, grid
