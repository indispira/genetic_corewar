import os
import sys
import shlex
import subprocess

from subprocess import Popen, PIPE

if len(sys.argv) == 1:
  exit(0)
p1 = sys.argv[1]
score = 0
champs = os.listdir('full_stock')
print('There are', len(champs), 'champions in the full stock folder.')
for c in champs:
  p2 = 'full_stock/' + c
  cmd = './corewar ' + p1 + ' ' + p2
  args = shlex.split(cmd)
  res = subprocess.Popen(args, stdout=PIPE)
  res = res.communicate()[0].decode('utf-8').splitlines()
  if res[-1][11] == '1':
    print(c, 'defeated.')
    score += 1
print('Your champion has defeat', score, 'champions from the full stock.')
