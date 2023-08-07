import json

import networkx as nx

CIFP = {}
G = nx.MultiDiGraph()


def findRoute(dep, arr):
    global G
    try:
        GC = G.copy()
        if dep in CIFP['SiE'] and len(CIFP['SiE'][dep]) != 0:
            if arr in CIFP['StaE'] and len(CIFP['StaE'][arr]) != 0:
                for each in CIFP['SiE'][dep]:
                    GC.add_edge(dep, each, weight=0)
                for each in CIFP['StaE'][arr]:
                    GC.add_edge(each, arr, weight=0)
                routeList = nx.dijkstra_path(GC, dep, arr)
                return proceedRouteList(routeList, GC)
            return None
        return None
    except:
        return None


def proceedRouteList(routeList, GC):
    edge_labels = nx.get_edge_attributes(GC.subgraph(routeList), 'name')
    result = ''
    lastRoute = ''
    for i in range(1, len(routeList) - 1):
        if i == len(routeList) - 2:
            # print(routeList[i][2:])
            result+=routeList[i][2:]
            continue
        lab = (routeList[i], routeList[i + 1], 0)
        # print(f'{routeList[i][2:]} ------------ {edge_labels[lab]}')
        if lastRoute == edge_labels[lab]:
            continue
        lastRoute = edge_labels[lab]
        result+=routeList[i][2:]+f' {edge_labels[lab]} '
    return result


def loadData():
    global G
    global CIFP
    G.clear()
    with open('BakedData/CIFP.json', 'r') as f:
        CIFP = json.load(f)
    with open('BakedData/data.json', 'r') as f:
        data = json.load(f)
    for seg in data:
        if (seg['seg_type'] == 'N'):
            G.add_edge(seg['start_region'] + seg['start'], seg['end_region'] + seg['end'], weight=seg['weight'],
                       name=seg['route_name'])
            G.add_edge(seg['end_region'] + seg['end'], seg['start_region'] + seg['start'], weight=seg['weight'],
                       name=seg['route_name'])
        if (seg['seg_type'] == 'B'):
            G.add_edge(seg['end_region'] + seg['end'], seg['start_region'] + seg['start'], weight=seg['weight'],
                       name=seg['route_name'])
        if (seg['seg_type'] == 'F'):
            G.add_edge(seg['start_region'] + seg['start'], seg['end_region'] + seg['end'], weight=seg['weight'],
                       name=seg['route_name'])


loadData()
r = findRoute('ZSSS', 'LOWW')
print(r)
