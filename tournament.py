import os
import time
import shutil

from evaluate import evaluate_stock, pool, evaluate_stock_cycles
from generate import generate_random
from reproduction import reproduct_v2

# Fixed variables for the train
size_pop = 80
epochs = 1000
cores = 8
stock = os.listdir('stock')

newbies = int(0.1 * size_pop)
remove = int(0.9 * size_pop)
childs = int(0.8 * size_pop / 2)

# Initialization
init_time = time.time()
epoch = 0
folder = 'pops/pop0'

log = open('log', 'w')

# Loop on epochs
while epoch < epochs:
  epoch_time = time.time()
  folder = 'pops/pop' + str(epoch)

  # Fill the population with random newbies
  old_pop = len(os.listdir(folder))
  for i in range(size_pop - old_pop):
    generate_random(folder)

  # Evaluate the pool winners against all stock
  scores = evaluate_stock_cycles(folder, cores, remove)
  if scores[-1][1] == stock:
    print('Reference score obtained')
    break
  log.write('Epoch ' + str(epoch) + ' -> ' + scores[-1][0] + ' ' + str(scores[-1][1]) + '\n')

  # Generate childs from winners
  reproduct_v2(folder, childs, scores)

  # Transfer the current population to the next population
  shutil.copytree(folder, 'pops/pop' + str(epoch + 1))

  epoch += 1
  print(epoch, '->', scores[-1][0], scores[-1][1], 'in', int(time.time() - epoch_time), 's')
log.close()
print('Training computed in', time.time() - init_time, 'seconds')
