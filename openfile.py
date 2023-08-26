with open("absolventen.txt", 'r') as f:
    lines = [line.rstrip() for line in f]

print(list(lines))