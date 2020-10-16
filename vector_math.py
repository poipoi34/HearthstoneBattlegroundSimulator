def add(u,v):
	res = [0] * len(u)
	for i in range(len(u)):
		res[i] = u[i] + v[i]
	return res

def mul(a,v):
	return [a*vi for vi in v]

def sub(u,v):
	res = [0] * len(u)
	for i in range(len(u)):
		res[i] = u[i] - v[i]
	return res