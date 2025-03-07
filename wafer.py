# array of temp daily temp reading for n conecutive days,
# each day find the next warmest day
T = [30, 35, 40, 38, 42, 42, 39]

# index
# [1, 2, 4, 4, -1, -1, -1]
highest = 0
lt = [-1]*len(T)
for i in range(len(T)-1):
    print(T[i])
    if T[i+1]>T[i]:
        lt.insert(i,T.index(T[i+1]))
        highest = T[i]
    elif T[i+1]==T[i]:
        lt.insert(i,T.index(T[i+1]))
    # elif highest >T[i]:
        # lt.append(i,-1)

print(lt)
# monotonous decreasing stack

def next_warmer_day(T):
    n = len(T)
    res = [-1] * n  # Default all indices to -1
    stack = []  # Monotonic decreasing stack storing indices

    for i in range(n):
        while stack and T[i] > T[stack[-1]]:
            prev_index = stack.pop()
            res[prev_index] = i  # Store the index of the next warmer day
        stack.append(i)

    return res

T = [30, 35, 40, 38, 42, 42, 39]
print(next_warmer_day(T))  # Output: [1, 2, 4, 4, -1, -1, -1]


# pyspark jobs small dataset , fails for larger dataset
# wide transformation



 