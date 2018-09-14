import os
import time
import shutil

from mutation import mutate
from reproduction import reproduct
from generate import generate_random
from evaluate import evaluate_active, evaluate_reference, evaluate_all_refs, evaluate_cycles

size_pop = 1000
epochs = 2000

newbies = 0.1 * size_pop
remove = 0.7 * size_pop
childs = 0.3 * size_pop

# Initialization
init_time = time.time()
step = 0
folder = 'pops/pop0'

# Generate the first population if needed
old_pop = len(os.listdir(folder))
for i in range(size_pop - old_pop):
  generate_random(folder)

# Loop for training
for i in range(epochs):
  epoch_time = time.time()
  folder = 'pops/pop' + str(i)

  # Transfer of the population to the next
  if i != 0:
    shutil.copytree('pops/pop' + str(i - 1), folder)

  # Evaluate the population
  results = evaluate_cycles(folder)

  # Delete the losers
  for j, k in enumerate(results):
    if j == int(remove):
      break
    os.remove(folder + '/' + k[0])

  # Evaluate against all references of champions to stop
  if evaluate_all_refs(folder, results[-1][0]):
    print('Reference score obtained')
    break

  # Reproduct the best ones
  reproduct(folder, childs)

  # Mutate some childs
  mutate(folder)
  # Add some fresh generated
  for j in range(int(newbies)):
    generate_random(folder)

  print('Epoch', i, 'computed in', time.time() - epoch_time, 'seconds')
print('Training computed in', time.time() - init_time, 'seconds')
print('Champion generated:', results[-1][0])
