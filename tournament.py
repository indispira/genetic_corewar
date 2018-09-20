import os
import time
import shutil

from evaluate import evaluate_stock, pool
from generate import generate_random
from reproduction import reproduct_v2

# Fixed variables for the train
size_pop = 800
epochs = 2000
pools = 8
stock = os.listdir('stock')
newbies = int(0.1 * size_pop)
remove = int(0.9 * size_pop / pools)
childs = int(0.8 * size_pop)

# Initialization
init_time = time.time()
epoch = 0
folder = 'pops/pop0'

# Loop on epochs
while epoch < epochs:
  epoch_time = time.time()
  folder = 'pops/pop' + str(epoch)

  # Fill the population with random newbies
  old_pop = len(os.listdir(folder))
  for i in range(size_pop - old_pop):
    generate_random(folder)

  # Evaluate each pool of champions and kill the losers
  pool(pools, folder, remove)

  # Evaluate the pool winners against all stock
  scores = evaluate_stock(folder)
  if scores[-1] == stock:
    print('Reference score obtained')
    break

  # Generate childs from winners
  reproduct_v2(folder, childs, scores)

  # Transfer the current population to the next population
  shutil.copytree(folder, 'pops/pop' + str(epoch + 1))

  epoch += 1
  print('Epoch', epoch, 'computed in', time.time() - epoch_time, 'seconds')
print('Training computed in', time.time() - init_time, 'seconds')
