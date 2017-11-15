# Edited source code from: http://code.activestate.com/recipes/578919-python-a-pathfinding-with-binary-heap/

import numpy
from heapq import *


def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def astar(array, start, goal, body, size):

    neighbors = [(0,1),(0,-1),(1,0),(-1,0)]

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    
    while oheap:

        current = heappop(oheap)[1]

        if current != start:
            body[0] = current
            body.insert(1, came_from[current])
            array[body[len(body)-1]] = 0
            body = body[:len(body)-1]
            for i in range(1, len(body)):
                array[body[i]] = 1
        

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j           
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:                
                    if array[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    # array bound y walls
                    continue
            else:
                # array bound x walls
                continue
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))
                
    return False


   #astar(array, start, destination)

def forBen(directions, orig):
    retArr = [] 

    cur = orig
    for i in range(len(directions)-1, -1, -1):
        print(i, directions[i], cur)
        if ( cur[0] == directions[i][0] - 1 and cur[1] == directions[i][1] ):
            retArr.append("DOWN")

        elif ( cur[0] == directions[i][0] + 1 and cur[1] == directions[i][1] ):
            retArr.append("UP")

        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] - 1 ):
            retArr.append("RIGHT")

        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] + 1 ):
            retArr.append("LEFT")

        cur = directions[i]

    return retArr

def forJosh(directions, orig, prev):
    retArr = [] 

    cur = orig
    ori = prev
    for i in range(len(directions)-1, -1, -1):

        if ( cur[0] == directions[i][0] - 1 and cur[1] == directions[i][1] and ori == "UP"):
            retArr.append("1")
        elif ( cur[0] == directions[i][0] - 1 and cur[1] == directions[i][1] and ori == "DOWN"):
            retArr.append("R")
            retArr.append("R")
            retArr.append("1")
            ori = "UP"
        elif ( cur[0] == directions[i][0] - 1 and cur[1] == directions[i][1] and ori == "LEFT"):
            retArr.append("R")
            retArr.append("1")
            ori = "UP"
        elif ( cur[0] == directions[i][0] - 1 and cur[1] == directions[i][1] and ori == "RIGHT"):
            retArr.append("L")
            retArr.append("1")
            ori = "UP"

        elif ( cur[0] == directions[i][0] + 1 and cur[1] == directions[i][1] and ori == "DOWN"):
            retArr.append("1")
        elif ( cur[0] == directions[i][0] + 1 and cur[1] == directions[i][1] and ori == "UP"):
            retArr.append("L")
            retArr.append("L")
            retArr.append("1")
            ori = "DOWN"
        elif ( cur[0] == directions[i][0] + 1 and cur[1] == directions[i][1] and ori == "LEFT"):
            retArr.append("L")
            retArr.append("1")
            ori = "DOWN"
        elif ( cur[0] == directions[i][0] + 1 and cur[1] == directions[i][1] and ori == "RIGHT"):
            retArr.append("R")
            retArr.append("1")
            ori = "DOWN"

        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] - 1 and ori == "LEFT"):
            retArr.append("1")
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] - 1 and ori == "UP"):
            retArr.append("R")
            retArr.append("1")
            ori = "LEFT"
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] - 1 and ori == "DOWN"):
            retArr.append("L")
            retArr.append("1")
            ori = "LEFT"
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] - 1 and ori == "RIGHT"):
            retArr.append("R")
            retArr.append("R")
            retArr.append("1")
            ori = "LEFT"

        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] + 1 and ori == "RIGHT"):
            retArr.append("1")
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] + 1 and ori == "UP"):
            retArr.append("L")
            retArr.append("1")
            ori = "RIGHT"
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] + 1 and ori == "DOWN"):
            retArr.append("R")
            retArr.append("1")
            ori = "RIGHT"
        elif ( cur[0] == directions[i][0] and cur[1] == directions[i][1] + 1 and ori == "LEFT"):
            retArr.append("L")
            retArr.append("L")
            retArr.append("1")
            ori = "RIGHT"

        cur = directions[i]

    return retArr


def getDir(body, size, dest, prev):

    nmap = numpy.array([
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]])

    print(body)
    for i in range(1, len(body)):
        nmap[body[i][0]][body[i][1]] = 1

    head = body[0]

    directions = (astar(nmap, head, dest, body, size))
    
    forBoth = []
    if directions != False: 
        forBoth.append(forBen(directions, head))
        forBoth.append(forJosh(directions, head, prev))

        return forBoth

    else: 
        return [["P"], ["P"]]
    
   
#example call for getDir

 #   body = [(1,1), (1, 2)]

 #   snake_size = 2

 #   dest = (3,3)

 #   prev = "L" 

 #   array = getDir(body, snake_size, dest, prev)

 #   array[0] is for Ben, array[1] is for being sent to the PIC







    