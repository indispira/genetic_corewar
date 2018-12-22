import os
import sys
import shlex
import subprocess

from subprocess import Popen, PIPE

stock = os.listdir('stock')
print('There are', len(stock), 'champions in the stock folder.')

for s in stock:
  score = 0
  p1 = 'stock/' + s
  for ss in stock:
    if ss == s:
      continue
    p2 = 'stock/' + ss
    cmd = './corewar ' + p1 + ' ' + p2
    args = shlex.split(cmd)
    res = subprocess.Popen(args, stdout=PIPE)
    res = res.communicate()[0].decode('utf-8').splitlines()
    if res[-1][11] == '1':
      score += 1
  print(s, 'has defeat', score, 'champions from the stock.')
