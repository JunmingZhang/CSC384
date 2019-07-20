#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    '''
    pick the next variable which has most restricted domain
    '''
    #IMPLEMENT

    # get all unassigned variables in the csp
    all_vars = csp.get_all_unasgn_vars()
    # initialize the check
    min_var = all_vars[-1]
    min_domain_len = min_var.cur_domain_size()

    # check each unassigned variable  for the csp
    for var in all_vars:
        domain_len = var.cur_domain_size()
        # pick up variable with most restriced domain
        if domain_len < min_domain_len:
            min_var = var
            min_domain_len = domain_len

    return min_var

def val_lcv(csp,var):
    '''
    return a list of value assignments for the variable which
    lead to from the most to least flexibility for following variables
    to prune values
    '''
    #IMPLEMENT

    # get all constraints with this variable and domain of the variable
    constraints = csp.get_cons_with_var(var)
    var_domain = var.cur_domain()
    # list for tuples map value in the domain and
    # number of prunes resulted in by this value
    # ie. (value, number of prunes led by this value for the following variables)
    val_to_prune = []

    # check each value in the domain
    for val in var_domain:
        # assign the value to the variable, and
        # set number of prunes to 0
        var.assign(val)
        num_prune = 0

        # check each constraint with this variable
        for constraint in constraints:
            # get all unassigned variables from this constraint
            unassigned = constraint.get_unasgn_vars()

            # get the domain of each unassigned variable
            for another_var in unassigned:
                another_domain = another_var.cur_domain()

                # check if the assignment is applicable
                # if not, increase number of prunes by 1
                for another_val in another_domain:
                    if not constraint.has_support(another_var, another_val):
                        num_prune += 1

        # unassign this variable and map the value assignment to number of prunes caused by this assignment
        var.unassign()
        val_to_prune.append((val, num_prune))
    
    # sort the value assignment by number of prunes from minimum to maximum
    sorted_list = sorted(val_to_prune, key=lambda x: x[1], reverse=False)
    result = [y[0] for y in sorted_list]

    return result