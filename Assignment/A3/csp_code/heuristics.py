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
    #IMPLEMENT
    all_vars = csp.get_all_unasgn_vars()
    min_var = all_vars[-1]
    min_domain_len = min_var.cur_domain_size()

    for var in all_vars:
        domain_len = var.cur_domain_size()
        if domain_len < min_domain_len:
            min_var = var
            min_domain_len = domain_len

    return min_var

def val_lcv(csp,var):
    #IMPLEMENT
    constraints = csp.get_cons_with_var(var)
    var_domain = var.cur_domain()
    val_to_prune = []

    for val in var_domain:
        var.assign(val)
        num_prune = 0

        for constraint in constraints:
            unassigned = constraint.get_unasgn_vars()

            for another_var in unassigned:
                another_domain = another_var.cur_domain()

                for another_val in another_domain:
                    if not constraint.has_support(another_var, another_val):
                        num_prune += 1

        var.unassign()
        val_to_prune.append((val, num_prune))
    
    sorted_list = sorted(val_to_prune, key=lambda x: x[1], reverse=False)
    result = [y[0] for y in sorted_list]

    return result