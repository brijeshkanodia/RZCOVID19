#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:30:27 2020

@author: brijesh

GENERIC CODE
"""

import csv
import numpy as np
import math as m
import matplotlib.pyplot as plt
import scipy.optimize as sci

#### Path of CSV Covid File ####
with open("/Path/File.csv", 'r') as f:
    cases = list(csv.reader(f, delimiter=","))
##########################
cases = np.array(cases[1:])

days=np.arange(0,len(cases),step=1)
inf=[]
for i in range(len(cases)):
    inf.append(cases[i][2])
    
infected = [int(float(numeric_string)) for numeric_string in inf]

#plt.plot(days, np.log(infected))      

#### counting data on weekely basis ###
weekely_inf=[]
x=14
week=[]
for j in range(len(infected)):
    if(x%7==0 and x<=len(infected)):
        weekely_inf.append(infected[x])
        week.append((x/7)-1)
        x+=7
        
    
    
## Regulazation fucntion coming from particle physics model ###
def fit_func(week,a,b,g):
    return np.exp(a*np.exp(week*g)/(b+np.exp(week*g)))
# Log of the same funtion
def fit_log_func(week,a,b,g):
    return a*np.exp(week*g)/(b+np.exp(week*g))

# using scipy otimizer to do the polynomial fit 
popt, pcov = sci.curve_fit(fit_func, week, weekely_inf)
popt1, pcov1 = sci.curve_fit(fit_log_func, week, np.log(weekely_inf))

print(popt)
print(popt1)

# fit parameters 
a=popt1[0]
b=popt1[1]
g=popt1[2]

# comparsion with actual function
def func(t):
    return a*np.exp(t*g)/(b+np.exp(g*t))

def fbeta(alpha, t):
    return -alpha*b*g/(b+np.exp(g*t))

time= np.linspace(-10,10, num=50)

alpha=[]
beta=[]

### trucation of data 

for i in range(len(time)):
    alpha.append(func(time[i]))
    beta.append(fbeta(alpha[i],time[i]))
for j in range(len(time)):
    if(beta[j]-beta[j-1]<=1e-8):
        print(alpha[i])
        
    
# using matplotlib to show data behaviour    
plt.plot(time,alpha)
plt.xlabel("weeks(upto-28Aug)")
plt.ylabel(" alpha")
plt.title("Maharashtra") 
plt.show()

plt.plot(alpha,beta)
plt.xlim(xmin=0)
plt.xlabel("alpha")
plt.ylabel("Beta")
plt.title("Maharashtra") 
plt.show()


plt.plot(week, weekely_inf,'o',linestyle='dotted', label="data plot")
plt.plot(np.array(week), fit_func(np.array(week),*popt),label="fitted plot")
plt.legend()
plt.xlabel("weeks(upto 28-AUG)")
plt.ylabel(" Infected case")
plt.title("State-Maharashtra") 
plt.show()


plt.plot(week, np.log(weekely_inf),'o',linestyle='dotted', label="data plot")
plt.plot(np.array(week), fit_log_func(np.array(week),*popt1),label="fitted plot")
plt.legend()
plt.xlabel("weeks(upto 28-AUG)")
plt.ylabel(" log(Infected case)")
plt.title("State-Maharashtra") 
plt.show()
