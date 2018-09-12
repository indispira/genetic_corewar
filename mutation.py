import os
import shlex
import string
import shutil
import random
import subprocess

from subprocess import Popen, PIPE

def load_twins():
  files = os.listdir('childs')
  twins = []
  for p in files:
    with open('childs/' + p, 'r') as f:
      twins.append(f.read().split('\n')[3:-1])
  return twins

def shuffle_numbers(line):
  res = ''
  for c in line:
    if c.isdigit() and res[-1] != 'r' and res[-2] != 'r':
      c = str(random.randint(0, 9))
    res += c
  return res

def mutate(folder):
  twins = load_twins()
  for t in twins:
    name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))

    # Generate the .s file
    with open('childs/' + name + '.s', 'w') as f:
      # The minimum for a champion: name, comment and 1 operation
      f.write('.name "%s"\n.comment ""\n\n' % name)

      for l in t:
        if random.randint(0, 50) == 0:
          f.write(shuffle_numbers(l) + '\n')
        else:
          f.write(l + '\n')

  childs = os.listdir('childs')
  for c in childs:
    # Compile the childs
    cmd = './asm childs/' + c
    args = shlex.split(cmd)
    res = subprocess.Popen(args, stdout=PIPE)
    res = res.communicate()[0].decode('utf-8').split('\n')

    # Move the childs in the right folder
    shutil.move('childs/' + c, 'newbies/' + c)
    shutil.move('childs/' + c[:-1] + 'cor', folder + '/' + c[:-1] + 'cor')
