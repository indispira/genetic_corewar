import os

ops = ['live', 'lldi', 'ldi', 'lld', 'ld', 'lfork', 'sti', 'st',
      'add', 'sub', 'and', 'xor', 'fork', 'or', 'zjmp']

instructions = [0 for i in range(len(ops))]
champs = os.listdir('sources')
for c in champs:
  with open('sources/' + c) as f:
    data = f.read().split('\n')

    for d in data:
      for i, o in enumerate(ops):
        if o in d:
          instructions[i] += 1
          break

for i, o in zip(instructions, ops):
  print(i, o)
