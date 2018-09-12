import os
import string
import random

def load_parents(folder):
  files = os.listdir(folder)
  parents = []
  for p in files:
    with open('newbies/' + p[:-3] + 's', 'r') as f:
      parents.append(f.read().split('\n')[3:-1])
  return parents

def reproduct(folder, nb):
  parents = load_parents(folder)

  for i in range(int(nb)):
    name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))

    # Generate the .s file
    with open('childs/' + name + '.s', 'w') as f:
      # The minimum for a champion: name, comment and 1 operation
      f.write('.name "%s"\n.comment ""\n\n' % name)
      
      half = int(len(parents[i]) / 2)
      for j in range(half):
        f.write(parents[i][j] + '\n')
      half = int(len(parents[(i + 1) % len(parents)]) / 2)
      for j in range(half):
        f.write(parents[(i + 1) % len(parents)][j + half] + '\n')
