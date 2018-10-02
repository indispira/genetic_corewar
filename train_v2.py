import os
import time
import shutil

from evaluate import mp_eval_cycles, break_time, recovered
from generate import generate_random
from reproduction import reproduction

# Fixed variables for the train
size_pop = 80
epochs = 1000
cores = 8
pause = 10
stock = os.listdir('stock')

newbies = 1#int(0.1 * size_pop)
remove = 7#int(0.9 * size_pop)
childs = 3#int(0.8 * size_pop / 2)

# Initialization
epoch = 0
folder = 'pops/pop0'
old_weaks = {}
break_list = {}
log = open('log', 'w')
init_time = time.time()

# Loop on epochs
while epoch < epochs:
  epoch_time = time.time()
  folder = 'pops/pop' + str(epoch)

  # Fill the population with random newbies
  old_pop = len(os.listdir(folder))
  for i in range(size_pop - old_pop):
    generate_random(folder)

  # Evaluate the pool winners against all stock
  scores, weaks = mp_eval_cycles(folder, 'stock', cores, remove)
  if scores[-1][1] == len(stock):
    print('Reference score obtained')
    break
  log.write('Epoch ' + str(epoch) + ' -> ' + scores[-1][0] + ' ' + str(scores[-1][1]) + '\n')
  print(epoch, '->', scores[-1][0], scores[-1][1], len(os.listdir('stock')), 'in', int(time.time() - epoch_time), 's')

  # Check if some champions have recovered
  break_list = recovered(break_list)

  # Remove champions losing too much and give it a break time of some epochs
  old_weaks, break_list = break_time(weaks, old_weaks, size_pop, pause, break_list)

  # Generate childs from winners
  reproduction(folder, childs, scores)

  # Transfer the current population to the next population
  shutil.copytree(folder, 'pops/pop' + str(epoch + 1))
  epoch += 1
log.close()
print('Training computed in', time.time() - init_time, 'seconds')
