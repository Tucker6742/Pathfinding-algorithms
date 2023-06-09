from ..models.Maze import Maze


    
    
# def checkCell(maze, direction):
#     if direction == "E":
            
    
def dfs(maze):    
    startCell = maze.getCell(maze.getStart()[0], maze.getStart()[1])
    endCell = maze.getCell(maze.getEnd()[0], maze.getEnd()[1])
    explored = []
    frontier = [startCell]
    sequence = "ESNW"
    dfs_path={}
    while len(frontier)> 0:
        # Set the current cell as the first element of frontier (frontier is a stack of cells that wait for processing)
        currentCell = frontier[0]
        # Append that cell into explored list as it was gone through
        explored.append(currentCell)
        # Delete it from frontier list
        frontier.pop(0)
        # Break the loop if you have found the destination
        if currentCell.getCoordinates()[0] == endCell.getCoordinates()[0] and currentCell.getCoordinates()[1] == endCell.getCoordinates()[1]:
            print("Found")
            break
            
        # Find all way to go for current cell and append it to temp list (east, south, north, west respectively)
        temp = []        
        for neighbor in maze.getNeighbors(currentCell):
            if neighbor.getStatus() == 0:
                # If cell is explored then continue to the next loop
                if neighbor in explored:
                    continue
                # Add each next cell to temp
                temp.append(neighbor)

                dfs_path[neighbor] = currentCell
        # After having a full way of the cell, extend the frontier list by adding the temp to the begin of the frontier        
        temp.extend(frontier)
        frontier = temp.copy()

    fwd_path = {}
    cell = endCell
    while cell != startCell:
        fwd_path[dfs_path[cell]] = cell
        cell = dfs_path[cell]

    path = list(fwd_path.values())
    path.reverse()
    
    return path, explored
