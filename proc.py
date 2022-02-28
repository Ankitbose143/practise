


from itertools import permutations , combinations_with_replacement, combinations

# import request
# print(request.post)
# input: 
nums = [1,2,3] 
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]



d = permutations(nums,3)
comb = combinations_with_replacement([1, 2, 3], 3)
 
# Print the obtained combinations
for i in list(comb):
    print(i)
print(d.__str__)
lt = []
lt1 = []
# df = [list(t) for t in combinations(nums,3)]
# print("df",df)
for i in d:
    # print(list(i))
    lt.append(list(i))
# print(lt)
# for t in range(len(nums)):
#     for k in range(len(nums)):
        
#         lt.append()


