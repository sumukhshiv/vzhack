import xlrd
import csv

def antenna_classify ():
    homes_path = '/Users/sumukhshivakumar/Desktop/vzhack/houseList.xlsx'
    antennas_path = '/Users/sumukhshivakumar/Desktop/vzhack/antennaLocations.xlsx'

    #Clears previous output
    open('output.csv', 'w').close()

    homes_sheet = xlrd.open_workbook(homes_path).sheet_by_index(0)
    antennas_sheet = xlrd.open_workbook(antennas_path).sheet_by_index(0)
    print("houseList has " + str(homes_sheet.nrows) + " rows and " + str(homes_sheet.ncols) + " columns.")
    print("antennaLocations has " + str(antennas_sheet.nrows) + " rows and " + str(antennas_sheet.ncols) + " columns.")

    for row in range(1, homes_sheet.nrows):
            print("code: " + str(homes_sheet.cell_value(row, 0)) + " addr: " + str(homes_sheet.cell_value(row, 1)) + " LAT: " + str(homes_sheet.cell_value(row, 2)) + " LONG: " + str(homes_sheet.cell_value(row, 3)))

    with open("output.csv",'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        # wr.writerow(RESULT)
        # wr.writerow(RESULT1)


antenna_classify()
