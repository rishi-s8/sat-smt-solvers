#!/usr/bin/python

from z3 import *
import argparse
import itertools
from time import time
import numpy as np
import sys

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],

[ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],

[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]

problem = problem1
# problem = problem2

# define the problem variables
# Hint: three dimentional array
vs = [[  [Bool("x_{}_{}_{}".format(i,j,k))  for k in range(9)] for j in range(9)] for i in range(9)]

def sum_to_one( ls ):
    # At least one
    atLeastOne = Or(ls)
    atMostOne = True
    for i,j in itertools.combinations(ls,2):
        atMostOne = And(Or(Not(i), Not(j)), atMostOne)
    exactlyOne = And(atLeastOne, atMostOne)
    return exactlyOne

# Accumulate constraints in the following list
Fs = []

# Encode already filled positions
for i in range(len(problem)):
    for j in range(len(problem)):
        if problem[i][j]!=0:
            for k in range(0, 9):
                if k==problem[i][j]-1:
                    Fs.append(vs[i][j][k] == True)
                else:
                    Fs.append(vs[i][j][k] == False)

# Encode for i,j  \sum_k x_i_j_k = 1
for i in vs:
    for j in i:
        Fs.append(sum_to_one(j))

# Encode for j,k  \sum_i x_i_j_k = 1
vsnp = np.array(vs)
for j in range(9):
    for k in range(9):
        Fs.append(sum_to_one(vsnp[:,j,k].tolist()))

# Encode for i,k  \sum_j x_i_j_k = 1
for i in range(9):
    for k in range(9):
        Fs.append(sum_to_one(vsnp[i,:,k].tolist()))

# Encode for i,j,k  \sum_r_s x_3i+r_3j+s_k = 1
for i in range(0,9,3):
    for j in range(0,9,3):
        for k in range(0,9,3):
            Fs.append(sum_to_one(vsnp[i:i+3, j:j+3,k].reshape(-1).tolist()))


s = Solver()
s.add( And( Fs ) )
tic = time()
if s.check() == sat:
   m = s.model()
   for i in range(9):
       if i % 3 == 0 :
           print("|-------|-------|-------|")
       for j in range(9):
           if j % 3 == 0 :
               print ("|", end =" ")
           for k in range(9):
               # FILL THE GAP
               # val model for the variables
               val = m[vs[i][j][k]]
               if is_true( val ):
                   print("{}".format(k+1), end =" ")
       print("|")
   print("|-------|-------|-------|")
else:
   print("sudoku is unsat")

print("Time: ", time()-tic)


# print vars
