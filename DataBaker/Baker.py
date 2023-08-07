import json
import os

from geopy.distance import geodesic

fix = []
nav = []
route = []


def bakeAll():
    global fix, nav, route
    route = bakeRoute()
    fix = bakePoint()
    nav = bakeNav()
    route = proceedRoute(route)
    with open('data.json', 'w') as f:
        json.dump(route, f)


def findNode(name, node_type, region):
    if node_type == 11:
        for fi in fix:
            if fi['name'] == name and fi['region'] == region:
                return fi
    if node_type == 2:
        for na in nav:
            if na['name'] == name and na['region'] == region and na['type'] == 2:
                return na
    if node_type == 3:
        for na in nav:
            if na['name'] == name and na['region'] == region and na['type'] != 2:
                return na


def removeSpace(words: list):
    while '' in words:
        words.remove('')
    return words


def proceedRoute(routes):
    resultRoute = []
    count = 1
    for route in routes:
        pt1 = findNode(route['start'], route['start_type'], route['start_region'])
        pt2 = findNode(route['end'], route['end_type'], route['end_region'])
        distance = geodesic((pt1['lat'], pt1['lon']), (pt2['lat'], pt2['lon'])).nm
        route['weight'] = distance
        resultRoute.append(route)
        print(
            f'航路{route["route_name"]}中的{route["start"]}和{route["end"]}之间的距离为{distance}海里 [{count}/{len(routes)}]')
        count += 1
    return resultRoute


def bakePoint():
    with open('./navdata/earth_fix.dat') as f:
        data = f.read()
    lines = data.split('\n')[3:]
    fixData = []
    for line in lines:
        words = line.split(' ')
        words = removeSpace(words)
        if len(words) < 7:
            continue

        fix = {
            'lat': float(words[0]),
            'lon': float(words[1]),
            'name': words[2],
            'tma': words[3],
            'region': words[4],
        }
        fixData.append(fix)
    return fixData


def bakeNav():
    with open('./navdata/earth_nav.dat') as f:
        data = f.read()
    lines = data.split('\n')[3:]
    navData = []
    for line in lines:
        words = line.split(' ')
        words = removeSpace(words)
        if len(words) < 7:
            continue

        nav = {
            'type': int(words[0]),
            'lat': float(words[1]),
            'lon': float(words[2]),
            'elev': words[3],
            'freq': int(words[4]),
            'name': words[7],
            'region': words[9],
        }
        navData.append(nav)
    return navData


def bakeRoute():
    with open('./navdata/earth_awy.dat') as f:
        data = f.read()
    existingSeg = {}
    lines = data.split('\n')
    resultRoute = []
    for line in lines:
        words = line.split(' ')
        words = removeSpace(words)
        if len(words) != 11:
            continue
        if words[7] == '1':
            continue
        if words[10] not in existingSeg:
            existingSeg[words[10]] = {}
        if words[0] not in existingSeg[words[10]]:
            existingSeg[words[10]][words[0]] = []
        if words[3] not in existingSeg[words[10]][words[0]]:
            existingSeg[words[10]][words[0]].append(words[3])
        else:
            continue
        for eachR in words[10].split('-'):
            segment = {
                'start': words[0],
                'start_region': words[1],
                'start_type': int(words[2]),
                'end': words[3],
                'end_region': words[4],
                'end_type': int(words[5]),
                'seg_type': words[6],
                'alt_low': int(words[8]),
                'alt_high': int(words[9]),
                'route_name': eachR,
            }
            resultRoute.append(segment)
    return resultRoute

def bakeCIFP():
    dirs = os.listdir('./navdata/CIFP')
    resultData = {'SiE':{},'StaE':{}}
    for airport in dirs:
        with open(f'./navdata/CIFP/{airport}','r')as f:
            airportData = f.read()
        lines = airportData.split('\n')
        resultData['SiE'][airport[:-4]] = set()
        resultData['StaE'][airport[:-4]] = set()
        for i in range(len(lines)):
            line = lines[i]
            if line[:3]=='SID':
                fields = line[4:].split(',')
                if fields[4] == ' ':
                    continue
                if i == len(lines)-1:
                    continue
                nextLine = lines[i+1]
                if fields[1]=='5' or fields[1]=='2':
                    if nextLine[:3] == 'SID':
                        nextField = nextLine[4:].split(',')
                        if nextField[2] == fields[2]:
                            continue
                    resultData['SiE'][airport[:-4]].add(fields[5]+fields[4])
                elif fields[1]=='6' or fields[1]=='3':
                    if nextLine[:3] == 'SID':
                        nextField = nextLine[4:].split(',')
                        if nextField[3] == fields[3]:
                            continue
                    resultData['SiE'][airport[:-4]].add(fields[5]+fields[4])
            if line[:3] == 'STA':
                fields = line[5:].split(',')
                if fields[4] == ' ':
                    continue
                if i == len(lines)-1:
                    continue
                nextLine = lines[i-1]
                if fields[1]=='5' or fields[1]=='2':
                    if nextLine[:3] == 'STA':
                        nextField = nextLine[5:].split(',')
                        if nextField[2] == fields[2]:
                            continue
                    resultData['StaE'][airport[:-4]].add(fields[5]+fields[4])
                if fields[1]=='1' or fields[1]=='4':
                    if nextLine[:3] == 'STA':
                        nextField = nextLine[5:].split(',')
                        if nextField[3] == fields[3]:
                            continue
                    resultData['StaE'][airport[:-4]].add(fields[5]+fields[4])
        resultData['SiE'][airport[:-4]] = list(resultData['SiE'][airport[:-4]])
        resultData['StaE'][airport[:-4]] = list(resultData['StaE'][airport[:-4]])
    return resultData
