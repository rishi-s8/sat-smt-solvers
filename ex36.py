import sys
from random import randint

file = open("edges.txt", 'w')

n = int(sys.argv[1])
m = int(sys.argv[2])
for x in range(m):
    a = randint(0,n-1)
    b = randint(0,n-1)
    if b==a:
        b = (b+1)%n
    file.write(str(a) + "," + str(b) + "\n")
file.close()
