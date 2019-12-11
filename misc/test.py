import random
f = {}  # dict containing name:group
for i, line in enumerate(open("names.txt", "r").readlines()):
    group = line.strip().split(" ")
    f.update({p: i for p in group})
names = list(f.keys())

while True:
    random.shuffle(names)
    assignments = {a: b for a, b in zip(names, names[1:] + [names[0]])}
    if all([f[a] != f[b] for a, b in assignments.items()]):
        break
for a, b in assignments.items():
    print("{} ({}) -> {} ({})".format(a, f[a], b, f[b]))
