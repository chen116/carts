#!/usr/bin/env python

# File: cartsFuncs.py
# Author: Geoffrey Tran gtran@isi.edu

# This file contains useful functions for interfacing with CARTS from Python. 

import xml.etree.ElementTree as ET
import xml
import copy
import subprocess
import os
import pprint
import numpy
import time
import datetime


# from termcolor import colored

CARTS_TEMPLATE_FILE = 'template.xml'
TASKS_FILE_DIR = 'task_sets_icloud_granular/'
CARTS_INPUT_FILE = './CARTS_input_files/'
CARTS_OUTPUT_FILE = './outputs/'
CARTS_LOCATION = './Carts.jar'
CARTS_MODEL = "MPR"

dist = ['uni-light','uni-medium']
lower_b = 0.2
upper_b = 8.4
step = 0.2


util_range = numpy.linspace(lower_b,upper_b,round((upper_b-lower_b)/step + 1))
iters = range(0,25)
util = []
taskset_files_names=[]
print util_range
def run_CARTS_all():
	subprocess.call(["mkdir","-p",CARTS_OUTPUT_FILE])
	print taskset_files_names
	# for i in dist:
	# 	for j in util_range:
	# 		for k in iters:
	# 			if( (j*10)%10==0 ):
	# 				run_one_CARTS(i+'_uni-moderate_'+str(j)[:-2]+'_'+str(k)+".xml")
	# 			else:
	# 				run_one_CARTS(i+'_uni-moderate_'+str(j)+'_'+str(k)+".xml")

# def run_one_CARTS(input_xml_file):	
	# print colored("\tRunning CARTS...","red"),
	print "start CARTS:"
	cart_stdout = open("cart_stdout", 'w')
	cart_stderr = open("cart_stderr", 'w')


	for xml_file_name in taskset_files_names:
		ts=time.time()
		print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')+" : "+xml_file_name

		cart_stderr.write(xml_file_name +'\n')
		cart_stderr.flush()
		subprocess.check_call([
			"java",
			"-jar",
			CARTS_LOCATION,
			CARTS_INPUT_FILE+xml_file_name,
			CARTS_MODEL, 
			CARTS_OUTPUT_FILE+ 'out_'+xml_file_name
			],stderr = cart_stderr, stdout = cart_stdout)
		subprocess.call(["rm","./Ak_max.log"])
		subprocess.call(["rm","./run.log"])
	cart_stdout.close()
	cart_stderr.close()




def create_input_files_for_CARTS():
	subprocess.call(["mkdir","-p",CARTS_INPUT_FILE ])
	for i in dist:
		for j in util_range:
			for k in iters:
				if( str(j)[-1]=='0' ):
					create_one_input_file_for_CARTS(i+'_uni-moderate_'+str(j)[:-2]+'_'+str(k))
				else:
					create_one_input_file_for_CARTS(i+'_uni-moderate_'+str(j)+'_'+str(k))

def create_one_input_file_for_CARTS(input_taskset_file):
	rtDict = {}
	rtDict['vm1'] = []
	with open(TASKS_FILE_DIR+input_taskset_file) as f:
		lines = f.read().splitlines()
    	for line in lines:
			rtDict['vm1'].append(line.split())

	tree = ET.parse(CARTS_TEMPLATE_FILE)
	root = tree.getroot()

	# Write out to STDOUT
	# ET.dump(root)

	for index,item in enumerate(rtDict):
		# print colored("Processing %s"%(item),"green")

		# This creates the new COMPONENT
		component = copy.deepcopy(root[0])
		# print root[0]
  		root.append(component)
  		component.attrib['name'] = item
  		component.tag = 'component'
  		# print component[0]

		# budgets = rtDict[item][0]
		# periods = rtDict[item][1]
		# deadlines = rtDict[item][2]


		for index2, item2 in enumerate(rtDict[item]):
			task = copy.deepcopy(component[0])
			# print task
			component.append(task)
			task.attrib['p'] = str(float(item2[1])/1000)
			task.attrib['d'] = str(float(item2[1])/1000)
			task.attrib['e'] = str(float(item2[0])/1000)
			task.attrib['name'] = 't'+str(index2)

			task.tag = "task"

		# Here, delete the first task, as it is the template
		component.remove(component.find('oldTask'))

	# Here, delete the first component, as it is the placeholder
	root.remove(root.find('oldComponent'))

	# print "Output tree:"

	# ET.dump(root)

	# Write to file

	tree.write(CARTS_INPUT_FILE+input_taskset_file+".xml")	
	taskset_files_names.append(input_taskset_file+".xml")	


def run_CARTS(rtDict):
	# print colored("\tGenerating input XML...","red"),

	tree = ET.parse(CARTS_TEMPLATE_FILE)
	root = tree.getroot()

	# Write out to STDOUT
	# ET.dump(root)

	for index,item in enumerate(rtDict):
		# print colored("Processing %s"%(item),"green")

		# This creates the new COMPONENT
		component = copy.deepcopy(root[0])
		# print root[0]
  		root.append(component)
  		component.attrib['name'] = item
  		component.tag = 'component'
  		# print component[0]

		# budgets = rtDict[item][0]
		# periods = rtDict[item][1]
		# deadlines = rtDict[item][2]

		for index2, item2 in enumerate(rtDict[item]):
			task = copy.deepcopy(component[0])
			# print task
			component.append(task)
			task.attrib['p'] = str(item2[1])
			task.attrib['d'] = str(item2[1])
			task.attrib['e'] = str(item2[0])
			task.tag = "task"

		# Here, delete the first task, as it is the template
		component.remove(component.find('oldTask'))

	# Here, delete the first component, as it is the placeholder
	root.remove(root.find('oldComponent'))

	print "Output tree:"

	ET.dump(root)

	# Write to file
	try:
		tree.write(CARTS_INPUT_FILE)
	except Exception as exc:
		print colored("Caught exception: ","red"),exc
		colored("Ignoring...","red")

	# subprocess.call(["service", services[x], "stop" ])
	# print colored("Done!","green")

	# print colored("\tRunning CARTS...","red"),
	cart_stdout = open("cart_stdout", 'w')
	cart_stderr = open("cart_stderr", 'w')


	for i in range(0,2):
		cart_stderr.write('This is sdfa test' + str(i) +'\n')
		cart_stderr.flush()

		subprocess.check_call([
			"java",
			"-jar",
			CARTS_LOCATION,
			CARTS_INPUT_FILE,
			CARTS_MODEL, 
			CARTS_OUTPUT_FILE
			],stderr = cart_stderr, stdout = cart_stdout)
	cart_stdout.close()
	cart_stderr.close()
	# print colored("Done","green"),


def read_CARTS_Output():
	tree = ET.parse(CARTS_OUTPUT_FILE)
	root = tree.getroot()
	VMs = root.findall('component')
	vmParamDict = {}
	for index,item in enumerate(VMs):
		# print colored('Processing %s'%item.attrib['name'],'green')
		VCPU_budgets = []
		VCPU_periods = []
		VCPU_deadlines = []
		VCPU_data = item.find('processed_task')
		for index2,item2 in enumerate(VCPU_data):
			VCPU_budgets.append(item2.attrib['execution_time'])
			VCPU_periods.append(item2.attrib['period'])
			VCPU_deadlines.append(item2.attrib['deadline'])
		# print VCPU_budgets,VCPU_periods,VCPU_deadlines
		vmParamDict[item.attrib["name"]]=[VCPU_budgets,VCPU_periods,VCPU_deadlines]
	return vmParamDict



if __name__ == "__main__":
	from pprint import pprint

	# rtDict = make_rtDict()
	# print "Input taskset:"
	# pprint(rtDict)

	# run_CARTS(rtDict)
	create_input_files_for_CARTS()
	run_CARTS_all()
	ts=time.time()
	print datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print "DONE"
	# print 
	# print "Output VCPU parameters"
	# pprint(read_CARTS_Output())

