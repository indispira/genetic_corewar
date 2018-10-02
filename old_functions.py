
def load_parents(folder):
  files = os.listdir(folder)
  parents = []
  for p in files:
    with open('newbies/' + p[:-3] + 's', 'r') as f:
      parents.append(f.read().split('\n')[3:-1])
  return parents

def reproduct(folder, nb):
  parents = load_parents(folder)

  for i in range(int(nb)):
    name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))

    # Generate the .s file
    with open('childs/' + name + '.s', 'w') as f:
      # The minimum for a champion: name, comment and 1 operation
      f.write('.name "%s"\n.comment ""\n\n' % name)
      
      half = int(len(parents[i]) / 2)
      for j in range(half):
        f.write(parents[i][j] + '\n')
      half = int(len(parents[(i + 1) % len(parents)]) / 2)
      for j in range(half):
        f.write(parents[(i + 1) % len(parents)][j + half] + '\n')

def generate_child(folder, father, mother):
  start = father[:int(len(father) / 2)]
  end = mother[int(len(mother) / 2):]
  while len(start) + len(end) < 60:
    start.append(father[random.randint(int(len(father) / 2), len(father) - 1)])
    end.append(mother[random.randint(0, int(len(mother) / 2))])

  # Mutate the child ?
  if random.randint(0, 20) == 0:
    start, end = mutate_v2(start, end)

  # Generate the .s file
  name = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=40))
  with open('childs/' + name + '.s', 'w') as f:
    # The minimum for a champion: name, comment and 1 operation
    f.write('.name "%s"\n.comment ""\n\n' % name)
    for l in start:
      f.write(l + '\n')
    for l in end:
      f.write(l + '\n')

def launch_evaluation(p1, p2):
  cmd = './corewar ' + p1 + ' ' + p2
  args = shlex.split(cmd)
  res = subprocess.Popen(args, stdout=PIPE)
  return res.communicate()[0].decode('utf-8').splitlines()

def launch_evaluation_scores(p1, p2):
  cmd = './corewar -v 2 ' + p1 + ' ' + p2
  args = shlex.split(cmd)
  res = subprocess.Popen(args, stdout=PIPE)
  return res.communicate()[0].decode('utf-8').splitlines()

def evaluate_inside_folder(folder):
  pop, scores = get_population(folder)  
  before = time.time()
  for i, p in enumerate(pop):
    p1 = folder + '/' + p
    j = i + 1
    while j < len(pop):
      p2 = folder + '/' + pop[j] 
      res = launch_evaluation(p1, p2)
      if res[-1][11] == '1':
        scores[p1[len(folder) + 1:]] += 1
      else:
        scores[p2[len(folder) + 1:]] += 1
      j += 1

  scores = [(k, scores[k]) for k in sorted(scores, key=scores.get)]
  print('Evaluations of active population done in', time.time() - before, 'seconds')
  return scores

def evaluate_one_vs_stock(folder, name):
  score = 0
  ref, _ = get_population('stock')
  before = time.time()
  p1 = folder + '/' + name
  for r in ref:
    p2 = 'stock/' + r
    res = launch_evaluation_timeout(p1, p2, 5)
    if len(res) and res[-1][11] == '1':
      score += 1

  print('Evaluations against the stock done in', time.time() - before, 'seconds')
  print('The Score of the actual champion is', score)

  if score == len(ref):
    return True
  return False

def evaluate_test(name):
  res = launch_evaluation('test/' + name + '.cor', 'base.cor')
  if res[-1][11] == '1':
    return True
  return False

def each_pool(folder, pop, remove):
  # Each champion fight against each reference
  scores = {p: 0 for p in pop}
  ref, _ = get_population('refs')
  for p in pop:
    p1 = folder + '/' + p
    for r in ref:
      p2 = 'refs/' + r
      res = launch_evaluation_timeout(p1, p2, 5)
      if len(res) and res[-1][11] == '1':
        scores[p] += 1

  # Sort the scores and delete the losers
  scores = [(k, scores[k]) for k in sorted(scores, key=scores.get)]
  for i in range(remove):
    os.remove(folder + '/' + scores[i][0])

def pool(pools, folder, remove):
  pop = os.listdir(folder)
  batch = len(pop) / pools
  processes = []
  for i in range(pools):
    p = Process(target=each_pool, args=(folder, pop[int(i * batch):int((i + 1) * batch)], remove,))
    processes.append(p)
    p.start()

  for p in processes:
    p.join()

def evaluate_cycles(folder):
  pop, scores = get_population(folder)
  ref, _ = get_population('refs')
  before = time.time()
  for p in pop:
    p1 = folder + '/' + p
    for r in ref:
      p2 = 'refs/' + r
      res = launch_evaluation_scores(p1, p2)
      if res[-1][11] == '1':
        scores[p1[len(folder) + 1:]] += 1000000
      else:
        text = res[-2].split(' ')
        scores[p1[len(folder) + 1:]] += int(text[-1])

  scores = [(k, scores[k]) for k in sorted(scores, key=scores.get)]
  print('Evaluations against reference done in', time.time() - before, 'seconds')

  print(scores[-10:])
  # for k in scores:
  #   print(k)
  return scores

def evaluate_reference(folder):
  pop, scores = get_population(folder)
  ref, _ = get_population('refs')
  before = time.time()
  for p in pop:
    p1 = folder + '/' + p
    for r in ref:
      p2 = 'refs/' + r
      res = launch_evaluation(p1, p2)
      if res[-1][11] == '1':
        scores[p1[len(folder) + 1:]] += 1

  scores = [(k, scores[k]) for k in sorted(scores, key=scores.get)]
  print('Evaluations against reference done in', time.time() - before, 'seconds')

  print(scores[-10:])
  # for k in scores:
  #   print(k)
  return scores

def each_stock(folder, pop, scores):
  stk, _ = get_population('stock')
  for p in pop:
    scores[p] = 0
    p1 = folder + '/' + p
    for s in stk:
      p2 = 'stock/' + s
      res = launch_evaluation_timeout(p1, p2, 5)
      if len(res) and res[-1][11] == '1':
        scores[p] += 1

def evaluate_stock(folder, pools, remove=0):
  pop, scores = get_population(folder)
  ref, _ = get_population('stock')
  batch = len(pop) / pools
  processes = []
  with Manager() as manager:
    scores = manager.dict()
    before = time.time()
    for i in range(pools):
      p = Process(target=each_stock, args=(folder, pop[int(i * batch):int((i + 1) * batch)], scores,))
      processes.append(p)
      p.start()

    for p in processes:
      p.join()

    result = sorted([(k, v) for k, v in scores.items()], key=lambda x: x[1])
  # print('Evaluations against all stock done in', time.time() - before, 'seconds')

  # If no pool selection, remove the losers
  if remove:
    for i in range(remove):
      os.remove(folder + '/' + result[i][0])

  result = result[remove:]
  # print(result[-10:])
  return result

def eval_cycles(p1, p2, timeout=3600):
  cmd = './corewar -v 2 ' + p1 + ' ' + p2
  res = subprocess.Popen(shlex.split(cmd), stdout=PIPE)
  timer = Timer(timeout, res.kill)
  try:
    timer.start()
    result = res.communicate()[0].decode('utf-8').splitlines()
  finally:
    timer.cancel()
    return result

def eval_victory(p1, p2, timeout=3600):
  cmd = './corewar ' + p1 + ' ' + p2
  res = subprocess.Popen(shlex.split(cmd), stdout=PIPE)
  timer = Timer(timeout, res.kill)
  try:
    timer.start()
    result = res.communicate()[0].decode('utf-8').splitlines()
  finally:
    timer.cancel()
    return result
