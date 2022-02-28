# l = [11,12,13,14,15, 12, 2 ,4,5,6,7]
# k = 0
# for t in range(0,len(l)):
#     for y in range(t+1, len(l)):
#         if l[t]+l[y] == 24:
#             print("24 sum", l[t], l[y])



# f = 
# d = [k+=1 for i in range(l) for j in range(1,i)  if i%j==0]
# for i in l:
    
# t = 0
# for j in range(1,l[t]+1):
#     t+1
#     if l[t]!=1:
#         k = 0
#     # print(i,j)
#     if l[t]%j==0:
#         k+=1
#     if k ==2:
#         print("prime", i)


def getPairsCount(arr, n, sum):
    unordered_map = {}
    count = 0
    for i in range(n):
        if sum - arr[i] in unordered_map:
            count += unordered_map[sum - arr[i]]
 
        if arr[i] in unordered_map:
            unordered_map[arr[i]] += 1
        else:
            unordered_map[arr[i]] = 1
        print(unordered_map)
 
    return count
 
# Driver code
arr = [1, 5, 7, -1, 5]
n = len(arr)
sum = 6
print('Count of pairs is', getPairsCount(arr, n, sum))