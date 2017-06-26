import xlrd
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans

def antenna_classify ():
    homes_path = 'houseList.xlsx'
    antennas_path = 'antennaLocations.xlsx'

    #Clears previous output
    open('output.csv', 'w').close()

    homes_sheet = xlrd.open_workbook(homes_path).sheet_by_index(0)
    antennas_sheet = xlrd.open_workbook(antennas_path).sheet_by_index(0)
    print("houseList has " + str(homes_sheet.nrows) + " rows and " + str(homes_sheet.ncols) + " columns.")
    print("antennaLocations has " + str(antennas_sheet.nrows) + " rows and " + str(antennas_sheet.ncols) + " columns.")

    for row in range(1, homes_sheet.nrows):
            print("code: " + str(homes_sheet.cell_value(row, 0)) + " addr: " + str(homes_sheet.cell_value(row, 1)) + " LAT: " + str(homes_sheet.cell_value(row, 2)) + " LONG: " + str(homes_sheet.cell_value(row, 3)))


    house_array = []

    for row in range(1, homes_sheet.nrows):
        array_tuple = [homes_sheet.cell_value(row, 2), homes_sheet.cell_value(row, 3)]
        house_array.append(array_tuple)

    # print(house_array)
    # print(len(house_array))

    X = np.array(house_array)
    kmeans = KMeans(n_clusters=4)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    print(centroids)
    print(labels)


    colors = ["g.","r.","c.","y."]

    for i in range(len(X)):
        print("coordinate:",X[i], "label:", labels[i])
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)

    plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)
    plt.show()

    with open("output.csv",'w') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        # wr.writerow(RESULT)
        # wr.writerow(RESULT1)


antenna_classify()
