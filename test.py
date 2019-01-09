a = [1, 1]
def foo(list):
    list[1] = 10
    return list

print ('a = ', a)
x = foo(a)
print ('a = ', a)
x[1] = 100
print ('a = ', a)
