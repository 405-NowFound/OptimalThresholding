import csv
import operator
from itertools import combinations, permutations
import math

def read_csv():
    with open('/workspaces/OptimalThresholding/Main implementation/tests/global.CSV', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        csv_info = []

        for row in reader:
            csv_info.append(row)

        optimalTresholdings = csv_info[0]
        fMeasures = csv_info[1]

    return optimalTresholdings,fMeasures

def main():
    operations_map = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }
    
    plus_list = []
    minus_list = []
    multiply_list = []
    divide_list = []

    optimalTresholdings, fMeasures = read_csv()
    ideal_th = optimalTresholdings[0]
    values_th = optimalTresholdings[1:15]

    for i in range(0, 4):
        plus_list.append("+")
        minus_list.append("-")
        multiply_list.append("*")
        divide_list.append("/")
    
    operators_list = plus_list + minus_list + multiply_list + divide_list
    
    comb1 = list(set(list(combinations(operators_list, 4))))
    comb2 = list(set(list(combinations(operators_list, 4))))
    comb3 = list(set(list(combinations(operators_list, 4))))
    comb4 = list(set(list(combinations(operators_list, 2))))

    interesting = []
    result = 0

    for e1 in comb1:
        for e2 in comb2:
            for e3 in comb3:
                for e4 in comb4:
                    order = e1 + e2 + e3 + e4
                    result = float(values_th[0])
                    for i in range(1, len(values_th)):
                        result = operations_map[order[i - 1]](result, float(values_th[i]))
                        if result <= 1 and result > 0:
                            index = math.floor(result * 255)
                            if float(fMeasures[index]) > 99.99:
                                interesting.append(order)
    
    print(len(set(interesting)))
  
if __name__ == "__main__":
    main()
