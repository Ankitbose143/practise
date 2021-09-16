# Reverse the string and keep the word "iopex" at begining of the string, if exists

String="This is a test string from iopex, to evaluate your iopex perfromance iopex"
# sorted

str1 = String[::-1]
print(str1)
# xepoi
sd = ''
sd = String.split()
sd1 = str1.count('xepoi')
print(str1.count('xepoi'))
c = 0
for tr in sd:
    if 'xepoi' in str1.lower():
        c+=1
        str1 = str1.replace('xepoi', '')
print(str1, c)
print(String, c)

for t in range(sd1):
    print(t)
    str1 ='iopex '+str1
    # print(str1)

print("Output:")
print(str1)

