global a
a = 'dssas'
try:
    # name = 'Bob'
    # name += 5

    l = [1,2,3]
    print(l[3])
except NameError as ne:
    # Code to handle NameError
    print("yes",ne)
    # rollbar.report_exc_info()
# except LookupError as e:
#     print('Lookup error')
except TypeError as te:
    # Code to handle TypeError
    print("ok",te)
    # rollbar.report_exc_info()
except IndexError as te:
    # Code to handle TypeError
    print("ok123",te)

# name = 'Bob'
# name += 5