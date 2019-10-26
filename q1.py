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