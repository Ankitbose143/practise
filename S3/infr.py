cmr = {'take':10,'bake':10,'cake':5,'rake':5,'sake':2,'pake':2}

# s = {k: v for k, v in sorted(cmr.items(), key=lambda item: item[1])}
print(sorted(cmr.items(), key = lambda x: (x[1],x[0])))
s = {val[0] for val in sorted(cmr.items(), key = lambda x: (-x[1], x[0]))}
print(s)
