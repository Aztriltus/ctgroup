import numpy as np
from sklearn.cluster import Kmeans

def cluster(orders,number_trucks):
    array = []
    for order in orders:
        array.append(order[1],order[2])
        
    X = np.array(array)
        
    kmeans = Kmeans(n_clusters=number_trucks)
    kmeans.fit(X)
    
    temp = {}
    i = 0
    for cluster_no in cluster.labels_:
        if cluster_no not in temp:
            temp[cluster_no] = orders[i]
        else:
            temp[cluster_no].append(orders[i])
        i += 1
        
return temp #{0:[ID,x,y]...24:[ID,x,y]}

d = cluster(orders,number_trucks)
start = (0,0,0)

for cluster_no in d.keys():
    cityList = []
    for order in d[cluster_no]:
        city = (order[0],order[1], order[2])
        cityList.append(start)
        cityList.append(city) #cityList = [[(ID,x,y),(ID,x,y)],[]...[]]

cityList = [[('s',0,0),('a',5,12),('b',4,32),('c',20,5)],
            [('s',0,0),('d',121,222),('e',12,32),('f',260,213),('g',54,2),('x',2,1),('y',23,2),('z',2,2)]]

truck_paths = []

for route in cityList:
    temp = {}
    for ea in range(len(route)):
        temp[route[ea][0]] = [route[ea][1],route[ea][2]]
    
    r = list(temp.values())
    r2 = list(temp.keys())
    
    r = np.array(r)
    
    def path_distance(r,Citylist):
        for p in range(len(r)):
            return sum([np.linalg.norm(r[p]-r[p-1])])
    
    def two_opt_swap(r,i,k):
        for i in range(len(r)):
            for k in range(len(r)):
                # Reverse the order of all elements from element i to element k in array r.
                return np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))
            
            
            
    def two_opt(cities,improvement_threshold): # 2-opt Algorithm adapted from https://en.wikipedia.org/wiki/2-opt
        cities = np.array(cities)
        route = np.arange(cities.shape[0]) # Make an array of row numbers corresponding to cities.
        print(route)
        improvement_factor = 1 # Initialize the improvement factor.
        best_distance = path_distance(route,cities) # Calculate the distance of the initial path
        print(best_distance)
        while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
            distance_to_beat = best_distance # Record the distance at the beginning of the loop.
            for swap_first in range(1,len(route)-2): # From each city except the first and last,
                for swap_last in range(swap_first+1,len(route)): # to each of the cities following,
                    new_route = two_opt_swap(route,swap_first,swap_last) # try reversing the order of these cities
                    new_distance = path_distance(new_route,cities) # and check the total distance with this modification.
                    if new_distance < best_distance: # If the path distance is an improvement,
                        route = new_route # make this the accepted best route
                        best_distance = new_distance # and update the distance corresponding to this route.
            improvement_factor = 1 - best_distance/distance_to_beat # Calculate how much the route has improved.
        return route # When the route is no longer improving substantially, stop searching and return the route.
    
    truck_paths.append(two_opt(route,0.001))        
    