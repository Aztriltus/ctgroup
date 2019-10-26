# 
# <Team members' names>
import numpy as np
import csv
from sklearn.cluster import AgglomerativeClustering

def list_reader(csv_file):
    the_list = []
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            the_list.append(row)
    return the_list

# replace the content of this function with your own algorithm
def schedule_q1(orders=None, number_trucks=25):
  orders = list_reader('./orders.csv')
  d = {}
  for order in orders:
    d[order[0]] = [order[1],order[2]]
  data = list(d.values())
  X = np.array(data)
  cluster = AgglomerativeClustering(n_clusters=number_trucks, affinity='euclidean', linkage='ward')
  cluster.fit_predict(X)
  print(cluster.labels_)
	#return truck_paths
  return

schedule_q1()





##########################sorting of the distance#########################
orders = [['O001', 5.5, 3.4], ['O002', -10.0, -8.9], ['O003', -1.9, -5.6]] 
number_trucks = 5
def schedule_q1(orders, number_trucks):
    distance_list = {}

    for orderA in orders:
#         distance = ((orderA[1] - 0 )**2 + (orderA[2] - 0)**2)** 0.5
#         distance  = round(distance, 5)
#         distance_list['Origin' + '-' + orderA[0]] = distance

        for orderB in orders:
            if orderA[0] != orderB[0]:
                distance = ((orderA[1] - orderB[1])**2 + (orderA[2] - orderB[2])**2)** 0.5
                distance  = round(distance, 5)
                distance_list[orderA[0] + '-' + orderB[0]] = distance
                

    for distanceA in distance_list.copy().keys():
        for distanceB in distance_list.copy().keys():
            if distanceA.split('-') == distanceB.split('-')[::-1]:
                distance_list.pop(distanceA)
    distance_list = sorted(distance_list.items(), key=lambda x: x[1])
    
    print(distance_list)
    
    
    
    
    import random 
    route = []
    for truck_no in range(number_trucks):
        number_truck = []
        
        number_truck.append 
#     return(distance_list)       