# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 3 
# Author: Joseph Ko
# Unification algorithm from AIMA textbook
# -------------------------------------------------------

def unify(x, y, theta): 
    """
    Input: 
    x = variable, constant, or list of parameters 
    y = variable, constant, or list of parameters 
    theta = substitutions as dictionary
    Note: assumed there are no compound expressions, 
    i.e., occur check is not implemented
    output: 
    returns theta = dict of substitutions {var:x}
    or False if cannot be unified 
    """
    if theta == False:
        return False
    elif x == y:
        return theta
    elif isinstance(x, str) and x[0].islower(): # if x is a variable
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y[0].islower(): # if y is a variable
        return unify_var(y, x, theta)
    elif isinstance(x, list) and isinstance(y, list): # both x and y are lists
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return False

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta

# # testing 
# x = ["John", "x"]
# y = ["y", "z"]
# theta = unify(x, y, {})
# print(theta)