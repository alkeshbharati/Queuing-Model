from __future__ import division
import Queue
import math
import threading
import time
import numpy
waiting_queue=Queue.Queue()
current_plaza=[]

num_booths=int(raw_input("enter the number of toll booths:"))
avg_arrival=float(raw_input("enter the average arrival rate (cars per minute)")) #lambda
avg_service=float(raw_input("enter the average service rate (cars per minute)")) #Mu
rho=(1.0*avg_arrival/(avg_service*num_booths)) # service utilization
c1=0.00
if rho==1.0:
	rho=1.1
for i in range(num_booths):
	c1=c1+(math.pow((num_booths*rho),i)/math.factorial(i))
c1=c1+(math.pow((num_booths*rho),num_booths)/(math.factorial(num_booths)*(1-rho)))
pzero=1/c1
Lq= pzero*math.pow((1.0*avg_arrival/avg_service),num_booths)*rho # average number of cars in the queue
Lq= Lq/(math.factorial(num_booths)*math.pow((1-rho),2))
if rho<1: # condition for stable system
	print "The utilisation of the queue is %0.2f" %rho
	print "pzero is: %f" %pzero
	print "Lq (mean number of customers in the queue are) %f" %Lq
else:
	print "The queue is unstable and will grow without bounds"
print "Starting simulation:"

on=True

def toll_booth(booth_num):
	while on:
		car_no=waiting_queue.get()
		if car_no==-1:
			waiting_queue.task_done()
			break
		else:
			t=60/avg_service
			t=numpy.random.exponential(int(t),size=(1))[0]
			current_plaza[booth_num]=car_no
			for i in range(int(t)):
				time.sleep(1)
				if not on:
					break
			current_plaza[booth_num]=0
			
def start_queue():
	j=1
	while on:
		waiting_queue.put(j)
		j+=1
		t=60/avg_arrival
		interval=numpy.random.poisson(t,size=(1))[0]
		for i in range(interval):
			time.sleep(1)
			if not on:
				break
		



for i in range(num_booths):
	current_plaza+=[0]
	threading.Thread(target=toll_booth, args=(i,)).start()

threading.Thread(target=start_queue).start()


try:
	while True:
		print "\n\n"
		print "Queue Condition:"
		for i in list(waiting_queue.queue):
			print "%d " %i,
		print "\n"
		print "Toll Plaza respective service car numbers:"
		for i in range(num_booths):
			print "%d " %current_plaza[i],
		print "\n"
		for i in range(int(30/avg_service)):
			time.sleep(1)
		
except KeyboardInterrupt:
	for i in range(num_booths):
		waiting_queue.put(-1)
		on=False
		break;
		
