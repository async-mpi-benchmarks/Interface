import re
import json
from operator import attrgetter
from tkinter import *

class Init:
	operation_type = 'Init'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])
		self.rank = ''

	def print(self):
		print(str(self.operation_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,'','','','','','',''))
		return table

class Finalize:
	operation_type = 'Finalize'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.time = float(string[4])
		self.rank = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t: ' + str(self.t_before) + ' real time: ' + str(self.time) + ' rank: ' + str(self.rank))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,'','',self.rank,'','','',''))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')

class Wait:
	operation_type = 'Wait'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.rank = int(string[8])
		self.request = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + ' rank: ' + str(self.rank) + ' req: ' +  str(self.request))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,(self.t_after-deb)/ratio,'',self.rank ,'','','',self.request))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
		x0 = offset + (self.t_before - deb)/ratio
		x1 = offset + (self.t_after - deb)/ratio
		y0 = y1 + 15
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
		canvas.create_text(x0+ 3,y0+ 3,text = str(self.operation_type) + "\n" +  "request " + str(self.request),anchor = NW)

class Irecv:
	operation_type = 'Irecv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[16])
		self.dest = int(string[14])
		self.rank = int(string[12])
		self.request = int(string[10])
		self.comm = int(string[8])
		self.nb_bytes = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + " bytes: " + str(self.nb_bytes) +' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,(self.t_after-deb)/ratio,self.nb_bytes,self.rank ,self.dest,self.tag,self.comm,self.request))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
		x0 = offset + (self.t_before - deb)/ratio
		x1 = offset + (self.t_after - deb)/ratio
		y0 = y1 + 15
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
		canvas.create_text(x0 + 3 ,y0 + 3,text = str(self.operation_type) + "\n" + str(self.nb_bytes) + " bytes receiv from " + str(self.dest) + "\n" + "with tag " + str(self.tag) + " on comm " + str(self.comm) + "\n with request " + str(self.request),anchor = NW)

class Recv:
	operation_type = 'Recv'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.comm = int(string[8])
		self.nb_bytes = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' +str(self.t_before) + ' t2: ' +  str(self.t_after) + " bytes: " + str(self.nb_bytes) +' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,(self.t_after-deb)/ratio,self.nb_bytes ,self.rank ,self.dest,self.tag,self.comm,''))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
		x0 = offset + (self.t_before - deb)/ratio
		x1 = offset + (self.t_after - deb)/ratio
		y0 = y1 + 15
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
		canvas.create_text(x0 + 3,y0 + 3,text = str(self.operation_type) +  "\n" + str(self.nb_bytes) + " bytes receiv from " + str(self.dest) + "\n" + "with tag " + str(self.tag) + " on comm " + str(self.comm),anchor = NW)


class Send:
	operation_type = 'Send'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[14])
		self.dest = int(string[12])
		self.rank = int(string[10])
		self.comm = int(string[8])
		self.nb_bytes = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + " bytes: " + str(self.nb_bytes) +' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) +  ' comm: ' + str(self.comm))

	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,(self.t_after-deb)/ratio,self.nb_bytes ,self.rank ,self.dest,self.tag,self.comm,''))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
		x0 = offset + (self.t_before - deb)/ratio
		x1 = offset + (self.t_after - deb)/ratio
		y0 = y1 + 15
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
		canvas.create_text(x0+ 3,y0+ 3,text = str(self.operation_type) +  "\n" + str(self.nb_bytes) + " bytes sent to " + str(self.dest) + "\n" + "with tag " + str(self.tag) + " on comm " + str(self.comm),anchor = NW)

class Isend:
	operation_type = 'Isend'
	def __init__(self, string):
		self.t_before = int(string[2])
		self.t_after = int(string[4])
		self.tag = int(string[16])
		self.dest = int(string[14])
		self.rank = int(string[12])
		self.request = int(string[10])
		self.comm = int(string[8])
		self.nb_bytes = int(string[6])
	def print(self):
		print(str(self.operation_type) + ' t1: ' + str(self.t_before) + ' t2: ' +  str(self.t_after) + " bytes: " + str(self.nb_bytes) +' tag: ' + str(self.tag) + ' dest: '+ str(self.dest) +' rank: ' + str(self.rank) + ' req: ' +  str(self.request) + ' comm: ' + str(self.comm))
	
	def table(self,table,deb,ratio):
		table.insert(parent='',index='end',values=(self.operation_type,(self.t_before-deb)/ratio,(self.t_after-deb)/ratio,self.nb_bytes ,self.rank ,self.dest,self.tag,self.comm,self.request))
		return table

	def draw_timeline(self,deb,canvas,last_op,offset,voffset,ratio):
		x0 = offset + (last_op[self.rank] - deb)/ratio
		y0 = self.rank*150 + voffset
		x1 = offset + (self.t_before - deb)/ratio
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'grey')
		x0 = offset + (self.t_before - deb)/ratio
		x1 = offset + (self.t_after - deb)/ratio
		y0 = y1 + 15
		y1 = y0 + 50
		canvas.create_rectangle(x0, y0, x1, y1, fill = 'blue')
		canvas.create_text(x0+ 3,y0+ 3,text = str(self.operation_type) +  "\n" + str(self.nb_bytes) + " bytes sent to " + str(self.dest) + "\n" + "with tag " + str(self.tag) + " on comm " + str(self.comm) + "\nwith request " + str(self.request),anchor = NW)

def make_pair_isw(mpi_operation):
	pair_isw = []
	for i in range(0,len(mpi_operation)):
		for j in range(i,len(mpi_operation)):
			if ((mpi_operation[i].operation_type == 'Isend') or (mpi_operation[i].operation_type == 'Irecv')) and (mpi_operation[j].operation_type == 'Wait'):
				if(mpi_operation[i].request == mpi_operation[j].request ) and (mpi_operation[i].rank == mpi_operation[j].rank ):
					pair_isw.append(pair_isend_wait(mpi_operation[i],mpi_operation[j]))
					break

	return pair_isw

class pair_isend_wait:
	def coverage(self):
		cost_op = self.op1.t_after - self.op1.t_before + self.op2.t_after - self.op2.t_before
		cost_compu = self.op2.t_before - self.op1.t_after
		return (cost_compu/cost_op)*100

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

class pair_send_receiv:

	def  __init__(self, op1, op2):
		self.send = op1
		self.receiv = op2
		self.time = self.receiv.t_after - self.send.t_before
		self.debit = self.send.nb_bytes / self.time

	def print(self):
		self.send.print() 
		self.receiv.print()
		print("Debit: " + str(self.debit))
		print("Time: " + str(self.time))

def make_pair_sr(mpi_operation):
	pair_sr = []
	for i in range(0,len(mpi_operation)):
		for j in range(i,len(mpi_operation)):
			if ((mpi_operation[i].operation_type == 'Isend') or (mpi_operation[i].operation_type == 'Send')) and ((mpi_operation[j].operation_type == 'Recv') or (mpi_operation[j].operation_type == 'Irecv')):
				if (mpi_operation[i].tag == mpi_operation[j].tag) and (mpi_operation[i].dest == mpi_operation[j].rank) and (mpi_operation[i].rank == mpi_operation[j].dest) and (mpi_operation[i].comm == mpi_operation[j].comm) and (mpi_operation[i].nb_bytes == mpi_operation[j].nb_bytes):
					print("i:" + str(i) + " j:"+str(j))
					pair_sr.append(pair_send_receiv(mpi_operation[i],mpi_operation[j]))
					break
	return pair_sr

def nb_rank(liste):
	max_ = 0
	for elem in liste:
		if elem.rank != '':
			max_ = max(max_,elem.rank)
	return max_ + 1

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
	if len(liste):
		return cpt
	else:
		return "No Async"

def total_asynchronisme(liste):
	compu_cost = 0
	mpi_cost = 0
	for elem in liste:
		compu_cost = compu_cost + (elem.op2.t_before - elem.op1.t_after)
		mpi_cost = mpi_cost + (elem.op1.t_after - elem.op1.t_before + elem.op2.t_after - elem.op2.t_before)
	if len(liste):
		return (compu_cost/mpi_cost)*100
	else:
		return 0

def ratio_cycle2sec(liste):
	if liste[0].operation_type != 'Init':
		print("Error the first MPI operation is not an Init")
	if liste[len(liste)-1].operation_type != 'Finalize':
		print("Error the last MPI operation is not a Finalize")

	delta_rdtsc = liste[len(liste)-1].t_before - liste[0].t_before
	delta_time = liste[len(liste)-1].time - liste[0].time
	return delta_rdtsc/delta_time


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
