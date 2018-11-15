import os
import shlex
import shutil
import string
import random
import generate
import subprocess

from generate import random_op
from subprocess import Popen, PIPE

def code_parents(folder):
  files = os.listdir(folder)
  parents = {}
  for f in files:
    with open('newbies/' + f[:-3] + 's', 'r') as n:
      parents[f] = n.read().splitlines()[3:]
  return parents

def mutate_line(line):
  if not random.randint(0, 3):
    line, _ = random_op(0)
  else:
    op, code = line.split('\t')
    op = 'op_' + op
    line, _ = getattr(generate, op)(0)
  return line[:-1]

def crossover_v2(folder, father, mother):
  parts = random.randint(2, 20)
  l = int(min(len(father), len(mother)) / parts)

  son = []
  daughter = []
  for i in range(parts):
    if random.randint(0, 1):
      son += father[i * l:(i + 1) * l]
      daughter += mother[i * l:(i + 1) * l]
    else:
      son += mother[i * l:(i + 1) * l]
      daughter += father[i * l:(i + 1) * l]
  son += father[len(son):]
  daughter += mother[len(daughter):]

  mutate = False if random.randint(0, 4) else True
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for line in son:
      if mutate and not random.randint(0, 24):
        line = mutate_line(line)
      f.write(line + '\n')

  mutate = False if random.randint(0, 4) else True
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for line in daughter:
      if mutate and not random.randint(0, 24):
        line = mutate_line(line)
      f.write(line + '\n')  

def crossover(folder, father, mother):
  l = int(min(len(father), len(mother)) / 4)
  son = father[:l] + mother[l:l * 2] + father[l * 2:l * 3] + mother[l * 3:l * 4] + father[l * 4:]
  daughter = mother[:l] + father[l:l * 2] + mother[l * 2:l * 3] + father[l * 3:l * 4] + mother[l * 4:]

  mutate = False if random.randint(0, 4) else True
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for line in son:
      if mutate and not random.randint(0, 24):
        line = mutate_line(line)
      f.write(line + '\n')

  mutate = False if random.randint(0, 4) else True
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for line in daughter:
      if mutate and not random.randint(0, 24):
        line = mutate_line(line)
      f.write(line + '\n')

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

def reproduction(folder, nb, scores):
  redcode = code_parents(folder)

  # Ponderate the chance to be parent following the score of each champion
  parents = os.listdir(folder)
  for s in scores:
    for _ in range(int(s[1])):
      parents.append(s[0])

  for i in range(nb):
    father = random.randint(0, len(parents) - 1)
    mother = random.randint(0, len(parents) - 1)
    while father == mother:
      mother = random.randint(0, len(parents) - 1)
    crossover_v2(folder, redcode[parents[father]], redcode[parents[mother]])

  compile_childs(folder)
