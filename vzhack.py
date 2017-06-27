import xlrd
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
import math
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def antenna_classify ():
    homes_path = 'houseList.xlsx'
    antennas_path = 'antennaLocations.xlsx'

    number_clusters = 50 #50 has been best

    #Clears previous output
    open('output.csv', 'w').close()

    homes_sheet = xlrd.open_workbook(homes_path).sheet_by_index(0)
    antennas_sheet = xlrd.open_workbook(antennas_path).sheet_by_index(0)
    # print("houseList has " + str(homes_sheet.nrows) + " rows and " + str(homes_sheet.ncols) + " columns.")
    # print("antennaLocations has " + str(antennas_sheet.nrows) + " rows and " + str(antennas_sheet.ncols) + " columns.")

    # for row in range(1, homes_sheet.nrows):
    #         print("code: " + str(homes_sheet.cell_value(row, 0)) + " addr: " + str(homes_sheet.cell_value(row, 1)) + " LAT: " + str(homes_sheet.cell_value(row, 2)) + " LONG: " + str(homes_sheet.cell_value(row, 3)))


    house_array = []

    for row in range(1, homes_sheet.nrows):
        array_tuple = [homes_sheet.cell_value(row, 2), homes_sheet.cell_value(row, 3)]
        house_array.append(array_tuple)

    # print(house_array)
    # print(len(house_array))

    X = np.array(house_array)
    kmeans = KMeans(n_clusters=number_clusters)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    # print(centroids)
    # print(labels)


    colors = ["g.","r.","c.","y.", "k.", "b."] * 500

    labeled_points = [[] for i in range(number_clusters)]


    for i in range(len(X)):
        # print("coordinate:",X[i], "label:", labels[i])
        labeled_points[labels[i]].append(X[i])

        # #LONG AND LAT BACKWARDS ON EXCEL
        # dist = haversine((centroids[labels[i]][1]),[labels[i]][0],X[i][1],X[i][0])
        # # dist = math.sqrt((centroids[labels[i]][0]-X[i][0])**2 +(centroids[labels[i]][1]-X[i][1])**2)
        # distances_from_centroid[labels[i]].append(dist)

        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)


    distances_from_centroid = [[] for i in range(number_clusters)]
    index = 0
    for clus in labeled_points:
        for point in clus:
            # dist = sqrt((point[1] - centroids[index][1])**2 + (point[0] - centroids[index][0])**2)
            dist = haversine(point[1], point[0], centroids[index][1], centroids[index][0]) ###IN KM
            dist_ft = dist * 3280.84
            # print(dist)
            # print(dist_ft)
            distances_from_centroid[index].append(dist_ft)
        index += 1
            # print (point)
            # print(len(clus))
            # print(len(labeled_points[0])+len(labeled_points[1])+len(labeled_points[2])+len(labeled_points[3]))


        #LONG AND LAT BACKWARDS ON EXCEL
        # dist = haversine((centroids[labels[i]][1]),centroids[labels[i]][0],l[i][1],X[i][0])
        # dist = math.sqrt((centroids[labels[i]][0]-X[i][0])**2 +(centroids[labels[i]][1]-X[i][1])**2)
        # distances_from_centroid[labels[i]].append(dist)



    # print(labeled_points)
    # print(len(labeled_points))
    # print(type(labeled_points[0]))
    # print(type(centroids))
    # print(type(X))
    # print(distances_from_centroid)

    below = 0
    above = 0

    for x in distances_from_centroid:
        maxim = max(x)
        if maxim < 500:
            below += 1
        elif maxim > 500:
            above += 1
        # print(maxim)
    # print(min(distances_from_centroid[0]))
    # print(below)
    # print(above)


    antenna_array = []

    for row in range(1, antennas_sheet.nrows):
        array_tuple = [antennas_sheet.cell_value(row, 0), antennas_sheet.cell_value(row, 1), antennas_sheet.cell_value(row, 2), antennas_sheet.cell_value(row, 3)]
        antenna_array.append(array_tuple)

    print(len(antenna_array))
    print(len(centroids))


    antennas_final = []
    index_antenna = 0
    for cent in centroids:
        temp_best = []
        for point in antenna_array:
            antenna_type = ""
            dist = sqrt((cent[0] - point[2])**2 + (cent[1] - point[3])**2)
            if max(distances_from_centroid[index_antenna]) <= 100:
                antenna_type = "T-1"
            elif max(distances_from_centroid[index_antenna]) <= 200 and max(distances_from_centroid[index_antenna]) > 100:
                antenna_type = "T-2"
            elif max(distances_from_centroid[index_antenna]) <= 300 and max(distances_from_centroid[index_antenna]) > 200:
                antenna_type = "T-3"
            elif max(distances_from_centroid[index_antenna]) <= 400 and max(distances_from_centroid[index_antenna]) > 300:
                antenna_type = "T-4"
            else:
                antenna_type = "T-5"
            if (temp_best == []):
                temp_best = [point, antenna_type]
            elif (dist) < sqrt((temp_best[0][2] - cent[0])**2 + (temp_best[0][3] - cent[1])**2):
                temp_best = [point, antenna_type]

        antennas_final.append(temp_best)
        index_antenna += 1




    print(antennas_final)
    print(len(antennas_final))

    plt.scatter(centroids[:, 0],centroids[:, 1], marker = "x", s=150, linewidths = 5, zorder = 10)
    plt.show()



    with open("output.csv",'w') as resultFile:
        wr = csv.writer(resultFile, delimiter = ",")
        wr.writerow(['AntennaLocationCode', 'AntennaType'])
        for elem in antennas_final:
            wr.writerow([elem[0][0], elem[1]])

antenna_classify()
