"""
Redmart Skiing Code
"""

pathInfo = []

"""
read the first line and return a list of lists 
or a multi-dimensuinal array or a grid of 
1000x1000 
"""
def configMatrix(content):
    with open(content) as map:
        for line in map:
            dimensions = line.split()
            grid = [[0 for x in range(int(dimensions[0]))] for x in range(int(dimensions[1]))]     
            return grid

"""
Fill the 1000x1000 grid with points in the map
"""
def fillGrid(content,grid):
    row = -2
    with open(content) as map:
        for line in map:
            row = row + 1;
            if row > -1:
                mapPoints = line.split()
                col = 0
                for point in mapPoints:
                    grid[row][col] = int(point)
                    col = col + 1
    return grid

"""
Function to detect if there is a slope in any direction.
If yes then in what directions and what are the pssible routes
and then recursively call the path tracing function from th next point to 
see all these possibilities again till there is no path left to trace
"""    
def hasFork(grid, row, col, pathInfoRow):
    direction = ""
    pathPossible = 0
    if row - 1 != -1 and grid[row - 1][col] < grid[row][col]:
        pathPossible = pathPossible + 1
        direction = "N" 
    if row + 1 != 1000 and grid[row + 1][col] < grid[row][col]:
        pathPossible = pathPossible + 1
        direction = direction + "S"
    if col - 1 != -1 and grid[row][col - 1] < grid[row][col]:
        pathPossible = pathPossible + 1
        direction = direction + "W"
    if col + 1 != 1000 and grid[row][col + 1] < grid[row][col]:
        pathPossible = pathPossible + 1
        direction = direction + "E"
    threadName = str(pathPossible) + " " + str(grid[row][col]) + " " + direction
    counter = 0
    elementsToCopy = 0
    if pathPossible > 0:
        elementsToCopy = len(pathInfo[pathInfoRow])
        for counter in range(pathPossible):
            rowMod = 0
            colMod = 0
            if counter > 0:
                pathInfo.append([])    
            if direction[counter] == "N":
                rowMod = -1
            elif direction[counter] == "S":
                rowMod = 1
            elif direction[counter] == "W":
                colMod = -1
            elif direction[counter] == "E":
                colMod = 1
            tracePath(grid, row + rowMod, col + colMod, pathInfoRow + counter, counter, elementsToCopy)

"""
Trace the skiing path
"""
def tracePath(grid, row, col, pathInfoRow, rowToTraverseBack, elementsToCopy ):
    global pathInfo
    if rowToTraverseBack == 0:
        point = pathInfo[pathInfoRow]
    else:
        totalLength = len(pathInfo[pathInfoRow - rowToTraverseBack])
        elementsNotToCopy = totalLength - elementsToCopy
        point = pathInfo[pathInfoRow - rowToTraverseBack][ : -(elementsNotToCopy)]
        pathInfoRow = len(pathInfo) - 1
    point.append(grid[row][col])
    pathInfo[pathInfoRow] = point
    hasFork(grid, row, col, pathInfoRow)

"""
Get the maximum path length among all possible routes that can be taken
"""    
def getMaxPath(pathInfo):
    max = 0
    for paths in pathInfo:
        if len(paths) > max:
            max = len(paths)
    return max

"""
Get max drop between same length routes
"""             
def getMaxDrop(maxPaths):
    maxDrop = 0
    for paths in maxPaths:
        if paths[0] - paths[-1] > maxDrop:
            maxDrop = paths[0] - paths[-1]
    return maxDrop
    
        
grid = configMatrix("map.txt")
grid = fillGrid("map.txt", grid)

rowcounter = -1
for row in grid:
    rowcounter = rowcounter + 1
    colcounter = -1
    
    for col in row:
        colcounter = colcounter + 1
        pathInfoRow = len(pathInfo);
        pathInfo.append([])
        tracePath(grid, rowcounter, colcounter, pathInfoRow, 0, 0)

max = getMaxPath(pathInfo)

maxPaths = []
for paths in pathInfo:
    if len(paths) == max:
        maxPaths.append(paths)

if len(maxPaths) > 1:
    maxDrop = getMaxDrop(maxPaths)
    print str(max) + str(maxDrop)
else:
    print str(max) + str(maxPaths[0][0] - maxPaths[0][-1])

        
