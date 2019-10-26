# Team ID??
# Jiang Jia Xing, Ng Zheng Hao, Ong Soon Heng
import numpy as np
import csv
from sklearn.cluster import AgglomerativeClustering

# Reads CSV 
# Remove when submitting
def list_reader(csv_file):
    the_list = []
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            the_list.append(row)
    return the_list

#
#
# Algorithm main method here
#
#
def schedule_q1(orders=None, number_trucks=25):
  # add in orders next time
  d = cluster(25)
  tsp(d[0]) 
  return

#
#
# Returns dictionary 
# Key=group_number and value='array of orders'
#
#
def cluster(number_trucks, orders=None):
  # use orders argument next time
  orders = list_reader('./orders.csv')

  # Grab only the coordinates
  array = []
  for order in orders:
    array.append([order[1],order[2]])

  # Convert into numpy array
  X = np.array(array)

  # Find clusters using sklearn
  cluster = AgglomerativeClustering(n_clusters=number_trucks, affinity='euclidean', linkage='ward')
  cluster.fit_predict(X)

  # Create dictionary with
  # key=group_no and value='array of orders' 
  d = {}
  index = 0
  for group_no in cluster.labels_:
    order = orders[index]
    if group_no in d:
      d[group_no].append(order)
    else:
      d[group_no] = [order]
    index += 1

  return d

# 
#
# Accepts an array of orders 
# Returns optimised route 
#
#
def tsp(orders):
    distance_list = {}
    print(orders)

    for orderA in orders:
#         distance = ((orderA[1] - 0 )**2 + (orderA[2] - 0)**2)** 0.5
#         distance  = round(distance, 5)
#         distance_list['Origin' + '-' + orderA[0]] = distance

        for orderB in orders:
            if orderA[0] != orderB[0]:
                ax, ay = float(orderA[1]), float(orderA[2])
                bx, by = float(orderB[1]), float(orderB[2])

                distance = ((ax - bx)**2 + (ay - by)**2)** 0.5
                distance  = round(distance, 5)
                distance_list[orderA[0] + '-' + orderB[0]] = distance
                

    for distanceA in distance_list.copy().keys():
        for distanceB in distance_list.copy().keys():
            if distanceA.split('-') == distanceB.split('-')[::-1]:
                distance_list.pop(distanceA)
    distance_list = sorted(distance_list.items(), key=lambda x: x[1])
    
    print()
    print(distance_list)
    
    # import random 
    # route = []
    # for truck_no in range(number_trucks):
    #     number_truck = []
        
    #     number_truck.append 
#     return(distance_list)       

schedule_q1()