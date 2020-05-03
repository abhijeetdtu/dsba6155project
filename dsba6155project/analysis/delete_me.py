
from collections import defaultdict

vals = defaultdict(int)

def stringMatch(a , b):
    print(a,b)
    k = a + "_" + b
    if k in vals:
        return  vals[k]
    if a == b:
        return 0

    # addition
    valA = -1 + stringMatch(a, b[1:])
    valD = -1 + stringMatch(a[1:] , b)
    valR = -1 + stringMatch(a[1:] , b[1:])
    val =  max(valA , valD , valR)
    vals[k] = val
    return val

stringMatch("geek" , "gesek")
