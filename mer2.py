s = 808
flag = 0
for r, _ in enumerate(iter(bool, True), start=s):
# for r in range(808,100000):
    # input(
    flag = 0
    k = 0
    n = 0
    digits = list(map(int, str(r)))
    # print(r, digits)
    if len(digits)>=2:
        for i in range(len(digits)):
            if digits[i]%2==0 and digits[i] !=0:
                k = 1
            if digits[i]%2==1:
                n = 1
        if k ==1 and n==1:
            for j in range(len(digits)):
                if digits.count(digits[j])==digits[j]:
                    flag +=1
            if flag == len(digits):
                print(r)
                # yield(r)
                # break

                # return r
            

