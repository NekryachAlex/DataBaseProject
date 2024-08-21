import random

def successor(chromosome):
    candidates = []
    for k in range(len(chromosome[0])):
        for j in range(len(chromosome[2][chromosome[0][k]['Appointed_class']])):
            if chromosome[2][chromosome[0][k]['Appointed_class']][j] >= 2:
                candidates.append(k)
        for j in range(len(chromosome[1][chromosome[0][k]['Teacher']])):
            if chromosome[1][chromosome[0][k]['Teacher']][j] >= 2:
                candidates.append(k)
        for group in chromosome[0][k]['Group']:
            for j in range(len(chromosome[3][group])):
                if chromosome[3][group][j] >= 2:
                    candidates.append(k)

    if not candidates:
        i = random.randrange(len(chromosome[0]))
    else:
        i = random.choice(candidates)

    
    for j in range(chromosome[0][i]['Appointed_time'], chromosome[0][i]['Appointed_time'] + int(chromosome[0][i]['Duration'])):
        chromosome[1][chromosome[0][i]['Teacher']][j] -= 1
        chromosome[2][chromosome[0][i]['Appointed_class']][j] -= 1
        for group in chromosome[0][i]['Group']:
            chromosome[3][group][j] -= 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].remove((chromosome[0][i]['Appointed_time'], chromosome[0][i]['Group']))

    
    length = int(chromosome[0][i]['Duration'])
    found = False
    pairs = []
    for classroom in chromosome[2]:
        c = 0
        if classroom not in chromosome[0][i]['Classroom']:
            continue
        for k in range(len(chromosome[2][classroom])):
            if chromosome[2][classroom][k] == 0 and k % 12 + length  <= 12: 
                c += 1
                
                if c == length:
                    time = k + 1 - c
                    
                    pairs.append((time, classroom))
                    found = True
                    c = 0
            else:
                c = 0
    if not found:
        classroom = random.choice(chromosome[0][i]['Classroom'])
        day = random.randrange(0, 5)
      
        period = random.randrange(0, 13 - int(chromosome[0][i]['Duration']))
        time = 12 * day + period

        chromosome[0][i]['Appointed_class'] = classroom
        chromosome[0][i]['Appointed_time'] = time

    if found:
        candidate = random.choice(pairs)
        chromosome[0][i]['Appointed_class'] = candidate[1]
        chromosome[0][i]['Appointed_time'] = candidate[0]

    for j in range(chromosome[0][i]['Appointed_time'], chromosome[0][i]['Appointed_time'] + int(chromosome[0][i]['Duration'])):
        chromosome[1][chromosome[0][i]['Teacher']][j] += 1
        chromosome[2][chromosome[0][i]['Appointed_class']][j] += 1
        for group in chromosome[0][i]['Group']:
            chromosome[3][group][j] += 1
    chromosome[4][chromosome[0][i]['Subject']][chromosome[0][i]['Type']].append((chromosome[0][i]['Appointed_time'], chromosome[0][i]['Group']))

    return chromosome

