def contains_even_number(l):
    for ele in l:
        if ele % 2 == 0:
            print ("list contains an even number",ele)
            break
 
    # This else executes only if break is NEVER
    # reached and loop terminated after all iterations.
    else:    
        print ("list does not contain an even number",ele)
 
# Driver code
print ("For List 1:")
contains_even_number([1, 9, 8])
print (" \nFor List 2:")
contains_even_number([1, 3, 5])