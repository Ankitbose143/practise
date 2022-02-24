n = 5
ft = 1
for i in range(1,n+1):
    ft= ft*i

print("fact",ft)

import time

# d = time.time()
# for t in range(10000000):
#     # f = d/3600
#     print("time",d)


class Vehicle:
    def __init__(self,name,wheels,windows):
        self.name = name
        self.wheels = wheels
        self.windows = windows


class Driver:
    def __init__(self,name,mobile,address):
        self.name = name
        self.mobile = mobile
        self.address = address

s = Vehicle('Maruti', 4, 4)

import time
  
# define the countdown func.
def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        # print(mins,secs)
        for i in range(10000):
            print('{:02d}'.format(t),end='\r')
        # print("sasa",'{:0d}'.format(secs))
        # timer = '{:02d}:{:02d}'.format(mins, secs)
        # print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Fire in the hole!!')
  
  
# input time in seconds
t = input("Enter the time in seconds: ")
  
# function call
countdown(int(t))