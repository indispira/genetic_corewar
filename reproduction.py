import os
import shlex
import shutil
import string
import random
import subprocess

from mutation import mutate_v2
from subprocess import Popen, PIPE

def load_parents(folder):
  files = os.listdir(folder)
  parents = []
  for p in files:
    with open('newbies/' + p[:-3] + 's', 'r') as f:
      parents.append(f.read().split('\n')[3:-1])
  return parents

def code_parents(folder):
  files = os.listdir(folder)
  parents = {}
  for f in files:
    with open('newbies/' + f[:-3] + 's', 'r') as n:
      parents[f] = n.read().splitlines()[3:]
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

def generate_child(folder, father, mother):
  start = father[:int(len(father) / 2)]
  end = mother[int(len(mother) / 2):]
  while len(start) + len(end) < 60:
    start.append(father[random.randint(int(len(father) / 2), len(father) - 1)])
    end.append(mother[random.randint(0, int(len(mother) / 2))])

  # Mutate the child ?
  if random.randint(0, 20) == 0:
    start, end = mutate_v2(start, end)

  # Generate the .s file
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    # The minimum for a champion: name, comment and 1 operation
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for l in start:
      f.write(l + '\n')
    for l in end:
      f.write(l + '\n')

def compile_childs(folder):
  childs = os.listdir('childs')
  for c in childs:
    # Compile the childs
    cmd = './asm childs/' + c
    res = subprocess.Popen(shlex.split(cmd), stdout=PIPE)
    res = res.communicate()[0].decode('utf-8').split('\n')

    # Move the childs in the right folder
    shutil.move('childs/' + c, 'newbies/' + c)
    shutil.move('childs/' + c[:-1] + 'cor', folder + '/' + c[:-1] + 'cor')

def reproduct_v2(folder, nb, scores):
  redcode = code_parents(folder)

  # Ponderate the chance to be parent following the score of each champion
  parents = os.listdir(folder)
  for s in scores:
    for _ in range(s[1]):
      parents.append(s[0])

  for i in range(nb):
    father = random.randint(0, len(parents) - 1)
    mother = random.randint(0, len(parents) - 1)
    generate_child(folder, redcode[parents[father]], redcode[parents[mother]])

  compile_childs(folder)
