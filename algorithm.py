import data as dt
import cost_functions
import mutation
from copy import deepcopy


#conn = dt.psycopg2.connect("dbname= user= password=")
max_generations = 600
iterations = 1
input_file = 'example/example_classes.json'
output_file = 'example/example_classes_output.json'
cost_function = cost_functions.cost


def algorithm():
    result = None
    data = dt.load_data(input_file)
    #data = dt.load_data_from_db(conn)
    for i in range(iterations):
        chromosome = dt.generate_chromosome(data)

        for j in range(max_generations):
            new_chromosome = mutation.successor(deepcopy(chromosome))
            fit = cost_function(chromosome)
            if fit == 0:
                break
            new_fit = cost_function(new_chromosome)
            if new_fit <= fit:
                chromosome = new_chromosome
            if j % 10 == 0:
                print('Iteration', j, 'cost', cost_function(chromosome))

        print('Run', i + 1, 'cost:', cost_function(chromosome))

        if result is None or cost_function(chromosome) <= cost_function(result):
            result = deepcopy(chromosome)

    chromosome = result
    
    dt.write_data(chromosome[0], output_file)
    #dt.write_data_to_db(chromosome[0], conn)
   

algorithm()