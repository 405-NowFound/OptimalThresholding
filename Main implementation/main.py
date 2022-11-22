import csv

def main():
    pass

if __name__ == "__main__":

    with open('/workspaces/OptimalThresholding/Main implementation/tests/global.CSV', 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        optimalTreshholdings = []
        for row in reader:
	        print(row[0])
	
