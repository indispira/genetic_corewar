import os

champs = os.listdir('newbies')
for c in champs:
  os.remove('newbies/' + c)
