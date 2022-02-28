from itertools import takewhile
#, izip
import itertools 

def match_iter():
    elements = 0
    i=1
    for element in itertools.count(i):
        print(element)
        if element==100000:
            break
            # i+=1
        elements+=1
    print(elements)
    return elements
    # return sum(1 for x in itertools(lambda x: x[0] == x[1],
                                        # izip(self, other)))

def match_loop():
    elements = 0
    for element in range(1,100000):
        elements+=1
    # for element in range(min(len(self), len(other))):
        # if self[element] != other[element]:
            # element -= 1
            # break
    return elements

def test():
    a = [0, 1, 2, 3, 4]
    b = [0, 1, 2, 3, 4, 0]

    print("match_loop a=%s, b=%s, result=%s" % (a, b, match_loop()))
    print("match_iter a=%s, b=%s, result=%s" % (a, b, match_iter()))

    # i = 10000
    # while i > 0:
    #     i -= 1
    #     match_loop()
    match_iter()

def profile_test():
    import cProfile
    cProfile.run('test()')

if __name__ == '__main__':
    profile_test()