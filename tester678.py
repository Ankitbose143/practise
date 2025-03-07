# airport structure
# class airport feature terminal
# terminal - gates, 
# gates - flight
# flight details
# passenger details

# class airport:
#     def __init__(self,airportname, flight_name, flight_no):
#         self.airportname = airportname
#         self.flight_name = flight_name
#         self.flight_no = flight_no

#     def __details__(self):
#         return f"flight name is {self.flight_name} , flight no is {self.flight_no}"
#         # self.flight_no = flight_no

# class flight:
#     def __init__(self,flight_name, flight_no):
#         self.flight_name = flight_name
#         self.flight_no = flight_no

#     def __str__(self):
#         return f"flight name is {self.flight_name} , flight no is {self.flight_no}"
#         # self.flight_no = flight_no

# class terminal(airport):
#     def __init__(self, gateno, flight_name):
#         self.flight_name = flight_name
#         self.gateno = gateno

#     def __str__(self):
#         return f"flight name is {self.flight_name} , gate no is {self.gateno}, airport {airport.airportname}"
#         # self.flight_no = flight_no


# obj = flight('XYZ', 123)
# print(obj)
# onj2 = terminal(1, 'XYZ')

ip ='aabbbcdfgghsfhi'
# {a:}
op = 'bcdfg'
op2 = 'gshfhi'
max_c = 0
op3 = ''
lo = []
for i in range(len(ip)-1):
    print(i, ip[i])
    if ip[i] != ip[i+1]:
        max_c+=1
        op3+=ip[i]
        print("op3",op3)
        lo.append(op3)
    else:
        lo.append(op3)
        op3 = ''
    # print("lert",i, len(ip), ip[i], ip[i+1])
    if i+1 == len(ip)-1 and ip[i] != ip[i+1]:
        print("len", len(ip))
        op3+=ip[i+1]
        lo.append(op3)

print("lo",lo)
f  = lo.sort(reverse=True)
print(lo[0])

    

