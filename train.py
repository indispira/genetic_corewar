import os
import time
import shutil
import multiprocessing

from evaluate import mp_eval_cycles
from generate import generate_random
from reproduction import reproduction

# Fixed variables for the train
# You can customize depending of your needs
cores = multiprocessing.cpu_count()
size_pop = 10 * cores
epochs = 1000
stock_folder = 'stock'
stock = os.listdir(stock_folder)

newbies = int(0.1 * size_pop)
remove = int(0.9 * size_pop)
childs = int(0.8 * size_pop / 2)

# Initialization
epoch = 0
scores = []
folder = 'pops/pop0'
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
  scores, _ = mp_eval_cycles(folder, stock_folder, cores, scores, remove)
  if scores[-1][1] > len(stock):
    print('Maximum score obtained')
    break
  log.write('Epoch ' + str(epoch) + ' -> ' + scores[-1][0] + ' ' + str(scores[-1][1]) + '\n')
  print(epoch, '-', scores[-1][0][:-4], scores[-1][1], 'in', int(time.time() - epoch_time), 's')

  # Generate childs and mutants from winners
  reproduction(folder, childs, scores)

  # Transfer the current population to the next population
  shutil.copytree(folder, 'pops/pop' + str(epoch + 1))
  epoch += 1
log.close()
print('Training computed in', time.time() - init_time, 'seconds')
