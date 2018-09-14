import os

champs = os.listdir('newbies')
for i, c in enumerate(champs):
  if i % 10000 == 0:
    print(i, 'elements deleted')
  os.remove('newbies/' + c)
