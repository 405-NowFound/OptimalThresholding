import csv
import operator
from itertools import combinations, permutations
import math

class csvParser:
    """
    This class is an abstract representation for informations offered in a .csv file.

    This contains functionalities for:
    - parsing the .csv file
    - saving relevant data
    """
    tresholdings = [] # values for thresholdings obtained from different algorithms
    fMeasures = [] # list of percentages
    plusList = [] # a list with "+"
    minusList = [] # a list with "-"
    multiplyList = [] # a list with "*"
    divideList = [] # a list with "/"
    operationMap = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    } # a dictionary with all the possible operators

    def __init__(self):
        for i in range(0, 4):
            self.plusList.append("+")
            self.minusList.append("-")
            self.multiplyList.append("*")
            self.divideList.append("/")

    def readCSV(self, inputFile):
        with open(inputFile, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            csv_info = []

            for row in reader:
                csv_info.append(row)

            self.tresholdings = csv_info[0]
            self.fMeasures = csv_info[1]
        return 0

class Binarization:

    def __init__(self):
        self.parser = csvParser() # .csv file parser
        self.idealTh = 0 # the value of the ideal treshold
        self.valuesTh = [] # values of all tresholds
        self.goodCombinations = [] # list of combinations of operators which are more than 99.99%


    def generateCombinations(self):
        operatorsList = self.parser.plusList + self.parser.minusList + self.parser.multiplyList + self.parser.divideList

        comb1 = list(set(list(combinations(operatorsList, 4))))
        comb2 = list(set(list(combinations(operatorsList, 4))))
        comb3 = list(set(list(combinations(operatorsList, 4))))
        comb4 = list(set(list(combinations(operatorsList, 2))))

        return comb1, comb2, comb3, comb4

    def computeResult(self, order, result):
        for i in range(1, len(self.valuesTh)):
            result = self.parser.operationMap[order[i - 1]](result, float(self.valuesTh[i]))
            if result <= 1 and result > 0:
                index = math.floor(result * 255)
                if float(self.parser.fMeasures[index]) > 99.99:
                    self.goodCombinations.append(order)

    def findSolutions(self, inputFile):
        self.parser.readCSV(inputFile)
        self.idealTh = self.parser.tresholdings[0]
        self.valuesTh = self.parser.tresholdings[1:15]

        result = 0
        if self.goodCombinations == []:
            comb1, comb2, comb3, comb4 = self.generateCombinations()

            for e1 in comb1:
                for e2 in comb2:
                    for e3 in comb3:
                        for e4 in comb4:
                            order = e1 + e2 + e3 + e4
                            result = float(self.valuesTh[0])
                            self.computeResult(order, result)
            
        else:
            for order in self.goodCombinations:
                result = float(self.valuesTh[0])
                self.computeResult(order, result)

        print(len(set(self.goodCombinations)))
        # self.printCombinations()

    def printCombinations(self):
        for combination in self.goodCombinations:
            print(combination)

def main():
    inputFile = '/workspaces/OptimalThresholding/Main implementation/tests/global.CSV'
    binarization = Binarization()
    binarization.findSolutions(inputFile)
  
if __name__ == "__main__":
    main()

    """
    TODO:
    - class for all input files for global
    - take the same idea for local
    - how to take as input all files from a folder
    https://stackoverflow.com/questions/18262293/how-to-open-every-file-in-a-folder
    """
