import xlrd
import csv

def antenna_classify (list_of_homes, list_of_antenna_locations):
    # RESULT = ['apple','cherry','orange','pineapple','strawberry']
    # RESULT1 = ['a', 'b', 'c', 'd', 'e']
    homes_path = '/Users/sumukhshivakumar/Desktop/vzhack/houseList.xlsx'
    antennas_path = '/Users/sumukhshivakumar/Desktop/vzhack/antennaLocations.xlsx'

    #Clears previous output
    open('output.csv', 'w').close()

    # homes = open(list_of_homes, 'r')
    # antennas = open(list_of_antenna_locations, 'r')
    homes_sheet = xlrd.open_workbook(homes_path).sheet_by_index(0)
    antennas_sheet = xlrd.open_workbook(antennas_path).sheet_by_index(0)
    print("houseList has " + str(homes_sheet.nrows) + " rows and " + str(homes_sheet.ncols) + " columns")
    print("antennaLocations has " + str(antennas_sheet.nrows) + " rows and " + str(antennas_sheet.ncols) + " columns")

    with open("output.csv",'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        # wr.writerow(RESULT)
        # wr.writerow(RESULT1)


antenna_classify('houseList.xlsx', 'antennaLocations.xlsx')
