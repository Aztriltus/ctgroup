# Team ID: G03T01
import random

def schedule1(locations, start_location, number_of_trucks, orders):
    
    # Set the number of iterations
    number_of_iterations = 7

    # TODO: replace the code in this function with your algorithm

    # orders: Order ID, Weight, Delivery location

    # This simple model solution does not make use of locations
    # However, to optimize your longest traveling time, you should use the information in locations.

    # Iterate into dictionary so that future access to location is O(1)
    dic_locations = {}
    for ea in locations:  # 0: From 1: To 2: Distance
        start, end, distance = ea.split(",")
        if start+end not in dic_locations:
            dic_locations[start+end] = int(distance)
        else:
            dic_locations[start+end].append(int(distance))

    # Add this so that it can calculate
    dic_locations[start_location+start_location] = 0

    # Iterate into dictionary so that future access to location is O(1)
    dic_orders = {} # Eg. { 'CAN' : [(2, 130, 'CAN')] } or  { 'CAN' : [(2, 130, 'CAN'),(3, 330, 'SIN')] }
    for ea in orders:
        loc = ea[2]
        if loc not in dic_orders:
            dic_orders[loc] = [ea]
        else:
            dic_orders[loc].append(ea)
    
    dic_copy = dic_orders.copy() # to be use when outputing
    best_tour =  []
    distance = 999999999999999999999999999999999999999999
    for i in range(number_of_iterations):
        
        dic_orders = dic_copy.copy()
        # Creates the placement
        tour = []
        for i in range(number_of_trucks):
            tour.append(start_location)
            tour.append(None) # None representing spaces that the order can be inserted into
        tour.append(start_location)
        t_distance = 0
        # Loop all orders till all orders are accounted for
        while len(dic_orders) > 0:
            
            

            temp_best_distance = 9999999999999999999999999999999999999999999999
            temp_best_index = 0
            # Pick a random order and place at different possible positions
            selected_order = random.choice(list(dic_orders.keys()))
            for i in range(1, len(tour), 2):
                temp_temp_tour = tour.copy()
                temp_temp_tour[i] = selected_order
                temp_temp_tour = list(filter(None, temp_temp_tour))
                
                # Calculate Distance
                temp_distance = [0]
                for j in range(0,len(temp_temp_tour) -1):
                    if temp_temp_tour[j] == start_location:
                        temp_distance.append(0)
                    temp_distance[-1] += dic_locations[temp_temp_tour[j] + temp_temp_tour[j+1]]

                max_temp_distance = max(temp_distance)
                if max_temp_distance < temp_best_distance:
                    temp_best_distance = max_temp_distance
                    temp_best_index = i

            # Remove the order that is inserted into tour
            del dic_orders[selected_order]
            t_distance = temp_best_distance
            # Update Placement
            tour = tour[0:temp_best_index] + [None] + [selected_order] + tour[temp_best_index:]
        
        if t_distance < distance:
            distance = t_distance
            best_tour = tour
    
    # Convert tour into require output
    best_tour = list(filter(None, best_tour))
    output = []
    for i in range(0, len(best_tour) - 1):
        if best_tour[i] == start_location:
            output.append([])
        else:
            output[-1] +=  dic_copy[best_tour[i]]
    
    return output
   
