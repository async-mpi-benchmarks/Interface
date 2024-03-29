import re
import json
from operator import attrgetter
from tkinter import *
import threading

MPI_SEND_OP = ['MpiIsend' , 'MpiSend']
MPI_RECV_OP = ['MpiRecv' , 'MpiIrecv']
MPI_WAIT_OP = ['MpiWait']
MPI_ASYNC_OP = ['MpiIsend' , 'MpiIrecv', 'MpiIbarrier','MpiIbcast','MpiIreduce','MpiIgather','MpiIscatter']
MPI_SYNC_OP = ['MpiSend' , 'MpiRecv', 'MpiBarrier']
MPI_INIT_OP = ['MpiInit' , 'MpiInitThread']
MPI_BARRIER_OP = ['MpiBarrier' , 'MpiIbarrier']
MPI_COLL_OP = ['MpiIbcast','MpiIreduce','MpiIgather','MpiIscatter','MpiBcast','MpiReduce','MpiGather','MpiScatter']
MPI_ASYNC_COLL_OP = ['MpiIbcast','MpiIreduce','MpiIgather','MpiIscatter']
MPI_SYNC_COLL_OP = ['MpiBcast','MpiReduce','MpiGather','MpiScatter']
#OPERATION_REDUCE=['MPI_OP_NUL','MPI_MAX','MPI_MIN','MPI_SUM','MPI_PROD','MPI_LAND','MPI_BAND','MPI_LOR','MPI_BOR','MPI_LXOR','MPI_BXOR','MPI_MAXLOC','MPI_MINLOC','MPI_REPLACE']

def tsc_after(elem):
    return elem["tsc"]+elem["duration"]

def draw_timeline_text(canvas,elem,x,y):
    if(elem["type"]=="MpiWait"):
        canvas.create_text(x, y,
                           text=str(elem["type"]) + "\n" + "req: " +
                           str(elem["req"]),
                           anchor=NW)
    elif(elem["type"]=="MpiIrecv"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           " partner: " + str(elem["partner_rank"]) + "\n" +
                           "tag: " + str(elem["tag"]) + " comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)
    elif(elem["type"]=="MpiRecv"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           " partner: " + str(elem["partner_rank"]) + "\n" +
                           "tag: " + str(elem["tag"]) + " comm: " +
                           str(elem["comm"]), anchor=NW)
    elif(elem["type"]=="MpiSend"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           " partner: " + str(elem["partner_rank"]) + "\n" +
                           "tag: " + str(elem["tag"]) + " comm: " +
                           str(elem["comm"]), anchor=NW)
    elif(elem["type"]=="MpiIsend"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           " partner: " + str(elem["partner_rank"]) + "\n" +
                           "tag: " + str(elem["tag"]) + " comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)
    elif(elem["type"]=="MpiBarrier"):
        canvas.create_text(x,y,
                           text=str(elem["type"])+ "\n" +" comm: " +
                           str(elem["comm"]), anchor=NW)
    elif(elem["type"]=="MpiIbarrier"):
        canvas.create_text(x,y,
                           text=str(elem["type"])+ "\n" +" comm: " +
                           str(elem["comm"])+"\n req: " +
                           str(elem["req"]), anchor=NW)

    elif(elem["type"]=="MpiIbcast"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           " root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)

    elif(elem["type"]=="MpiBcast"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +
                           "\nroot: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]),
                           anchor=NW)

    elif(elem["type"]=="MpiIgather"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\nnb_bytes_send: " + str(elem["nb_bytes_send"]) +
                           "\nnb_bytes_recv: " + str(elem["nb_bytes_recv"]) +
                           "\nroot: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)

    elif(elem["type"]=="MpiGather"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes_send: " + str(elem["nb_bytes_send"]) + "\n nb_bytes_recv: " + str(elem["nb_bytes_recv"]) +
                           " root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]),
                           anchor=NW)

    elif(elem["type"]=="MpiIscatter"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes_send: " + str(elem["nb_bytes_send"]) + "\n nb_bytes_recv: " + str(elem["nb_bytes_recv"]) +
                           " root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)

    elif(elem["type"]=="MpiIscatter"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes_send: " + str(elem["nb_bytes_send"]) + "\n nb_bytes_recv: " + str(elem["nb_bytes_recv"]) +
                           " root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]) + "\n req: " +
                           str(elem["req"]),
                           anchor=NW)

    elif(elem["type"]=="MpiReduce"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +'\nOp: '+ str(elem["op_type"])+
                           "\n root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"]),
                           anchor=NW)
    elif(elem["type"]=="MpiIreduce"):
        canvas.create_text(x,y,
                           text=str(elem["type"]) + "\n nb_bytes: " + str(elem["nb_bytes"]) +'\nOp: '+ str(elem["op_type"])+
                           "\n root: " + str(elem["partner_rank"]) + "\n" +" comm: " +
                           str(elem["comm"])+"\n req: " +
                           str(elem["req"]),
                           anchor=NW)
        

def draw_timeline(elem,deb,canvas,last_op,offset,voffset,ratio):
    x0 = offset + (last_op[elem["current_rank"]] - deb) / float(ratio)
    y0 = elem["current_rank"] * 150 + voffset
    x1 = offset + (elem["tsc"] - deb) / float(ratio)
    y1 = y0 + 50
    canvas.create_rectangle(x0, y0, x1, y1, fill='grey')
    if(elem["type"] not in MPI_INIT_OP and elem["type"] != "MpiFinalize"):
        if(elem["type"] in MPI_SEND_OP or elem["type"] in MPI_RECV_OP):
            color = "blue"
        if(elem["type"] in MPI_WAIT_OP):
            color = "dark red"
        if(elem["type"] in MPI_BARRIER_OP):
            color = "red"
        if(elem["type"] in MPI_COLL_OP):
            color = "green"
        x0 = offset + (elem["tsc"] - deb) / float(ratio)
        x1 = offset + (tsc_after(elem) - deb) / float(ratio)
        y0 = y1 + 15
        y1 = y0 + 50
        canvas.create_rectangle(x0, y0, x1, y1, fill=color)
        draw_timeline_text(canvas,elem,x0+3,y0+3)

def draw_table(elem,table, deb, ratio):
    if(elem["type"] in "MpiInit"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio), '', '',
                             elem["current_rank"], '', '', '', '','','','','','',''))
    elif(elem["type"] in "MpiInitThread"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio), '', '',
                             elem["current_rank"], '', '', '', '','','','','',elem['required_thread_lvl'],elem['proviwwwwwded_thread_lvl']))
    elif(elem["type"]=="MpiFinalize"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio), '', '',
                             elem["current_rank"], '', '', '', '','','','','','',''))
    elif(elem["type"]=="MpiWait"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), '', elem["current_rank"], '', '',
                             '', elem["req"],'','','','','',''))
    elif(elem["type"]=="MpiIrecv" or elem["type"]=="MpiIsend"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], elem["partner_rank"], elem["tag"], elem["comm"],
                             elem["req"],'','','','','',''))
    elif(elem["type"]=="MpiRecv" or elem["type"]=="MpiSend"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], elem["partner_rank"], elem["tag"], elem["comm"],'','','','','','',''))
    elif(elem["type"]=="MpiBarrier"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio),'',
                             elem["current_rank"],'','', elem["comm"],'','','','','','',''))

    elif(elem["type"]=="MpiIbarrier"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio),'',
                             elem["current_rank"],'','', elem["comm"],elem["req"],'','','','','',''))

    elif(elem["type"]=="MpiIbcast" or elem["type"]=="MpiIgather" or elem["type"]=="MpiIscatter"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), '',
                             elem["current_rank"], '','', elem["comm"],
                             elem["req"],elem["partner_rank"],'','','','',''))

    elif(elem["type"]=="MpiBcast" or elem["type"]=="MpiGather" or elem["type"]=="MpiScatter"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), '',
                             elem["current_rank"], '','', elem["comm"],
                             '',elem["partner_rank"],'','','','',''))

    elif(elem["type"]=="MpiIscatter"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], '','', elem["comm"],
                             elem["req"],elem["Root"],'',elem["nb_bytes_send"],elem["nb_bytes_recv"],'',''))

    elif(elem["type"]=="MpiScatter"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], '','', elem["comm"],
                             '',elem["partner_rank"],'',elem["nb_bytes_send"],elem["nb_bytes_recv"],'',''))
    elif(elem["type"]=="MpiIreduce"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], '','', elem["comm"],
                             elem["req"],elem["partner_rank"],elem["op_type"],'','','',''))
    elif(elem["type"]=="MpiReduce"):
        table.insert(parent='',
                     index='end',
                     values=(elem["type"], "%.8f" % ((elem["tsc"] - deb) / ratio),
                             "%.6e" % (elem["duration"] / ratio), elem["nb_bytes"],
                             elem["current_rank"], '','', elem["comm"],
                             '',elem["partner_rank"],elem["op_type"],'','','',''))

    return table

def make_pair_isw(mpi_operation):
    pair_isw = []
    for i in range(0, len(mpi_operation)):
        for j in range(i, len(mpi_operation)):
            if (((mpi_operation[i]["type"] in MPI_ASYNC_OP) and (mpi_operation[j]["type"] in MPI_WAIT_OP))):
                if (mpi_operation[i]["req"] == mpi_operation[j]["req"]) and (mpi_operation[i]["current_rank"] == mpi_operation[j]["current_rank"]):

                    pair_isw.append(pair_async_wait(mpi_operation[i], mpi_operation[j]))
                    break

    return pair_isw


class pair_async_wait:

    def coverage(self):
        cost_op = self.op1["duration"] + self.op2["duration"]
        cost_compu = self.op2["tsc"] - tsc_after(self.op1)
        cov = (cost_compu/cost_op) * 100
        if(cov < 100):
            return cov
        else:
            return 100 

    def __init__(self, op1, op2):
        if op1["tsc"] < op2["tsc"]:
            self.op1 = op1
            self.op2 = op2
        else:
            self.op1 = op2
            self.op2 = op1
        self.coverage = self.coverage()

    def print(self):
        print(self.op1)
        print(self.op2)
        print("coverage: " + str(self.coverage))


class pair_send_receiv:

    def __init__(self, op1, op2, ratio):
        self.send = op1
        self.receiv = op2
        self.time = abs(tsc_after(self.receiv) - self.send["tsc"]) / ratio
        self.debit = float(self.send["nb_bytes"]) / float(self.time)
    
    def print(self):
        print(self.send)
        print(self.receiv)
        print("Nb bytes: " + str(self.send["nb_bytes"]))
        print("Time: " + str(self.time))
        print("Debit: " + str(self.debit))
        


def make_pair_sr(mpi_operation, ratio):
    pair_sr = []
    marked_index = []
    for op1 in mpi_operation:
        index_op1 = mpi_operation.index(op1)
        
        if((op1["type"] in MPI_INIT_OP) or op1["type"]=="MpiFinalize"):
            continue
        if(index_op1 in marked_index):
            continue
        
        for op2 in mpi_operation[index_op1:]:
            index_op2 = mpi_operation.index(op2)
            
            if((op2["type"] in MPI_INIT_OP) or op1["type"]=="MpiFinalize"):
                continue
            if(index_op2 in marked_index):
                continue
            
            if ((op1["type"] in MPI_SEND_OP) and (op2["type"] in MPI_RECV_OP)):
                if ((op1["tag"] == op2["tag"]) and (op1["partner_rank"] == op2["current_rank"]) and (op1["current_rank"] == op2["partner_rank"]) and (op1["comm"] == op2["comm"])):
                    pair_sr.append(pair_send_receiv(op1, op2, ratio))
                    marked_index.append(index_op1)
                    marked_index.append(index_op2)
                    break
            if ((op2["type"] in MPI_SEND_OP)) and ((op1["type"] in MPI_RECV_OP)):
                if ((op2["tag"] == op1["tag"]) and (op2["partner_rank"] == op1["current_rank"]) and (op2["current_rank"] == op1["partner_rank"]) and (op2["comm"] == op1["comm"])):
                    pair_sr.append(pair_send_receiv(op2, op1, ratio))
                    marked_index.append(index_op1)
                    marked_index.append(index_op2)
                    break
    return pair_sr


def gather_info(liste_mpi_op, liste_isw):
    info = [0] * 4
    max_rank = 0
    nb_message = 0
    for elem in liste_mpi_op:
        max_rank = max(max_rank, elem["current_rank"])
        if elem["type"] in MPI_SEND_OP:
            nb_message = nb_message + 1

    info[0] = max_rank + 1
    info[1] = nb_message

    nb_bad_async = 0
    cov = 0
    cpt = 0
    for elem in liste_isw:
        if elem.coverage < 100:
            nb_bad_async = nb_bad_async + 1
        cov = cov + elem.coverage
        cpt = cpt + 1

    if len(liste_isw):
        info[2] = nb_bad_async
        info[3] = cov/cpt
    else:
        info[2] = "No Async"
        info[3] = 0
    return info

def gather_process_info(liste_mpi_op,nb_rank):
    process_info = [{} for i in range(0,nb_rank)]

    for i in range(0,nb_rank):
        process_info[i]["nb_message_sent"] = 0
        process_info[i]["nb_message_recv"] = 0
        process_info[i]["nb_barrier"] = 0
        process_info[i]["nb_async_op"] = 0
        process_info[i]["nb_sync_op"] = 0
        process_info[i]["list_partner"] = []
        process_info[i]["nb_partner"] = 0

    for elem in liste_mpi_op:
        
        erank = elem["current_rank"]
        
        if(elem["type"] in MPI_SEND_OP):
            process_info[erank]["nb_message_sent"] = process_info[erank]["nb_message_sent"] + 1
        
        if(elem["type"] in MPI_RECV_OP):
            process_info[erank]["nb_message_recv"] = process_info[erank]["nb_message_recv"] + 1
        
        if(elem["type"] in MPI_BARRIER_OP):
            process_info[erank]["nb_barrier"] = process_info[erank]["nb_barrier"] + 1
        
        if(elem["type"] in MPI_ASYNC_OP):
            process_info[erank]["nb_async_op"] = process_info[erank]["nb_async_op"] + 1
        
        elif(elem["type"] in MPI_SYNC_OP):
            process_info[erank]["nb_sync_op"] = process_info[erank]["nb_sync_op"] + 1
        
        if((elem["type"] in MPI_SEND_OP) or (elem["type"] in MPI_RECV_OP) or (elem["type"] in MPI_COLL_OP)):
            if(elem["partner_rank"] not in process_info[erank]["list_partner"]):
                process_info[erank]["list_partner"].append(elem["partner_rank"])
                process_info[erank]["nb_partner"] = process_info[erank]["nb_partner"] + 1
    
    list_string = []
    for i in range(0,nb_rank):
        list_string.append("Messages sent:\t\t" + str(process_info[i]["nb_message_sent"]) + "\n" +
            "Messages received:\t" + str(process_info[i]["nb_message_recv"]) + "\n" +
            "Barriers:\t\t\t" + str(process_info[i]["nb_barrier"]) + "\n" +
            "Async operation:\t\t" + str(process_info[i]["nb_async_op"]) + "\n" +
            "Sync operation:\t\t" + str(process_info[i]["nb_sync_op"]) + "\n" +
            "Number of partner:\t\t" + str(process_info[i]["nb_partner"]) + "\n" +
            "Partner list:\t" + str(process_info[i]["list_partner"]) + "\n"
            )
    return list_string


def nb_rank(liste):
    max_ = 0
    for elem in liste:
        max_ = max(max_, elem["current_rank"])
    return max_ + 1


def nb_message(liste):
    cpt = 0
    for elem in liste:
        if elem["type"] in MPI_SEND_OP:
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
    nb_bad_async = 0
    cov = 0
    cpt = 0
    for elem in liste_isw:
        if elem.coverage < 100:
            nb_bad_async = nb_bad_async + 1
        cov = cov + elem.coverage
        cpt = cpt + 1
    if len(liste_isw):
        info[2] = nb_bad_async
        info[3] = cov/cpt
    else:
        info[2] = "No Async"
        info[3] = 0
    return info


def ratio_cycle2sec(data):
    if data[0]["type"] not in MPI_INIT_OP:
        print("Error the first MPI operation is not an Init")
    if data[len(data) - 1]["type"] != 'MpiFinalize':
        print("Error the last MPI operation is not a Finalize")

    delta_rdtsc = data[len(data) - 1]["tsc"] - data[0]["tsc"]
    delta_time = data[len(data) - 1]["time"] - data[0]["time"]
    return delta_rdtsc / delta_time

def json_reader(name):
    f = open(name)
    data = json.load(f)
    return data

def test_reader(data):
    for elem in data:
        print(elem)