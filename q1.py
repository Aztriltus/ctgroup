# Team ID??
# Jiang Jia Xing, Ng Zheng Hao, Ong Soon Heng
import numpy as np
import csv
from sklearn.cluster import AgglomerativeClustering
from pandas import *
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
  # orders = list_reader('./orders.csv')

  # Get clusters (dict)
  # Need to change to a better clustering algo
  d = cluster(orders, number_trucks//6)

  # Find the best route per cluster
  # Uses greedy2
  total_tour = []
  for group in d.keys():
    total_tour.append(greedy2(d[group]))
  # print(total_tour)
  
  return total_tour

def getTotalDistanceFromTour(tour, original_orders):
  all_distances = distances(original_orders)
  total_distance = 0
  # print(all_distances)
  for i in range(len(tour)):
    next_i = (i + 1) if (i+1) < len(tour) else 0
    order_current = tour[i]
    order_next = tour[next_i]
    # print(order_current)
    # print(order_next)
    total_distance += all_distances[order_current][order_next]
  return total_distance

def greedy2(orders):
  all_distances = distances(orders) 
  all_distances_copy = all_distances.copy()

  # Variables for greedy 2
  tour = []

  # Grab the order with the smallest distance from origin and append to current tour 
  min_from_origin = min(all_distances_copy['origin'], key=lambda k: all_distances_copy['origin'][k])
  tour.append('origin')
  tour.append(min_from_origin)

  # Delete this order from both places - using key origin and using key min_from_origin
  del all_distances_copy['origin'][min_from_origin]
  del all_distances_copy[min_from_origin]['origin']

  while len(tour) <= len(orders):
    # Get order with shortest distance from any current tour order_ids
    next_destination = ''
    toured_city = ''
    toured_city_index = -1
    min_distance = 0
    index = 0
    for order in tour:
      id = min(all_distances_copy[order], key=lambda k: all_distances_copy[order][k])
      distance = all_distances_copy[order][id]
      if min_distance == 0:
        min_distance = distance
        next_destination = id
        toured_city_index = index
        toured_city = order
      elif min_distance > 0 and distance < min_distance:
        min_distance = distance
        next_destination = id
        toured_city_index = index
        toured_city = order
      index += 1

    # print("Toured City: " + toured_city)
    # print("Next Destination: " + next_destination)
    # Find the best place to insert the next destination (either left or right of toured_city)
    tourA = tour.copy()
    tourB = tour.copy()
    tourA.insert(toured_city_index, next_destination)
    # print("Tour A: " + str(tourA))
    tourB.insert(toured_city_index + 1, next_destination)
    # print("Tour B: " + str(tourB))
    distanceA = getTotalDistanceFromTour(tourA, orders)
    distanceB = getTotalDistanceFromTour(tourB, orders)
    if distanceA < distanceB and toured_city_index != 0:
      tour.insert(toured_city_index, next_destination)
    else:
      tour.insert(toured_city_index + 1, next_destination)
    
    # Delete this order from both places - using key origin and using key min_from_origin
    # del all_distances_copy[toured_city][next_destination]
    # del all_distances_copy[next_destination][toured_city]
    for order in all_distances.keys():
      try:
        del all_distances_copy[order][next_destination]
      except:
        lala = ''
    for order in tour:
      try:
        del all_distances_copy[next_destination][order]
      except:
        lala = ''
  
    # print(tour)
    # print(getTotalDistanceFromTour(tour, orders))

  # Return tour without origin (which is not supposed to be there)
  # print(tour)
  return tour[1::]
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
    # print(orders)

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

                # Puts orderA-Origin distance 
                origin_distance = ((0 - ax)**2 + (0 - ay)**2)** 0.5
                origin_distance  = round(origin_distance, 5)
                d_in_d = distance_list[orderA[0]]
                d_in_d['origin'] = origin_distance

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

######## modfiied the get distance ###########################################################################################################


def get_distance(orders):
    distance_list = {}

    for orderA in orders:
        for orderB in orders:
            if orderA[0] != orderB[0]:
                distance = ((orderA[1] - orderB[1])**2 + (orderA[2] - orderB[2])**2)** 0.5
                distance  = round(distance, 5)
                distance_list[orderA[0] + '-' + orderB[0]] = distance          

    for distanceA in distance_list.copy().keys():
        for distanceB in distance_list.copy().keys():
            if distanceA.split('-') == distanceB.split('-')[::-1]:
                distance_list.pop(distanceA)
    return(distance_list)
    
def get_origin_distance(orders):
    distance_list = {}
    for orderA in orders:
        distance = ((orderA[1] - 0 )**2 + (orderA[2] - 0)**2)** 0.5
        distance  = round(distance, 5)
        distance_list['Origin' + '-' + orderA[0]] = distance

    return(distance_list) 

def get_all_distance(orders):
    distance_list = {}

    for orderA in orders:
        distance = ((orderA[1] - 0 )**2 + (orderA[2] - 0)**2)** 0.5
        distance  = round(distance, 5)
        distance_list['Origin' + '-' + orderA[0]] = distance

        for orderB in orders:
            if orderA[0] != orderB[0]:
                distance = ((orderA[1] - orderB[1])**2 + (orderA[2] - orderB[2])**2)** 0.5
                distance  = round(distance, 5)
                distance_list[orderA[0] + '-' + orderB[0]] = distance          

    for distanceA in distance_list.copy().keys():
        for distanceB in distance_list.copy().keys():
            if distanceA.split('-') == distanceB.split('-')[::-1]:
                distance_list.pop(distanceA)
    return(distance_list)
    
# schedule_q1()