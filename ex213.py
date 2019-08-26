from z3 import *

isPositive = {}

def dfs(node,negDep):
	if node.decl().arity() == 0:
		# variable
		variableName = node.decl().name()
		if variableName not in isPositive:
			if negDep % 2 == 0:
				isPositive[variableName] = True
			else:
				isPositive[variableName] = False
		else:
			if isPositive[variableName] and negDep % 2 == 1:
				isPositive[variableName] = False
	else:
		opName = node.decl().name()
		if opName == "not":
			negDep += 1
		for child in node.children():
			dfs(child,negDep)

A = Bool("A")
B = Bool("B")
C = Bool("C")

phi = Not(And(Or(A,Not(C)),Not(Or(B,C))))

phi = Or(Not(A),A)

dfs(phi,0)

print("Positively occuring boolean variables... ")
for var in sorted(isPositive):
	if isPositive[var]:
		print(var)
