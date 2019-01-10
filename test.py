a = [1, 1]

def foo(b):
    b[1] = 10
    return b

print ('a = ', a)
x = foo(a)
print ('a = ', a)
x[1] = 100
print ('a = ', a)
