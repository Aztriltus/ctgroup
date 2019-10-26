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
# Main method here
# type either 'python q1.py' or 'python3 q1.py' to run this function
#
#
def schedule_q1(orders=None, number_trucks=25):
  # Remove this line when submitting
  orders = list_reader('./orders.csv')

  # Get clusters (dict)
  # Need to change to a better clustering algo
  d = cluster(orders, number_trucks)

  # Testing with first group of clusters
  all_distances = distances(d[0]) 
  
  # Grab the order with the smallest distance from origin
  min_from_origin = min(all_distances['origin'], key=lambda k: all_distances['origin'][k])
  # Get another order with shortest distance from either origin or min_from_origin
  # Insert it into an array (that is sorted to determine the sequence of delivery)
  # Repeat until all orders are in the array
  # and return the array

  return

#
#
# Returns dictionary 
# Key=group_number and value='array of orders'
#
#
def cluster(orders, number_trucks):

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
# Returns dictionary that has the same length as orders
# Key='order id' and value = dict('other order id': distance from original key)
# Modified from tsp function written by JX
#
#
def distances(orders):
    distance_list = {}
    print(orders)

    for orderA in orders:
#         distance = ((orderA[1] - 0 )**2 + (orderA[2] - 0)**2)** 0.5
#         distance  = round(distance, 5)
#         distance_list['Origin' + '-' + orderA[0]] = distance

        for orderB in orders:
            if orderA[0] != orderB[0]:
                # Convert coordinates from String back to Float
                ax, ay = float(orderA[1]), float(orderA[2])
                bx, by = float(orderB[1]), float(orderB[2])

                # Calculate distance
                distance = ((ax - bx)**2 + (ay - by)**2)** 0.5
                distance  = round(distance, 5)

                # For each order, find the distance
                if orderA[0] in distance_list:
                  d_in_d = distance_list[orderA[0]]
                  d_in_d[orderB[0]] = distance
                else:
                  d_in_d = {orderB[0]: distance}
                  distance_list[orderA[0]] = d_in_d

        # Added this to include distance between origin and all other orders
        distance = ((0 - ax)**2 + (0 - ay)**2)** 0.5
        distance  = round(distance, 5)
        if 'origin' in distance_list:
          d_in_d = distance_list['origin']
          d_in_d[orderA[0]] = distance
        else: 
          d_in_d = {orderA[0]: distance}
          distance_list['origin'] = d_in_d

    return distance_list  

# 
#
# Accepts an array of orders 
# Returns distance of pairs that is sorted in asc 
# Written by JX
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
        distance = ((0 - ax)**2 + (0 - ay)**2)** 0.5
        distance  = round(distance, 5)
        distance_list['origin-' + orderA[0]] = distance

                
    # Added this to include distance between origin and all other orders
    for distanceA in distance_list.copy().keys():
        for distanceB in distance_list.copy().keys():
            if distanceA.split('-') == distanceB.split('-')[::-1]:
                distance_list.pop(distanceA)
    distance_list = sorted(distance_list.items(), key=lambda x: x[1])
    
    print()
    print(distance_list)
    return distance_list

schedule_q1()