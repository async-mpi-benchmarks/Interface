import re
from enum import Enum
from operator import attrgetter

class attr(Enum):
	OPERATION = 0
	BEFORE = 1
	AFTER = 2
	TAG = 3
	DEST = 4
	RANK = 5
	REQUEST = 6
	COMM = 7

class Wait:
	opertion_type = 'Wait'
	def __init__(self, string):
		self.t_before = string[attr['BEFORE'].value]
		self.t_after = string[attr['AFTER'].value]
		self.rank = string[attr['RANK'].value]
		self.request = string[attr['REQUEST'].value]

	def print(self):
		print(self.opertion_type + ' t1: ' +self.t_before + ' t2: ' +  self.t_after + ' rank: ' + self.rank + ' req: ' +  self.request)

class Irecv:
	opertion_type = 'Irecv'
	def __init__(self, string):
		self.t_before = string[attr['BEFORE'].value]
		self.t_after = string[attr['AFTER'].value]
		self.tag = string[attr['TAG'].value]
		self.dest = string[attr['DEST'].value]
		self.rank = string[attr['RANK'].value]
		self.request = string[attr['REQUEST'].value]
		self.comm = string[attr['COMM'].value]

	def print(self):
		print(self.opertion_type + ' t1: ' +self.t_before + ' t2: ' +  self.t_after + ' tag: ' + self.tag + ' dest: '+ self.dest +' rank: ' + self.rank + ' req: ' +  self.request + ' comm: ' + self.comm)

class Recv:
	opertion_type = 'Recv'
	def __init__(self, string):
		self.t_before = string[attr['BEFORE'].value]
		self.t_after = string[attr['AFTER'].value]
		self.tag = string[attr['TAG'].value]
		self.dest = string[attr['DEST'].value]
		self.rank = string[attr['RANK'].value]
		self.comm = string[attr['COMM'].value]

	def print(self):
		print(self.opertion_type + ' t1: ' +self.t_before + ' t2: ' +  self.t_after + ' tag: ' + self.tag + ' dest: '+ self.dest +' rank: ' + self.rank +  ' comm: ' + self.comm)

class Send:
	opertion_type = 'Send'
	def __init__(self, string):
		self.t_before = string[attr['BEFORE'].value]
		self.t_after = string[attr['AFTER'].value]
		self.tag = string[attr['TAG'].value]
		self.dest = string[attr['DEST'].value]
		self.rank = string[attr['RANK'].value]
		self.comm = string[attr['COMM'].value]

	def print(self):
		print(self.opertion_type + ' t1: ' +self.t_before + ' t2: ' +  self.t_after + ' tag: ' + self.tag + ' dest: '+ self.dest +' rank: ' + self.rank +  ' comm: ' + self.comm)

class Isend:
	opertion_type = 'Isecv'
	def __init__(self, string):
		self.t_before = string[attr['BEFORE'].value]
		self.t_after = string[attr['AFTER'].value]
		self.tag = string[attr['TAG'].value]
		self.dest = string[attr['DEST'].value]
		self.rank = string[attr['RANK'].value]
		self.request = string[attr['REQUEST'].value]
		self.comm = string[attr['COMM'].value]

	def print(self):
		print(self.opertion_type + ' t1: ' +self.t_before + ' t2: ' +  self.t_after + ' tag: ' + self.tag + ' dest: '+ self.dest +' rank: ' + self.rank + ' req: ' +  self.request + ' comm: ' + self.comm)

file = open('exemple.dat', 'r')
liste = []

for line in file:
	string = re.findall(r'\w+', line)
	if string[attr['OPERATION'].value] == 'Wait':
		liste.append(Wait(string))
	elif string[attr['OPERATION'].value] == 'Irecv':
		liste.append(Irecv(string))
	elif  string[attr['OPERATION'].value] == 'Recv':
		liste.append(Recv(string))
	elif  string[attr['OPERATION'].value] == 'Send':
		liste.append(Send(string))
	elif  string[attr['OPERATION'].value] == 'Isend':
		liste.append(Isend(string))
	else:
		print("Empty or bad format!")

for elem in liste:
	elem.print()

liste.sort(key = lambda v: int(v.t_before))
print()

for elem in liste:
	elem.print()