import os
from collections import deque


pathname = 'test_dir'


if os.path.isfile == True:
    print(pathname)
elif os.path.isdir(pathname) == True:
    print('is dir')
    list = deque(map(lambda name: pathname + '/' + name, os.listdir(pathname)))
    print(list)
else:
    print('error')


#list append test

list1 = deque([1,2,3])
list2 = deque([4,5,6])

list1.extend(list2)

print(list1)
