from utility import *
from two_opt_2 import schedule_q1
from pandas import *

def legality_checking(truck_paths, order_list, number_trucks):
	check_trucks(truck_paths, number_trucks)
	checking_all_order(truck_paths, order_list)
	if checking_if_airports(truck_paths):
		print("no airport in q1")
		exit()

# replace these parameters with different csv file locations
order_csv = "./dataset/orders_009.csv"
parameter_csv = "./dataset/parameters_001.csv"

number_trucks, truck_speed, plane_speed = parameter_reader(parameter_csv)
orders = list_reader(order_csv)
location_dict = location_dict_generation([orders])

truck_paths = schedule_q1(orders, number_trucks)  # call your function
print(truck_paths)
print(len(truck_paths))
legality_checking(truck_paths, orders, number_trucks)
print("Score for q1 is:", scoring_q1(truck_paths, location_dict)) # print your score






