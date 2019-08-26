#!/usr/bin/python3

#
# A 3x3 magic square contains all integers from 1 to 9.
# Sum of all rows, columns, and diagonals are same.
#

from z3 import *
import itertools

# variables for the entries of the magic square
vs = [  [Int("x_{}_{}".format(i,j))  for j in range(3)] for i in range(3)]

# create constraints
def constraints(vs):
    #   -- all entries are between 1-9
    Constraints = []
    C1 = True
    for i in vs:
        for j in i:
            C1 = And(C1, And(j>=1, j<=9))
    Constraints.append(C1)
    #   -- all entries are distinct

    C2 = Distinct(list(itertools.chain(*vs)))
    Constraints.append(C2)
    #   There is a sum value t
    t = Int('t')
    #   -- sum of rows is t
    C3 = True
    for i in vs:
        rowSum = 0
        for j in i:
            rowSum+=j
        C3 = And(C3, rowSum==t)
    Constraints.append(C3)
    #   -- sum of columns is t
    C4= True
    for i in range(0, len(vs)):
        colSum = 0
        for j in range(0, len(vs)):
            colSum+=vs[j][i]
        C4 = And(C4, colSum==t)
    Constraints.append(C4)
    #   -- sum of diagonals is t
    C5 = And(And(vs[0][0]+vs[2][2] == vs[2][0]+vs[0][2]), vs[0][0]+vs[2][2]+vs[1][1] == t)
    Constraints.append(C5)
    C = True
    for i in Constraints:
        C = And(C, i)
    return C

phi = constraints(vs)
print(phi)

s = Solver()

s.add(phi)

r = s.check()
if r == sat:
    m = s.model()
    for i in range(3):
        print( "|-----|-----|-----|" )
        for j in range(3):
            print("|  ", end ="")
            val = m[vs[i][j]]
            print( val, end ="  ")
        print("|")
    print( "|-----|-----|-----|" )
    print("sat")
else:
    print("unsat")
