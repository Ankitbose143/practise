l = [7,2,3]
m = [2,2,2,2]
print(l)
r = 0
t = 0
while l[0]>0:
    print("====l",l,r)
    if 0 in l:
        l.remove(0)
    # while
    for k in range(1,len(l)):
        if len(l)==k:
            print(l,k)
            t = 1
        if t ==0:
            if l[k]>0:# and t==0:
                l[k]=l[k]-1
                l[0]=l[0]-1
                r+=2
                if 0 in l:
                    l.remove(0)
        
    # while 
    # print("l1",l,r)
    # if len(l)==3:
    #     if l[2]>0:
    #         l[2]=l[2]-1
    #         l[0]=l[0]-1
    #         r+=2
    # print("r",l,r)
    if len(l)==1:
        # print(l)
        if l[0]>1:
            print("hi")
            r+=1
            print("hi,",r)
            break
print("l2",l,r)
