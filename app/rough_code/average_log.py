import re

def average_log_count(data):
	print("I'm here")
	s = 0
	c = 0
	for d in data:
		print(d[4])
		print(d[1])
		s += d[4]
		c += 1
	if s == 0:
		res = 0
	else:
		res = s/c
	return int(res)

