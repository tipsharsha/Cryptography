def extended_euclidean(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        d, x, y = extended_euclidean(b, a % b)
        print(d, x, y)
        return (d, y, x - (a // b) * y)
    
