def fun():
    r = []
    for i in range(1,1000):
        if i%2==0:
            r.append(i)
    return r
import polling


def fun12():
    # test_list
    L = [2, 4, 6, 8, 9, 10, 12, 16, 18, 20, 7, 30]
    r = []
    # L= 1
    a = [n for n, _ in enumerate(L)]

    # using range and len
    a1 = [n for n in range(len(L))]
    print(a)
    print(a1)
    # for i,val in enumerate(test_list,1):
    #     print(i, val)
    #     if val%2==0:
    #         r.append(val)
    # print(r)
    return r

def rt():
    import cProfile
    # cProfile.run('fun12()')
    cProfile.run('fun12(), fun()')
fun12()
# rt()