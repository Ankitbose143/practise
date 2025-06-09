a = True
b = False
c = False

if not a or b:
    # print (not a , b)
    print ("1--", 1)
elif not a or not b and c:
    # print (not a , b, not b, a)
    print ("2--",2)
elif not a or b or not b and a:
    # print (not a , b, not b, a)
    print ("3--",3)
else:
    print ("4--",4)

count= 1
def doThis():

    global count

    for i in (1, 2, 3): 
        count += 1

doThis()

print (count) #4

list1 = [1998, 2002, 1997, 2000]
list2 = [2014, 2016, 1996, 2009]
 
print ("list1 + list 2 = : ", list1 + list2)
# list1 + list 2 = [1998, 2002, 1997, 2000, 2014, 2016, 1996, 2009]
 
print ("list1 * 2 = : ", list1 * 2)
# list1 * 2 = :  [1998, 2002, 1997, 2000,1998, 2002, 1997, 2000]