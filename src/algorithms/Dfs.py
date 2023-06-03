from ..models.Maze import Maze


    
    
# def checkCell(maze, direction):
#     if direction == "E":
            
    
def dfs(maze):    
    startCell = maze.cells[maze.starting_point[1]][maze.starting_point[0]]
    endCell = maze.cells[maze.ending_point[0]][maze.ending_point[1]]
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
        if currentCell.x == endCell.x and currentCell.y == endCell.y:
            print("Found")
            break
            
        # Find all way to go for current cell and append it to temp list (east, south, north, west respectively)
        temp = []        
        for direction in sequence:
            if currentCell.environment[direction] == 0:
                if direction == "E":
                    nextCell = maze.eastCell(currentCell)
                elif direction == "S":
                    nextCell = maze.southCell(currentCell)
                elif direction == "N":
                    nextCell = maze.northCell(currentCell)
                elif direction == "W":
                    nextCell = maze.westCell(currentCell)
                # If cell is explored then continue to the next loop
                if nextCell in explored:
                    continue
                # Add each next cell to temp
                temp.append(nextCell)
                dfs_path[nextCell] = currentCell
        # After having a full way of the cell, extend the frontier list by adding the temp to the begin of the frontier        
        temp.extend(frontier)
        frontier = temp.copy()

    fwd_path = {}
    cell = endCell
    while cell != startCell:
        fwd_path[dfs_path[cell]] = cell
        cell = dfs_path[cell]

    path = list(fwd_path.values())
    return path, explored
