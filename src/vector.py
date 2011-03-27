def add(v1, v2):
    """ Adds 2 vectors of the same size 
    v1 and v2 should be lists """
    return [v1[i] + v2[i] for i in range (len(v1))] # TODO: add size exception

def subtract(v1,v2):
    """ Adds 2 vectors of the same size
    v1 and v2 should be lists """
    return [v1[i] - v2[i] for i in range (len(v1))]
    
def unit(v1):
    """ Returns the unit vector of v1
    v1 2D a array as a list """
    dist = (v1[0] ** 2 + v1[1] ** 2) ** 0.5
    return [v1[0] / dist, v1[1] / dist] # Unit vector to return

def multiply(v1, v2):
    """ Multiplies the 2 vectors together
    v1 and v2 should be lists """
    return [v1[i] * v2[i] for i in range(len(v1))]

def scale(v1, f1):
    """ Multiplies all values in v1 by f1 """
    return [v1[i] * f1 for i in range(len(v1))]

def dot(v1, v2):
    """ Returns the dot product of v1 and v2
    v1 and v2 should be lists """
    v3 = multiply(v1,v2) # Multiply the components
    return sum(v3)  # Return the sum of the components

def absAdd(v1,v2):
    """ Adds the absolute values of v1 and v2 """
    from math import fabs
    return [fabs(v1[i]) + fabs(v2[i]) for i in range (len(v1))]