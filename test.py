import json

import networkx as nx
import matplotlib.pyplot as plt
G = nx.MultiDiGraph()

with open('BakedData/data.json','r')as f:
    data = json.load(f)

for seg in data:
    if(seg['seg_type']=='N'):
        G.add_edge(seg['start_region']+seg['start'],seg['end_region']+seg['end'],weight=seg['weight'],name=seg['route_name'])
        G.add_edge(seg['end_region'] + seg['end'], seg['start_region'] + seg['start'], weight=seg['weight'],
                   name=seg['route_name'])
    if (seg['seg_type'] == 'B'):
        G.add_edge(seg['end_region'] + seg['end'], seg['start_region'] + seg['start'], weight=seg['weight'],
                   name=seg['route_name'])
    if (seg['seg_type'] == 'F'):
        G.add_edge(seg['start_region'] + seg['start'], seg['end_region'] + seg['end'], weight=seg['weight'],
                   name=seg['route_name'])

print(G.number_of_nodes())
print(G.number_of_edges())

# print(nx.shortest_path(G,'ZGYIN','ZBAVBOX'))

# sts = nx.shortest_path(G,'ZGYIN','ZBDUGEB')
# sts = nx.bellman_ford_path(G,'ZGYIN','ZBDUGEB')
sts = nx.dijkstra_path(G,'ZGYIN','ZBDUGEB')

edge_labels = nx.get_edge_attributes(G.subgraph(sts), 'name')

for i in range(len(sts)):
    if i == len(sts)-1:
        print(sts[i][2:])
        continue
    lab = (sts[i],sts[i+1],0)
    print(f'{sts[i][2:]} ------------ {edge_labels[lab]}')
print('航路长度为：'+str(nx.dijkstra_path_length(G,'ZGYIN','ZBDUGEB')))

# from DataBaker import Baker
#
# Baker.bakeAll()