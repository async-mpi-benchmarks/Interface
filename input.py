import re
import json
from operator import attrgetter

class Init:
	opertion_type = 'Init'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])
	def print(self):
		print(str(self.opertion_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time))


class Finalize:
	opertion_type = 'Finalize'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])
		self.rank = int(string[6])
	def print(self):
		print(str(self.opertion_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time) + ' rank: ' + str(self.rank))

class Wait:
	opertion_type = 'Wait'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.rank = int(string[8])
		self.comm = int(string[6])
		self.request = int(string[10])
	def print(self):
		print(str(self.opertion_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' rank: ' + str(self.rank) + ' req: ' +  str(self.request))

class Irecv:
	opertion_type = 'Irecv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.request = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.opertion_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))

class Recv:
	opertion_type = 'Recv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[12])
		self.dest = int(string[10])
		self.rank = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.opertion_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

class Send:
	opertion_type = 'Send'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[12])
		self.dest = int(string[10])
		self.rank = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.opertion_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

class Isend:
	opertion_type = 'Isecv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.request = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.opertion_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))

def json_reader(name):
	f = open(name)
	data = json.load(f)

	liste = []

	for elem in data:
		tmp = str(elem)
		string = re.findall(r'\w+[.]\w+|\w+', tmp)

		if  string[0] == 'Wait':
			liste.append(Wait(string))

		elif string[0] == 'Irecv':
			liste.append(Irecv(string))

		elif  string[0] == 'Recv':
			liste.append(Recv(string))

		elif  string[0] == 'Send':
			liste.append(Send(string))

		elif  string[0] == 'Isend':
			liste.append(Isend(string))
		
		elif  string[0] == 'Init':
			liste.append(Init(string))
		
		elif  string[0] == 'Finalize':
			liste.append(Finalize(string))

		else:
			print("Empty or bad format!")

	f.close()
	return liste

liste = []

liste = liste + json_reader('test.json')
liste = liste + json_reader('test2.json')

for elem in liste:
	elem.print()
	print(elem.t_before)

liste = sorted(liste,key=lambda x: x.t_before)
print()
for elem in liste:
	elem.print()
