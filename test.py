l = [10,3,20,18,40,5]

#second smallest no
# sort(l)[]

for i in range(len(l)):
    for j in range(i+1, len(l)):
        if l[i]>l[j]:
            l[i], l[j]=l[j], l[i]


print("new list",l)
print("second smallest no",l[1])

import re

f = open(r'log.txt')
# print(f.read())
# lineread= f.readlines()
# print(lineread)

# if re.findall(r'error [a-zA-Z]*', lineread):
error_lines = re.findall(r"^.*\[ERROR\].*$", f.read(), re.MULTILINE)
for line in error_lines:
    print(line) 
# print("y",t)
print(re.findall(r"^.*\[ERROR\].*$", f.read(), re.MULTILINE))

# for i in lineread:
#     if "error" in i:
#         print("Error line", i)

error_pattern = re.compile(r".*\bERROR\b.*")

# Find and print all lines with errors
for line in f.read().strip().split('\n'):
    if error_pattern.search(line):
        print(line)