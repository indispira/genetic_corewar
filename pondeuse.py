import os
import shlex
import shutil
import subprocess

from threading import Timer
from subprocess import Popen, PIPE
from multiprocessing import Process, Manager

from generate import generate_random


def corewar(p1, p2, timeout=3600):
  cmd = './corewar ' + p1 + ' ' + p2
  res = subprocess.Popen(shlex.split(cmd), stdout=PIPE)
  timer = Timer(timeout, res.kill)
  try:
    timer.start()
    result = res.communicate()[0].decode('utf-8').splitlines()
  finally:
    timer.cancel()
    return result

def worker():
  maxi = 0
  while True:
    champ = generate_random('temp')
    stk = os.listdir('stock')
    score = 0
    for s in stk:
      p1 = 'temp/' + champ + '.cor'
      p2 = 'stock/' + s
      res = corewar(p1, p2, 5)
      if len(res):
        winner = res[-1] if 'Contestant' in res[-1] else res[-2]
        if winner[11] == '1':
          score += 1
    if score > maxi:
      maxi = score
    if score > 19:
      print(champ, 'has scored', score, '/', maxi)
    if score > 35:
      shutil.move('temp/' + champ + '.cor', 'goodones/' + champ + '.cor')
      print(champ, 'moved in the goodones folder')

processes = []
with Manager() as manager:
  for i in range(8):
    p = Process(target=worker)
    processes.append(p)
    p.start()

  for p in processes:
    p.join()
