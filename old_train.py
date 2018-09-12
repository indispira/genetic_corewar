import os
import time
import shutil

from mutation import mutate
from reproduction import reproduct
from generate import generate_random
from evaluate import evaluate_active, evaluate_reference

size_pop = 100
epochs = 200

newbies = 0.1 * size_pop
remove = 0.7 * size_pop
childs = 0.3 * size_pop

# Initialization
init_time = time.time()
step = 0
folder = 'pops/pop0'
os.mkdir(folder)
for i in range(size_pop):
# for i in range(5):
  # generate_random(folder)
  while generate_random(folder) is False:
    pass
print('First generation created')

# Loop for training
for i in range(epochs):
  epoch_time = time.time()
  folder = 'pops/pop' + str(i)
  # Transfer of the population
  if i != 0:
    shutil.copytree('pops/pop' + str(i - 1), folder)
  # Evaluate the population
  results = evaluate_reference(folder)
  # Delete the losers
  for j, k in enumerate(results):
    if j == int(remove):
      break
    os.remove(folder + '/' + k[0])
  # Evaluate against references to stop
  # if evaluate_reference(folder):
  #   print('Reference score obtained')
  #   break
  # Reproduct the best ones
  reproduct(folder, childs)
  # Mutate some of newbies
  mutate(folder)
  # Add some fresh generated
  for j in range(int(newbies)):
    while generate_random(folder) is False:
      pass
  print('Epoch', i, 'computed in', time.time() - epoch_time, 'seconds')

print('Training computed in', time.time() - init_time, 'seconds')
