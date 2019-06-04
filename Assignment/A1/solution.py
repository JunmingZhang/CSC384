#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

#import os for time functions
from search import * #for search engines
from lunarlockout import LunarLockoutState, Direction, lockout_goal_state #for LunarLockout specific classes and problems

#LunarLockout HEURISTICS
def heur_trivial(state):
    '''trivial admissible LunarLockout heuristic'''
    '''INPUT: a LunarLockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    return 0

def heur_manhattan_distance(state):
#OPTIONAL
    '''Manhattan distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
    hval = 0
    xanadus = state.xanadus
    center = int((state.width-1)/2)

    if isinstance(xanadus[0], int):
      hval += abs(xanadus[0] - center) + abs(xanadus[1] - center)
    else:
      for xanadu in xanadus:
        hval += abs(xanadu[0] - center) + abs(xanadu[1] - center)
    return hval

def heur_L_distance(state):
    #IMPLEMENT
    '''L distance LunarLockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
    #Your function should return a sum of the L distances between each xanadu and the escape hatch.
    hval = 0
    xanadus = state.xanadus
    center = int((state.width-1)/2)

    if isinstance(xanadus[0], int):
      hval += (xanadus[0] != center) + (xanadus[1] != center)
    else:
      for xanadu in xanadus:
        hval += (xanadu[0] != center) + (xanadu[1] != center)
    return hval

def heur_alternate(state):
#IMPLEMENT
    '''a better lunar lockout heuristic'''
    '''INPUT: a lunar lockout state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
    #Your function should return a numeric value for the estimate of the distance to the goal.

    '''
    Description of the alternative heuristic:
    My alternative heuristic checks dead cases at the first. At the beginning the algorithm
    finds if there is any dead end case, for such a case the heuristic is infinity (goal not reachable).
    At first, it checks if all pieces are in one cluster. If this happens, no piece can move.
    Then it checks if there any xanadu has two extreme coordinates together.
    If one satisfies this condition, it cannot slide to any other piece to make it to the escape hatch
    since no piece can reach in the same column or row as this xanadu. After those, the algorithm will
    regulate and return a specific numeric heuristic. To make the alternative heuristic dominate the L heuristic more
    possibly, set the initial heuristic with the sum of the L heuristic and Manhattan heuristic.
    And then regulate this value by the following:
    1.	Decrease the heuristic if a xanadu is in the same row or column as the escape hatch,
    Decrease even more if there is a piece helps the xanadu to move in the escape hatch in
    One move.
    2.	If there is a robot in the escape hatch, increase the heuristic. Increase more if it cannot be moved out within one step.
    3.	If there is one robot in the neighborhood of the escape hatch, decrease the heuristic
    since once a xanadu slides to it from the opposite side, the xanadu enters the escape hatch.
    '''
    
    if isinstance(state.robots[0], int):
      temp = []
      temp.append(state.robots)
      temp = tuple(temp)
      state.robots = temp
    
    if isinstance(state.xanadus[0], int):
      temp = []
      temp.append(state.xanadus)
      temp = tuple(temp)
      state.xanadus = temp
    
    # cases for goal not reachable
    if dead_case1(state):
      return float('inf')
    if dead_case2(state):
      return float('inf')
    if dead_end(state):
      return float('inf')
  
    # estimate heuristic value by summing up heur_L_distance and heur_manhattan_distance
    hval = heur_L_distance(state) + heur_manhattan_distance(state)
    center = int((state.width-1)/2)

    # regulation from xanadus
    for xanadu in state.xanadus:
      # check if any xanadu is on the same row or column of the escape hatch
      # decrease the heuristic value more if there is a xanadu can be moved into
      # the escape hatch by one step
      if xanadu[0] == center or xanadu[1] == center:
        if neighbor_fit(state, xanadu, center):
          hval = hval ** 0.5
        else:
          hval = hval * 0.5
    
    # regulation from robots
    for robot in state.robots:
      # check if any robot is covering the escape hatch
      # increase the heuristic value more if the robot cannot
      # be moved out of the escape hatch by one step
      if robot[0] == center and robot[1] == center:
        if not move_easily(state, robot, center):
          hval = hval ** 1.3
        else:
          hval += 1
      # if there is some robot in the neighborhood of the escape hatch, decrease the heuristic value
      elif (robot[0] == center and abs(robot[1] - center) == 1) or (robot[1] == center and abs(robot[0] - center) == 1):
        hval = hval * 0.5
    return hval


def dead_case1(state):
  '''use breadth first search to check if all pieces are in one block'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: return True if all pieces are in one cluster, or return False'''

  robots = state.robots
  xanadus = state.xanadus
  pieces = list(robots) + list(xanadus)
  
  # grey is the list for pieces discovered but not explored yet
  grey = []
  block = 1
  total = len(pieces)
  
  for piece in pieces:
    up_left = (piece[0] - 1, piece[1] + 1)
    up = (piece[0], piece[1] + 1)
    up_right = (piece[0] + 1, piece[1] + 1)
    left = (piece[0] - 1, piece[1])
    right = (piece[0] + 1, piece[1])
    down_left = (piece[0] - 1, piece[1] - 1)
    down = (piece[0], piece[1] - 1)
    down_right = (piece[0] + 1, piece[1] - 1)

    # calculate number of pieces in one block by discovering surrounding pieces
    if up_left in pieces and up_left not in grey:
      grey.append(up_left)
      block += 1
    if up in pieces and up not in grey:
      grey.append(up)
      block += 1
    if up_right in pieces and up_right not in grey:
      grey.append(up_right)
      block += 1
    if left in pieces and left not in grey:
      grey.append(left)
      block += 1
    if right in pieces and right not in grey:
      grey.append(right)
      block += 1
    if down_left in pieces and down_left not in grey:
      grey.append(down_left)
      block += 1
    if down in pieces and down not in grey:
      grey.append(down)
      block += 1
    if down_right in pieces and down_right not in grey:
      grey.append(down_right)
      block += 1
    
    # remove the piece after exploring
    pieces.remove(piece)
  return block == total

def dead_case2(state):
  '''find any piece x is the highest (lowest), and y is the highest (lowest)'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: return True if there is such a piece, or return False'''

  pieces = list(state.xanadus) + list(state.robots)

  # make a list of all x and y indices
  x_list = []
  y_list = []
  for piece in pieces:
     x_list.append(piece[0])
     y_list.append(piece[1])
  
  # find the maximum and minimum in each x and y list
  x_max = max(x_list)
  y_max = max(y_list)
  x_min = min(x_list)
  y_min = min(y_list)

  # check each xanadu
  # if one xanadu posseses two extreme value for index at the same time
  # there is a dead case, and return True
  for xanadu in state.xanadus:
    if xanadu[0] == x_max and xanadu[1] == y_max:
      return True
    if xanadu[0] == x_min and xanadu[1] == y_min:
      return True
    if xanadu[0] == x_max and xanadu[1] == y_min:
      return True
    if xanadu[0] == x_min and xanadu[1] == y_max:
      return True
  return False

def dead_end(state):
  '''find if the state is dead'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: True if there is no move can be made to make the goal achievable in the last state'''

  return (len(state.successors()) == 0) and (lockout_goal_state(state) == False)

def neighbor_fit(state, xanadu, center):
  '''find if a xanadu can be easily moved into the escape hatch'''
  '''INPUT: a lunar lockout state, a xanadu and the index of the center'''
  '''OUTPUT: True if it is easy to make such a move, otherwise False'''

  pieces = list(state.xanadus) + list(state.robots)
  pieces.remove(xanadu)

  # check if there is any robot makes the xanadu move into the escape hatch immediately
  for piece in pieces:
    if (piece[1] == center) and ((piece[0] < center and center < xanadu[0]) or (xanadu[0] < center and center < piece[0])):
      if abs(piece[0] - center) == 1:
        return True
    if (piece[0] == center) and ((piece[1] < center and center < xanadu[1]) or (xanadu[1] < center and center < piece[1])):
      if abs(piece[1] - center) == 1:
        return True
  return False

def move_easily(state, robot, center):
  '''find if the robot in the center can be moved out by one move'''
  '''INPUT: a lunar lockout state, a xanadu and the index of the center'''
  '''OUTPUT: True if it is easy to make such a move, otherwise False'''

  robots = list(state.robots)
  robots.remove(robot)

  # check if the robot can be moved from the escape hatch in one step only
  for another in robots:
    if another[0] == center and robot[0] == center and abs(another[1] - robot[1]) > 1:
      return True
    if another[1] == center and robot[1] == center and abs(another[0] - robot[0]) > 1:
      return True
  return False

def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a LunarLockoutState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return float(sN.gval + weight * sN.hval)

def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound = 2):
#IMPLEMENT
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  se = SearchEngine('custom', 'full')
  wrapped_fval_function = (lambda sN: fval_function(sN, weight))
  se.init_search(initial_state, lockout_goal_state, heur_fn, wrapped_fval_function)

  search_start_time = os.times()[0]
  final = se.search(timebound, (float('inf'), float('inf'), float('inf')))

  if not final:
    return final
  
  while timing(search_start_time) < timebound:
    weight = weight ** 0.5
    if weight <= 1:
      weight = 1
    
    f_val = final.gval + heur_fn(final)
    new_final = se.search(timebound - timing(search_start_time), (float('inf'), float('inf'), f_val))

    if not new_final:
      return final
    final = new_final
  
  return final


def anytime_gbfs(initial_state, heur_fn, timebound = 2):
#OPTIONAL
  '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
  '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
  '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  se = SearchEngine('best_first', 'full')
  se.init_search(initial_state, lockout_goal_state, heur_fn)

  search_start_time = os.times()[0]
  final = se.search(timebound, (float('inf'), float('inf'), float('inf')))

  if not final:
    return final
  
  while timing(search_start_time) < timebound:
    new_final = se.search(timebound - timing(search_start_time), (final.gval, float('inf'), float('inf')))

    if not new_final:
      return final
    final = new_final
  
  return final


def timing(search_start_time):
  return os.times()[0] - search_start_time

PROBLEMS = (
  #5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((0, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((1, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((2, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2),(0,4),(2,0),(4,0)),((4, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0),(2,2),(4,2),(0,4),(4,4)),((4, 3),)),
  #7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6,3), (5,4)), ((6, 2),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2,6)), ((4, 6),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2,6), (4,6)), ((2, 0),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0 ,2), (2 ,3), (4, 4), (2, 5)), ((2, 4),(3, 1),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0 ,2), (3 ,3), (4, 4), (2, 5)), ((1, 2),(3, 0),(4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0 ,2), (1 ,2), (6, 4), (2, 5)), ((2, 0),(3, 0),(4, 0))),
  )

if __name__ == "__main__":

  #TEST CODE
  solved = 0; unsolved = []; counter = 0; percent = 0; timebound = 2; #2 second time limit for each problem
  print("*************************************")  
  print("Running A-star")     

  for i in range(len(PROBLEMS)): #note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")  
    print("PROBLEM {}".format(i))
    
    s0 = PROBLEMS[i] #Problems will get harder as i gets bigger

    print("*******RUNNING A STAR*******") 
    se = SearchEngine('astar', 'full')
    se.init_search(s0, lockout_goal_state, heur_alternate)
    final = se.search(timebound) 

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)    
    counter += 1

  if counter > 0:  
    percent = (solved/counter)*100

  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime Weighted A-star")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    weight = 4
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************") 

  solved = 0; unsolved = []; counter = 0; percent = 0; 
  print("Running Anytime GBFS")   

  for i in range(len(PROBLEMS)):
    print("*************************************")  
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  
    final = anytime_gbfs(s0, heur_alternate, timebound)

    if final:
      final.print_path()   
      solved += 1 
    else:
      unsolved.append(i)
    counter += 1      

  if counter > 0:  
    percent = (solved/counter)*100   
      
  print("*************************************")  
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))  
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))      
  print("*************************************")   



  

