import math
import time

"""
Global variables
"""
MAX_INTEGER = (1 << 32) 
BASE = ["base", 0,0]

"""
Calculates distance between two locations
"""
def distance_calc(location_1,location_2):
	return math.hypot(location_1[1]-location_2[1], location_1[2]-location_2[2])

"""
Using the last visited location, find the next best location
"""
def find_closest_unfulfilled_order(last, locations, completed):
	
	min_distance = MAX_INTEGER
	best = []
	for location in locations.values():
		
		if location[0] in completed:
			continue
		else:
			dist = distance_calc(last, location)
			if (dist < min_distance):
				min_distance = dist
				best = location
				
	completed.add(best[0])
	return best, min_distance

"""
Greedy algorithm implementation
"""
def greedy(locations):
	
	completed = set()
	truck_path = []
	last, cost = find_closest_unfulfilled_order(BASE, locations, completed)
	truck_path.append(last[0])
	
	for i in range(len(locations)-1):
		last, c = find_closest_unfulfilled_order(last, locations, completed)
		truck_path.append(last[0])
		cost += c
	return truck_path,cost

"""
Generates a new route by swapping paths between locations
"""
def optSwap(existing, i, k, locations, best_cost):
	new_route = existing[:i] + existing[i:k][::-1] + existing[k:]
	
	cost = best_cost - distance_calc(locations[existing[i-1]],locations[existing[i]]) - \
		distance_calc(locations[existing[k-1]],locations[existing[k]]) + \
		distance_calc(locations[new_route[i-1]],locations[new_route[i]]) + \
		distance_calc(locations[new_route[k-1]],locations[new_route[k]]) + \
		distance_calc(["",0,0], locations[new_route[-1]]) - \
		distance_calc(["",0,0], locations[existing[-1]])
	return new_route, cost

"""
Iteration step in 2-opt
"""
def iteration(existing, best_cost, locations):
	for i in range(1,len(locations)-1):
		for j in range(i+1, len(locations)):
			new_route, new_cost = optSwap(existing, i, j, locations, best_cost)
			if new_cost + 1 < best_cost:
				print(len(new_route), i, j, best_cost)
				return new_route, new_cost
	return None, None

"""
Calculate cost of travelling between two locations
"""
def get_cost(track, locations):
	cost = 0
	for t in range(len(track)-1):
		cost += distance_calc(locations[track[t]], locations[track[t+1]])
	# print(track)
	cost += distance_calc(BASE, locations[track[0]]) + distance_calc(BASE,locations[track[-1]])
	return cost

"""
Get the index of the track with the largest cost, used in do_transfer
"""
def get_index_of_largest(tracks):
	largest = tracks[0][1]
	index = 0
	for i in range(1, len(tracks)):
		if largest < tracks[i][1]:
			largest = tracks[i][1]
			index = i
	print("largest index:", index)
	return index

"""
Find the route with the highest cost and attempt to transfer its location to its neighbours
"""
def do_transfer(tracks, locations):
	index = get_index_of_largest(tracks)
	cost_to_beat = tracks[index][1]
	if index > 0 and len(tracks[index-1])>1:
		to_base_cost = distance_calc(locations[tracks[index][0][0]], BASE)
		left_pcost = tracks[index-1][1] - distance_calc(locations[tracks[index-1][0][0]], BASE) + to_base_cost
		left_index_cost = tracks[index][1] + distance_calc(locations[tracks[index-1][0][1]], BASE) - to_base_cost
		if (left_pcost < cost_to_beat and left_index_cost < cost_to_beat):
			tracks[index-1][1] = left_pcost
			tracks[index][1] = left_index_cost
			tracks[index-1][0].append(tracks[index][0][0])
			tracks[index][0] = tracks[index][0][1:]
			print("Improvement at", index, "previously:", cost_to_beat, "now:", left_index_cost)
			return True

	if index < len(tracks) - 1 and len(tracks[index+1]) > 1:
		to_base_cost = distance_calc(locations[tracks[index][0][-1]], BASE)
		right_pcost =  tracks[index-1][1] - distance_calc(locations[tracks[index-1][0][-1]], BASE) + to_base_cost
		right_index_cost = tracks[index][1] + distance_calc(locations[tracks[index-1][0][-2]], BASE) - to_base_cost
		if (right_pcost < cost_to_beat and right_index_cost < cost_to_beat):
			tracks[index+1][1] = right_pcost
			tracks[index][1] = right_index_cost
			tracks[index+1][0].append(tracks[index][0][-1])
			tracks[index][0] = tracks[index][0][:-1]
			
			print("Improvement at", index, "previously:", cost_to_beat, "now:", right_index_cost)
			return True

	print("No improvement")
	return False

"""
Chopping the track up followed by calling do_transfer
"""
def get_results(existing, best_cost, number_trucks, locations):
	tracks = []

	remainder = len(existing) % number_trucks
	add = len(existing) // number_trucks
	# print(add)
	current = 0
	while (current < len(existing)):
		tracks.append([existing[current: current+add+min(1,remainder)], get_cost(existing[current: current+add+min(1,remainder)], locations)])
		current = current+add+min(1,remainder)
		remainder = max(0, remainder-1)
		# print(remainder)

	# print("DEBUG: number of locations = ", len(existing), "vs", current)
	# print("DEBUG: number of trucks = ", len(tracks))

	improvement = True
	while improvement == True:
		improvement = do_transfer(tracks, locations)

	return [x[0] for x in tracks]

def schedule_q1(orders, number_trucks):
	start = time.time()

	#Transforming data given
	locations = {item[0]:[item[0], float(item[1]), float(item[2])] for item in orders}

	#get a route from greedy
	existing, best_cost = greedy(locations)

	#begin 2-opt to improve route
	improvement = True
	while improvement:
		r, c = iteration(existing, best_cost, locations)

		#stops when there are no improvements
		if (r == None and c == None):
			improvement = False
			break
		else:
			existing, best_cost = r, c

	#chop up track to get many tracks
	results = get_results(existing, best_cost, number_trucks, locations)
	print(time.time() - start, "seconds")
	return results