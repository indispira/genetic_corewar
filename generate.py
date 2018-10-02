import os
import shlex
import shutil
import string
import random
import subprocess

from subprocess import Popen, PIPE

size_max = 650
size_min = 400

def reg():
  return str(random.randint(1, 16))

def dir():
  return str(random.randint(0, 4294967295))

def ind():
  return str(random.randint(-32768, 32767))

def reg_ind(length):
  if random.randint(0, 1):
    op = 'r' + reg()
  else:
    op = ind()
    length += 1
  return op, length + 1

def reg_dir(length):
  if random.randint(0, 1):
    op = 'r' + reg()
  else:
    op = '%' + dir()
    length += 3
  return op, length + 1

def ind_dir(length):
  if random.randint(0, 1):
    op = ind()
  else:
    op = '%' + dir()
    length += 2
  return op, length + 2

def reg_ind_dir(length):
  r = random.randint(0, 2)
  if r == 0:
    op = 'r' + reg()
  elif r == 1:
    op = ind()
    length += 1
  else:
    op = '%' + dir()
    length += 3
  return op, length + 1

def op_live(length):
  op = 'live\t%' + dir() + '\n'
  return op, length + 5

def op_ld(length):
  op = 'ld\t'
  tmp, length = ind_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_st(length):
  op = 'st\tr' + reg() + ','
  tmp, length = reg_ind(length)
  op += tmp + '\n'
  return op, length + 3

def op_add(length):
  op = 'add\tr' + reg() + ',r' + reg() + ',r' + reg() + '\n'
  return op, length + 5

def op_sub(length):
  op = 'sub\tr' + reg() + ',r' + reg() + ',r' + reg() + '\n'
  return op, length + 5

def op_and(length):
  op = 'and\t'
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_ind_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_or(length):
  op = 'or\t'
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_ind_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_xor(length):
  op = 'or\t'
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_ind_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_zjmp(length):
  op = 'zjmp\t%' + ind() + '\n'
  return op, length + 3

def op_ldi(length):
  op = 'ldi\t'
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_sti(length):
  op = 'sti\tr' + reg() + ','
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_dir(length)
  op += tmp + '\n'
  return op, length + 3

def op_fork(length):
  op = 'fork\t%' + ind() + '\n'
  return op, length + 3

def op_lld(length):
  op = 'lld\t'
  tmp, length = ind_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_lldi(length):
  op = 'lldi\t'
  tmp, length = reg_ind_dir(length)
  op += tmp + ','
  tmp, length = reg_dir(length)
  op += tmp + ',r' + reg() + '\n'
  return op, length + 3

def op_lfork(length):
  op = 'lfork\t%' + ind() + '\n'
  return op, length + 3

def initiate_ops_all():
  return [op_live, op_ld, op_st, op_add, op_sub, op_and, op_or, op_xor,
          op_zjmp, op_ldi, op_sti, op_fork, op_lld, op_lldi, op_lfork]

def initiate_ops_meta():
  ops = []
  ops.append(op_and)
  ops.append(op_sub)
  ops.append(op_ldi)
  ops.append(op_xor)
  for i in range(38):
    if i <= 2:
      ops.append(op_or)
      ops.append(op_add)
    if i <= 6: ops.append(op_fork)
    if i <= 7: ops.append(op_sti)
    if i <= 9: ops.append(op_zjmp)
    if i <= 10: ops.append(op_lfork)
    if i <= 20: ops.append(op_ld)
    if i <= 28: ops.append(op_live)
    if i <= 38: ops.append(op_st)
  return ops

ops = initiate_ops_meta()

def random_op(length):
  return ops[random.randint(0, len(ops) - 1)](length)

def generate_random(folder):
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  length = 0

  # Generate the .s file
  with open(folder + '/' + name + '.s', 'w') as f:
    # The minimum for a champion: name, comment and 1 operation
    f.write('.name "%s"\n.comment ""\n\n' % name)
    op, length = random_op(length)
    f.write(op)

    while length < size_min or (length < size_max and random.randint(0, 30)):
      op, length = random_op(length)
      f.write(op)

  # Compile the .s file to get .cor file
  cmd = './asm ' + folder + '/' + name + '.s'
  args = shlex.split(cmd)
  res = subprocess.Popen(args, stdout=PIPE)
  res = res.communicate()[0].decode('utf-8').split('\n')

  # Move .s file to the archives
  shutil.move(folder + '/' + name + '.s', 'newbies/' + name + '.s')
  return True
