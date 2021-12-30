import re
import json
from operator import attrgetter
from tkinter import *

class Init:
	operation_type = 'Init'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])

	def print(self):
		print(str(self.operation_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,'','','','','',''))
		return table


class Finalize:
	operation_type = 'Finalize'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])
		self.rank = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time) + ' rank: ' + str(self.rank))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,'',self.rank,'','','',''))
		return table

class Wait:
	operation_type = 'Wait'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.rank = int(string[10])
		self.comm = int(string[6])
		self.request = int(string[8])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' rank: ' + str(self.rank) + ' req: ' +  str(self.request))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,self.t_after,self.rank ,'','',self.comm,self.request))
		return table

class Irecv:
	operation_type = 'Irecv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.request = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,self.t_after,self.rank ,self.dest,self.tag,self.comm,self.request))
		return table

class Recv:
	operation_type = 'Recv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[12])
		self.dest = int(string[10])
		self.rank = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,self.t_after,self.rank ,self.dest,self.tag,self.comm,''))
		return table


class Send:
	operation_type = 'Send'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[12])
		self.dest = int(string[10])
		self.rank = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,self.t_after,self.rank ,self.dest,self.tag,self.comm,''))
		return table

class Isend:
	operation_type = 'Isend'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.request = int(string[8])
		self.comm = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))
	
	def table(self,table):
		table.insert(parent='',index='end',values=(self.operation_type,self.t_before,self.t_after,self.rank ,self.dest,self.tag,self.comm,self.request))
		return table

def make_pair_isw(mpi_operation):
	pair_isw = []
	for i in range(0,len(mpi_operation)):
		for j in range(i,len(mpi_operation)):
			if ((mpi_operation[i].operation_type == 'Isend') or (mpi_operation[i].operation_type == 'Irecv')) and (mpi_operation[j].operation_type == 'Wait'):
				if(mpi_operation[i].request == mpi_operation[j].request):
					pair_isw.append(pair_isend_wait(mpi_operation[i],mpi_operation[j]))
					break

	return pair_isw

class pair_isend_wait:
	def coverage(self):
		cost_op = self.op1.t_after - self.op1.t_before + self.op2.t_after - self.op2.t_before
		cost_compu = self.op2.t_before - self.op1.t_after
		return ((cost_compu/cost_op)*100)

	def  __init__(self, op1, op2):
		if op1.t_before<op2.t_before:
			self.op1 = op1
			self.op2 = op2
		else:
			self.op1 = op2
			self.op2 = op1
		self.coverage = self.coverage()
	
	def print(self):
		self.op1.print() 
		self.op2.print()



def nb_message(liste):
	cpt = 0
	for elem in liste:
		if elem.operation_type == 'Send' or elem.operation_type == 'Isend':
			cpt = cpt + 1
	return cpt

def nb_bad_async_message(liste):
	cpt = 0
	for elem in liste:
		if elem.coverage < 100:
			cpt = cpt + 1
	return cpt

def total_asynchronisme(liste):
	compu_cost = 0
	mpi_cost = 0
	for elem in liste:
		compu_cost = compu_cost + (elem.op2.t_before - elem.op1.t_after)
		mpi_cost = mpi_cost + (elem.op1.t_after - elem.op1.t_before + elem.op2.t_after - elem.op2.t_before)
	return (compu_cost/mpi_cost)*100

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