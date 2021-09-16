def solve (N, Q, A, query):
    # Write your code here
    # # print(N,Q,A,query)
    dfl = len(A)
    sfg = []
    As = A
    while len(A)>2:
        p = A[:2]
        sfg.append(p)
        A = A[2:]
    sfg.append(A)
    # # print(sfg)
    sdfh = 0
    A = As
    B = As
    # # print(A)
    # for t in A:
    sfge= []
    str_out = ''
    for s in query:
        
        # Bs = s
        A = As
        B = As
        
        if query.index(s)%2==0:
            # # print("index",query.index(s))
            # # print(A)
            sfge = []
            a, b = s
            k = 0
            # # print(a,b)
            if b ==0:
                while len(A)>2:
                    pr = A[:2]
                    sfge.append(pr)
                    A = A[2:]
                sfge.append(A)
                res = []
                # print("sfge1", sfge, res)
                for t in range(0,len(sfge[0])):
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
                # print("sfge", sfge, res,k,str_out)
                # print(k, end = '')
            elif b>=1 and b!=0:
                sfge = []
                sdf = A[-a:]
                # sdfg = A[-b:]
                A = A[:-a]
            
                c= 0
                for r in sdf:
                    
                    A.insert(c,r)
                    # c+1
                    # # print("A11",A)
                # # print("sdf",sdf)
                # # print("A",A)
                while len(A)>2:
                    pr = A[:2]
                    sfge.append(pr)
                    A = A[2:]
                sfge.append(A)
                res = []
                # # print("sfge1", sfge, res)
                for t in range(0,len(sfge[0])):
                    tmp = 0
                    for ty in range(len(sfge[t])):
                        tmp = tmp+sfge[t][ty]
                    # # print(tmp)
                    res.append(tmp)
                for tyu in res:
                    k = tyu-k
                # k = int(lambda x,y: x-y,res)
                # print("sfge11", sfge, res,k,str_out)
                str_out+=str(abs(k))
                # print(k, end = '')
        else:
            # # print("index12",query.index(s))
            sfge = []
            a, b = s
            # print(a,b)
            if b>=1:
                sdf = B[:a]
                # sdfg = A[-b:]
                B = B[-b:]
                # # print(B)
                B.insert(b,sdf[0])
                # # print("sdf12",sdf,sdfg)
                # print("A12",B)
            while len(B)>2:
                pr = B[:2]
                sfge.append(pr)
                B = B[2:]
            sfge.append(B)
            res = []
            # print("sfge14", sfge, res,str_out)
            for t in range(0,len(sfge[0])):
                tmp = 0
                for ty in range(0,len(sfge[t])):
                    tmp = tmp+sfge[t][ty]
                # # print(tmp)
                res.append(tmp)
            for tyu in res:
                k = tyu-k
            # k = int(lambda x,y: x-y,res)
            # print(k, end = '')
            str_out+=str(abs(k))
            # print("sfge13", sfge, res,k,str_out)
    
    return str_out
    #     # print(t)
    # pass

T = int(input())
for _ in range(T):
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    query = [list(map(int, input().split())) for i in range(Q)]

    out_ = solve(N, Q, A, query)
    # print("out=",out_)
    print (' '.join(map(str, out_)))