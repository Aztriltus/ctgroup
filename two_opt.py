def travel_order(orders):
    from operator import itemgetter
    quad1 = []
    quad2 = []
    quad3 = []
    quad4 = []

    for order in orders:
        # print(order[1])
        # print(order[2])
        if float(order[1]) <= 0 and float(order[2]) >= 0:
            quad1.append(order)
        elif float(order[1]) > 0 and float(order[2]) >= 0:
            quad2.append(order)
        elif float(order[1]) >= 0 and float(order[2]) < 0:
            quad3.append(order)
        else:
            quad4.append(order)
    quad1 = sorted(quad1, key = itemgetter(1))
    quad2 = sorted(quad2, key = itemgetter(1))
    quad3 = sorted(quad3, key = itemgetter(1))
    quad4 = sorted(quad4, key = itemgetter(1))

    all_orders = [['Origin', 0, 0]] + quad2 + quad3[::-1] + quad4 + quad1 + [['Origin', 0, 0]]
    
#     print(all_orders)
    
    returned_order = []
    for order in all_orders:
        returned_order.append([order[0]])
    return returned_order
# print(travel_order(orders))

def get_all_distance(orders):
    distance_list = {}

    for orderA in orders:
        distance = ((float(orderA[1]) - 0 )**2 + (float(orderA[2]) - 0)**2)** 0.5
        distance  = round(distance, 5)
        distance_list['Origin' + '-' + orderA[0]] = distance
        distance_list[orderA[0] + '-' + 'Origin'] = distance

        for orderB in orders:
            if orderA[0] != orderB[0]:
                distance = ((float(orderA[1]) - float(orderB[1]))**2 + (float(orderA[2]) - float(orderB[2]))**2)** 0.5
                distance  = round(distance, 5)
                distance_list[orderA[0] + '-' + orderB[0]] = distance          

#     for distanceA in distance_list.copy().keys():
#         for distanceB in distance_list.copy().keys():
#             if distanceA.split('-') == distanceB.split('-')[::-1]:
#                 distance_list.pop(distanceA)
    return(distance_list)
# print(get_all_distance(orders))


def schedule_q1(orders, number_trucks):
    order = travel_order(orders)
#     print(order)
#     print(111111111111111111111111111111111111111111111111111111111111111)
    distance_btw_locations = get_all_distance(orders)
#     print(distance_btw_locations)
#     print(222222222222222222222222222222222222222222222222222222222222222)
    
    total_distance = 0
    location_distance_list = []
    for i in range(len(order)):
        location_distance_two_way = []
        if i < len(order) - 1:
            total_distance += distance_btw_locations[order[i][0] + '-' + order[i + 1][0]]
            location_distance_two_way = [order[i][0] + '-' + order[i + 1][0], distance_btw_locations[order[i][0] + '-' + order[i + 1][0]]]
            location_distance_list.append(location_distance_two_way)
            
#     print(total_distance)
#     print(333333333333333333333333333333333333333333333333333333333333333)
#     print(location_distance_list)
#     print(444444444444444444444444444444444444444444444444444444444444444)
    
    average_distance_per_truck = total_distance/number_trucks
    returned_order = []
    for i in range(number_trucks):
        truck= []
        truck_travelled_distance = 0 
        while truck_travelled_distance < average_distance_per_truck and location_distance_list != []:
            truck_travelled_distance += location_distance_list[0][1]
            truck.append(location_distance_list[0][0].split('-')[0])
          
            del location_distance_list[0]  
        if len(truck) > 0: 
            returned_order.append(truck)
    
    del returned_order[0][0]
    for order in returned_order:
        if len(order) == 0:
            returned_order.remove(order)
    return(returned_order)
    
# print(schedule_q1(orders, number_trucks))        