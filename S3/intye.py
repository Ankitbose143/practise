# def mydec(f):
#     def wrapper(*args,**kwargs):
#         print("hi")
#         for t,j in kwargs.items():
#             print(t,j)
#         # d = f(*args)
#         print("hey124")
#         # return d
#     return wrapper

# # @mydec
def prasa(a,b):
    s = a+b
    return s
#     # assert s==8
#     # print()

# prasa(6,6)
# # print(prasa())
# def func(x):
#     return x +4
 
# def test_func():
#     assert prasa(4,5) == 8
import pytest, mathlib
# from pytest import mark

# @pytest.mark.parametrize("test_input", "expected_output", [ (5, 25), (6, 36), (7, 49) ] )
# def test_cal_square(test_input, expected_output):
#     result = mathlib.cal_square(test_input)
#     assert result == expected_output

# j = [1,2,3,4]
# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_eval(test_input, expected):
#     assert eval(test_input) == expected
# k = [3,4,5,6]
@pytest.mark.parametrize("test_input,expected", [("3+5",8),("3+6",9)])
def add(test_input,expected):
    # result = prasa()
    k = test_input.split('+')
    k = [int(t) for t in k]
    print(test_input,k)
    assert prasa(k[0],k[1])==expected
    # print("ooo",prasa(eval(test_input)), type(eval(test_input)),expected)
#     assert eval(test_input) == expected
    # assert prasa(eval(test_input))==expected
    # assert prasa(k[0],k[1])==expected

# add("6+9",15)

# @pytest.mark.parametrize("number", [1, 2, 3, 0, 42])
# def test_foo(number):
#     assert number > 0
#     a=9
#     b = 10
#     d = prasa(a,b)
#     assert d==(a+b)

# docker ps -a
# docker exec -it <containerid>

# import re
# a = 'ssas_.as@gmail.com'
# sd = re.search(r'\w+\_|.\w+|([a-z]+@)', a)
# print(sd.group(0,1))
# print(sd.start(), sd.end())

# nohup xyz.txt>log.txt &2

# vim 
# d = Jens
# if d ==0:
    # elif 
# boolean()