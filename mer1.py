def solve (N, Q, A, query):
    # Write your code here
    # print(N,Q,A,query)
    dfl = len(A)
    sfg = []
    As = A
    while len(A)>2:
        mid = round(N/2)
        p = A[:mid]
        sfg.append(p)
        A = A[mid:]
    sfg.append(A)
    # print(sfg)
    sdfh = 0
    A = As
    B = As
    # # print(A)
    # for t in A:
    sfge= []
    str_out = ''
    for s in query:
        A = As
        B = As
        a, b = s
        k = 0
        print(a,b)
        if a ==1:
            if b ==0:
                while len(A)>2:
                    mid = round(N/2)
                    pr = A[:mid]
                    sfge.append(pr)
                    A = A[mid:]
                sfge.append(A)
                res = []
                sfge = list(filter(None,sfge))
                print("sfge1", sfge, res,len(sfge))
                for t in range(0,len(sfge)):
                    tmp = 0
                    # print(sfge[t],len(sfge[t]))
                    print(t,len(sfge[t]))
                    for ty in range(0,len(sfge[t])):
                        print(t , ty)
                        print(sfge[t][ty])
                        # if sfge[t][ty]:

                        tmp = tmp+sfge[t][ty]
                    print(tmp)
                    res.append(tmp)
                    print(res)
                for tyu in res:
                    k = tyu-k
                # k = int(lambda x,y: x-y,res)
                str_out+=str(abs(k))
                # print("sfge", sfge, res,k,str_out)
                # print(k, end = '')
            else:
                sfge = []
                c=0
                print("lena",len(A),b)
                for t in range(1,b+1):
                    sdf = A[-1]
                    A= A[:-1]
                    A.insert(c,sdf)
                    # print("chk", sdf)
                for i in range(0, len(A), round(len(A)/2)):
                    # print("i==",i)
                    # if i>270:
                    #     n = int(len(A))
                    # else:
                    n = round(len(A)/2)
                    # if i == 590:
                    #     break
                    sfge.append(A[i:i+n])
                # if len(A)>2:
                #     mid = round(N/2)
                #     prq = A[:mid]
                #     sfge.append(prq)
                #     A = A[mid:]
                # sfge.append(A)
                res = []
                print("sfge1", sfge, len(sfge))
                sfge = list(filter(None,sfge))
                print(len(sfge))
                for t in range(0,len(sfge)):
                    tmp = 0
                    # print(sfge[t],len(sfge[t]))
                    for ty in range(0,len(sfge[t])):
                        # print(t , ty)
                        # print(sfge[t][ty])
                        # if sfge[t][ty]:
                        tmp = tmp+sfge[t][ty]
                    # print(tmp)
                    res.append(tmp)
                print(res)
                for tyu in res:
                    k = tyu-k
                print("k",k)
                # k = int(lambda x,y: x-y,res)
                str_out+=str(abs(k))
                # print("sfge11", sfge, res,k,str_out)
        elif a ==2:
            print("aaa",a,A)
            if b ==0:
                sfge =[]
                while len(A)>2:
                    mid = round(N/2)
                    pr = A[:mid]
                    sfge.append(pr)
                    A = A[mid:]
                sfge.append(A)
                res = []
                print("sfge1a", sfge, res)
                sfge = list(filter(None,sfge))
                for t in range(0,len(sfge)):
                    tmp = 0
                    # print(sfge[t],len(sfge[t]))
                    for ty in range(0,len(sfge[t])):
                        # print(t , ty)
                        # print(sfge[t][ty])
                        if sfge[t][ty]:
                            tmp = tmp+sfge[t][ty]
                    # print(tmp)
                    res.append(tmp)
                # print(res)
                for tyu in res:
                    k = tyu-k
                # k = int(lambda x,y: x-y,res)
                str_out+=str(abs(k))
                # print("sfge00", sfge, res,k,str_out)
                # print(k, end = '')
            else:
                sfge = []
                c=0
                print(A)
                for t in range(1,b+1):
                    # print("As2",A)
                    sdf = A[0]
                    A= A[1:]
                    A.insert(len(A),sdf)
                    print("As120",sdf,A)
                print("sfge00", sdf, A)
                while len(A)>2:
                    mid = round(N/2)
                    pr = A[:mid]
                    sfge.append(pr)
                    A = A[mid:]
                sfge.append(A)
                res = []
                # print("sfge1", sfge, res)
                sfge = list(filter(None,sfge))
                for t in range(0,len(sfge)):
                    tmp = 0
                    # print(sfge[t],len(sfge[t]))
                    for ty in range(0,len(sfge[t])):
                        # print(t , ty)
                        # print(sfge[t][ty])
                        if sfge[t][ty]:
                            tmp = tmp+sfge[t][ty]
                    # print(tmp)
                    res.append(tmp)
                # print(res)
                for tyu in res:
                    k = tyu-k
                # k = int(lambda x,y: x-y,res)
                str_out+=str(abs(k))
                # print("sfge00", sfge, res,k,str_out)



           
    return str_out
    #     # print(t)
    # pass

T = int(input())
for _ in range(T):
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    query = [list(map(int, input().split())) for i in range(Q)]

    out_ = solve(N, Q, A, query)
    print("out=",out_)
    print (' '.join(map(str, out_)))