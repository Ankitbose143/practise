arr = [11, 15, 6, 8, 9, 10,3,13]
d = sorted(arr, reverse = True)
print(d)
n = len(d)
h = 0
sum = 16
s = []
for i in range(0,n):
    for j in range(i + 1, n):
        if arr[i] + arr[j] == sum:
            print(arr[i],arr[j])
    # if arr[i]+arr[n-1]==16:
    #     s.append(arr[i])
    #     s.append(arr[n-1])
    #     continue
        # print(arr[i], arr[n-1])
# print(s)