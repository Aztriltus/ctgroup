# Team G2T08
# Jiang Jia Xing, Ng Zheng Hao, Ong Soon Heng

import numpy as np, random, operator, copy, pandas as pd, csv, math
from sklearn.cluster import KMeans
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def schedule_q1(orders, number_trucks):
  # Get groups from k-means clustering algo (using sk.learn)
  d = cluster(orders, number_trucks)

  # Initialise the main array
  # This will store arrays of orders
  # So for number_trucks = 25, this array should contain 25 arrays of orders
  all_tour = []

  # For-loop the keys gotten from clustering and 
  # Retrieve the orders from each group
  for group in d.keys():
    all_distances = distances(d[group])
    # Use greedy for rough first estimation
    existing_route = greedy2(d[group], all_distances)
    best_distance = calculateTotalDistance(existing_route, all_distances)
    # Two-opt starts here
    improved = True
    while improved:
      improved = False
      for i in range(len(existing_route) - 1):
        for k in range(i + 1, len(existing_route)):
          new_route = twoOptSwap(existing_route, i, k)
          new_distance = calculateTotalDistance(new_route, all_distances)
          if new_distance < best_distance:
            existing_route = new_route
            best_distance = new_distance
            improved = True
    # Add the best route in this cluster to output array
    all_tour.append(existing_route)
  return all_tour
  
def twoOptSwap(existing_route, i, k):
  return existing_route[:i] + existing_route[i:k][::-1] + existing_route[k:]

def cluster(orders, number_trucks):

  # Grab only the coordinates
  array = []
  for order in orders:
    array.append([order[1],order[2]])

  # Convert into numpy array
  X = np.array(array)

  # Find clusters using sklearn
  # cluster = KMeans
  # cluster.fit_predict(X)
  cluster = KMeans(n_clusters=number_trucks)
  cluster.fit(X)

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

def calculateTotalDistance(route, all_distances):
  total_distance = 0
  for i in range(len(route)):
    next_i = (i + 1) if (i+1) < len(route) else 0
    order_current = route[i]
    order_next = route[next_i]
    # print(order_current)
    # print(order_next)
    total_distance += all_distances[order_current][order_next]
  return total_distance

def greedy2(orders, all_distances):
  all_distances_copy = copy.deepcopy(all_distances)

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
    distanceA = calculateTotalDistance(tourA, all_distances)
    distanceB = calculateTotalDistance(tourB, all_distances)
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
      except Exception:
        pass
    for order in tour:
      try:
        del all_distances_copy[next_destination][order]
      except Exception:
        pass
  
    # print(tour)
    # print(getTotalDistanceFromTour(tour, orders))

  # Return tour without origin (which is not supposed to be there)
  # print(tour)
  return tour[1::]

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