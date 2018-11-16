import os
from collections import deque
from library.Library import Library
from player.Player import Player


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



# Library Test

lib = Library()
print(lib)
lib.add_tracks('media')

print(lib.list_tracks())


player = Player()

player.play('media/MoodyLoop.wav')

player.stream