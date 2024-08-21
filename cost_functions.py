def basic_cost(chromosome):
    prof_cost = 0
    classrooms_cost = 0
    groups_cost = 0
    for single_class in chromosome[0]:
        time = single_class['Appointed_time']
        class_len = single_class['Duration']

        for i in range(time, time + int(class_len)):
            if chromosome[1][single_class['Teacher']][i] > 1:
                prof_cost += 1
            if chromosome[2][single_class['Appointed_class']][i] > 1:
                classrooms_cost += 1
            for group in single_class['Group']:
                if chromosome[3][group][i] > 1:
                    groups_cost += 1
    return prof_cost + classrooms_cost + groups_cost 

def cost(chromosome):

    groups_empty = 0
    prof_empty = 0
    load_groups = 0
    load_prof = 0
    subjects_cost = 0

    basic_cost_result = basic_cost(chromosome)

    for single_class in chromosome[4]:
            for lab in chromosome[4][single_class]['W']:
                for practice in chromosome[4][single_class]['S']:
                    for grupa in lab[1]:
                        if grupa in practice[1] and lab[0] < practice[0]: # If lab is before practical
                            subjects_cost += 0.1
                for lecture in chromosome[4][single_class]['L']:
                    for grupa in lab[1]:
                        if grupa in lecture[1] and lab[0] < lecture[0]: # If lab is before lecture
                            subjects_cost += 0.1
            for practice in chromosome[4][single_class]['S']:
                for lecture in chromosome[4][single_class]['L']:
                    for grupa in practice[1]:
                        if grupa in lecture[1] and practice[0] < lecture[0]: # If practical is before lecture
                            subjects_cost += 0.1


    for group in chromosome[3]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[3][group][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        groups_empty += time - last_seen - 1
                    last_seen = time
                   
            if current_load > 6:
                load_groups += 0.1

   
    for prof in chromosome[1]:
        for day in range(5):
            last_seen = 0
            found = False
            current_load = 0
            for hour in range(12):
                time = day * 12 + hour
                if chromosome[1][prof][time] >= 1:
                    current_load += 1
                    if not found:
                        found = True
                    else:
                        prof_empty += time - last_seen - 1
                        
                    last_seen = time
                    
            if current_load > 6:
                load_prof += 0.1

    return basic_cost_result + groups_empty + prof_empty + load_prof + load_groups + subjects_cost