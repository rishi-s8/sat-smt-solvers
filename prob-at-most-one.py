#!/usr/bin/python

from z3 import *
import argparse
import itertools
import time

# number of variables
n=10

# constructed list of variables
vs = []

for i in range(n):
    temp = Bool("e_{}".format(i))
    vs.append(temp)
print(vs)

# write function that encodes that exactly one variable is one
def sum_to_one( ls ):
    # At least one
    atLeastOne = Or(ls)
    atMostOne = True
    for i,j in itertools.combinations(ls,2):
        print(i,j)
        atMostOne = And(Or(Not(i), Not(j)), atMostOne)
    exactlyOne = And(atLeastOne, atMostOne)
    return exactlyOne



# call the function
F = sum_to_one( vs )
print(F)

# construct Z3 solver
s = Solver()
# add the formula in the solver
s.add(F)
# check sat value
result = s.check()

if result == sat:
    # get satisfying model
    m = s.model()
    print("Model: ", m)
    # print only if value is true

else:
    print("unsat")
