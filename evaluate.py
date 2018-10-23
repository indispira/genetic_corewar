import os
import sys
import time
import shlex
import shutil
import subprocess

from threading import Timer
from subprocess import Popen, PIPE
from multiprocessing import Process, Manager

def corewar(p1, p2, flag, timeout=3600):
  cmd = './corewar '+ flag + ' ' + p1 + ' ' + p2
  res = subprocess.Popen(shlex.split(cmd), stdout=PIPE)
  timer = Timer(timeout, res.kill)
  try:
    timer.start()
    result = res.communicate()[0].decode('utf-8').splitlines()
  finally:
    timer.cancel()
    return result

def get_population(folder):
  population = os.listdir(folder)
  scores = {}
  for people in population:
    scores[people] = 0
  return population, scores

def each_eval_cycles(folder, target, pop, scores, defeats):
  tgt, _ = get_population(target)
  for p in pop:
    scores[p] = 0.
    p1 = folder + '/' + p
    for t in tgt:
      p2 = target + '/' + t
      res = corewar(p1, p2, '-v 2', 5)
      if len(res):
        winner = res[-1] if 'Contestant' in res[-1] else res[-2]
        cycle = res[-2] if 'It' in res[-2] else res[-3]
        if winner[11] == '1':
          scores[p] += 1 + (1 / float(cycle.split(' ')[-1]))
          defeats[t] += 1

def mp_eval_cycles(folder, target, cores, old_results, remove=0):
  all_pop, scores = get_population(folder)
  old_winners = [w[0] for w in old_results]
  pop = [p for p in all_pop if p not in old_winners]
  tgt, _ = get_population(target)
  batch = len(pop) / cores
  processes = []
  with Manager() as manager:
    scores = manager.dict()
    defeats = manager.dict()
    for t in tgt:
      defeats[t] = 0
    before = time.time()
    for i in range(cores):
      p = Process(target=each_eval_cycles, args=(folder, target, pop[int(i * batch):int((i + 1) * batch)], scores, defeats,))
      processes.append(p)
      p.start()

    for p in processes:
      p.join()

    for r in old_results:
      scores[r[0]] = r[1]
    result = sorted([(k, v) for k, v in scores.items()], key=lambda x: x[1])
    weaks = defeats.copy()

  # Remove the losers
  if remove:
    for i in range(remove):
      os.remove(folder + '/' + result[i][0])

  result = result[remove:]
  return result, weaks
