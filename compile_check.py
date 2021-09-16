import time
import re,os
from pathlib import Path
from gramex.debug import lineprofile
import line_profiler
profile = line_profiler.LineProfiler()
import inspect
import nltk
import atexit
s = 'hjsdsjd ankit bose jhdsjd apple'
# tags12 = nltk.tag(s.split())
# print(tags12)
# print(nltk.ne_chunk(tags12))
# print(nltk.ne_chunk(tags12).draw())

# print(os.path.basename(__file__))
# print(Path(__file__).stem)
# import logger
from datetime import datetime
# st1 = datetime.now()
# for i in range(1,100000):
#     re.findall('TP','''TP Tutorialspoint TP TP ''')
# t1 = datetime.now()
# print("normal findall",t1-st1)
# st = datetime.now()
# for i in range(1,100000):
#     pattern=re.compile('TP')
#     result=pattern.findall('''TP Tutorialspoint TP TP ''')
# et = datetime.now()
# print("compile",et-st)
i_run_once_has_been_run = False
s = ''
st1 = datetime.now()
# @lineprofile
@profile
def hunflair_run_once(macid):
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, 
     function_name, lines, index) = inspect.getframeinfo(previous_frame)
    print(filename, line_number, function_name, lines, index)

    frame,filename,line_number,function_name,lines,index = inspect.stack()[1]
    # print(frame,filename,line_number,function_name,lines,index)
    global i_run_once_has_been_run
    # print("123312", datetime.now()-st1)
    if i_run_once_has_been_run:
        return
    
    global s 
    s='uiu'
    print("Tagger initalize, tagger =r'xyz.pt'",s)
    # func12()
    i_run_once_has_been_run = True
    print(profile.print_stats)


def func12():
    hunflair_run_once(1)
    print("123",s)

func12()

hunflair_run_once(12)
print(profile.print_stats)
atexit.register(profile.print_stats)
func12()
hunflair_run_once(12)
func12()
func12()
func12()
hunflair_run_once(23)
func12()

def func(b):
    b =100
    print(b)

# a = 10
# func(a)