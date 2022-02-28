s = 212
flag = 0
import time
import itertools
st = time.time()
for r in range(s,10**12):

# for r, _ in enumerate(iter(bool, True), start=s):
# for r in range(808,100000):
    # input(
    t = []
    tr = []
    flag = 0
    flag1=0
    flag2 =0
    k = 0
    n = 0
    digits = list(map(int, str(r)))
    # print(r, digits)
    eve = 0
    odd =0
    if len(digits)>=2:
        word_eve = [t.append(digits[i])  for i in range(len(digits)) if digits[i]%2==0]
        word_odd = [tr.append(digits[i]) for i in range(len(digits)) if digits[i]%2==1 ]
        # for i in range(len(digits)):
        #     if digits[i]%2==0 and digits[i] !=0:
        #         k = 1
        #     if digits[i]%2==1:
        #         n = 1
    
        if len(set(t))==1 and len(set(tr))==1:# and word_eve and word_odd:
            
            sd = [1 for j in range(len(digits)) if digits.count(digits[j])==digits[j]]
            if sd and len(sd) == len(digits) and r>s:# and len(set(t))==1 and len(set(tr))==1:
                print(r)
                print(time.time()-st)
                # yield(r)
                break

                # return r
            

