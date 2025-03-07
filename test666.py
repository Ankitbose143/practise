# [[1, 2, [3, 4]], [5, 6], 7]
 
# Output: [1, 2, 3, 4, 5, 6, 7]
 
# Input: [[1, 2, [[3,4], 5]], [6, 7]]
def flatten(f):
    g = []
    g.extend(f)
    print(g)
    return g

l  = [[1, 2, [[3,4], 5]], [6, 7]]

emp_l = []
# [1, 2, [[3,4], 5]]
# [1, 2, [[3,4], 5]]

def rec_list(g):
    for i in g:
        # print("i", i, type(i), isinstance(i, list))
        if type(i)==list:
            f = rec_list(i)
            print("f", f)
        else:
            emp_l.append(i)
    return emp_l
print("list new", rec_list(l))

# git master, feat1 test.py, feat2, test.py
# feat2 has pushed to master
# 2 deve, 2 has put some error code
# git reflog
# success commit
# fail commit

# db 20 or 30 million
# select *
# in place of 8 use column names
# database partitioning


from itertools import chain

# def flatten_list(nested_list):
#     for i in nested_list:
#         if isinstance(i, list):
#             print("chain",chain.from_iterable(i))
#             print("chain2",chain.from_iterable(flatten_list(i)))
#         else:
#             print([i])

#     # return list(chain.from_iterable(flatten_list(i) if isinstance(i, list) else [i] for i in nested_list))

# l = [[1, 2, [[3, 4], 5]], [6, 7]]
# print("Flattened List:", flatten_list(l))


l = [1, 2, 3]

def foo(param):
    param = param.copy()  # Create a copy to avoid modifying the original list
    param.append(4)  # Modify the copy
    print(param)  # Output: [1, 2, 3, 4]

foo(l)  # Pass the original list
print(l)  # Output: [1, 2, 3] (Original list remains unchanged)



    




 