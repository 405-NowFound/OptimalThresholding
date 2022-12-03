import csv
import operator
from itertools import combinations, permutations
import math
import os
from datetime import datetime
import json
import time

class csvParser:
    """
    This class is an abstract representation for informations offered in a .csv file.

    This contains functionalities for:
    - parsing the .csv file
    - saving relevant data
    """
    tresholdings = [] # list of lists 
    pixelClass = []
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
        for i in range(0, 3):
            self.plusList.append("+")
            self.minusList.append("-")
            self.multiplyList.append("*")
            self.divideList.append("/")

    def readCSV(self, inputFile):
        with open(inputFile, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            for row in reader:
                self.tresholdings.append(row[2:])
                self.pixelClass.append(row[1])
        return 0


class Binarization:

    def __init__(self):
        self.parser = csvParser() # .csv file parser
        self.pixelClass = 0 # the value of the pixel class
        self.valuesTh = [] # values of all tresholds
        self.combPercentage = dict() # dict of all comb
        self.allCombinations = []

    def generateCombinations(self):
        operatorsList = self.parser.plusList + self.parser.minusList + self.parser.multiplyList + self.parser.divideList

        comb1 = list(set(list(combinations(operatorsList, 3))))
        comb2 = list(set(list(combinations(operatorsList, 3))))
        comb3 = list(set(list(combinations(operatorsList, 3))))

        return comb1, comb2, comb3

    def generateCombinationsList(self):
        allCombinations = []
        comb1, comb2, comb3 = self.generateCombinations()

        for e1 in comb1:
            for e2 in comb2:
                for e3 in comb3:
                    order = e1 + e2 + e3
                    nrPlus = order.count("+")
                    nrMinus = order.count("-")
                    nrDiv = order.count("/")
                    nrMul = order.count("*")

                    if (abs(nrPlus - nrMinus) == 0 and abs(nrMul - nrDiv) <= 1) or (abs(nrPlus - nrMinus) <= 1 and abs(nrMul - nrDiv) == 0):
                        allCombinations.append(order)

        return allCombinations

    def findSolutionForOneFile(self, inputFile):
        self.parser.readCSV(inputFile)
        self.valuesTh = self.parser.tresholdings
        self.pixelClass = self.parser.pixelClass

        for order in self.allCombinations:
            succes = 0
            for i in range(len(self.valuesTh)):
                pixelClass = self.pixelClass[i]
                result = float(self.valuesTh[i][0])
                for j in range(1, len(self.valuesTh[i])):
                    result = self.parser.operationMap[order[j - 1]](result, float(self.valuesTh[i][j]))

                if result >= 0 and result < 0.5:
                    if int(pixelClass) == 0:
                        succes += 1
                if result >= 0.5 and result <= 1:
                    if int(pixelClass) == 1:
                        succes += 1

            percent = float(succes) / len(self.valuesTh)
            self.combPercentage["".join(order)] = percent

            if "".join(order) in self.combPercentage.keys():
                self.combPercentage["".join(order)] = (self.combPercentage["".join(order)] + percent) / 2
            else:
                self.combPercentage["".join(order)] = percent

class LocalSolver:

    def __init__(self):
        self.binarization = Binarization()

    def localTrain(self):
        inputPath = os.getcwd() + '/tests/local/train'
        dir_list = os.listdir(inputPath)

        self.binarization.allCombinations = self.binarization.generateCombinationsList()
        

        idx = 0        
        for inFile in dir_list:
            idx += 1
            print(inFile + "...")
            inputFilePath = inputPath + '/' + str(inFile)
            self.binarization.findSolutionForOneFile(inputFilePath)

            jsonObj = json.dumps(self.binarization.combPercentage, indent=4)
            with open("localTrainResults.json", "w") as outfile:
                outfile.write(jsonObj)
            
            if idx == 1:
                break
        

def main():
    solver = LocalSolver()
    start_time = time.time()
    solver.localTrain()
    print(time.time() - start_time)
   
#    solver.binarization.combPercentage


if __name__ == "__main__":
    main()


# print(reader.plusList)
#     # reader.readCSV("tests/local/test/[S-MS]z92-F1s.CSV")

#     # print(len(reader.pixelClass))
#     # print(len(reader.tresholdings))
