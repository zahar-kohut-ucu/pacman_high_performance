def dijkstraFindShortestPathTo(myMaze, pacman, dotPos):
    visited = set()
    ways = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    pacmanPos = (pacman[0], pacman[1])
    distances = {pacmanPos: 0}
    queue = [(0 , pacmanPos)]
    avoidPositions = []
    for i, j in ghostsPosition:
        if ((pacman[1] == j and abs(pacman[0] - i) < 5) or (pacman[0] == i and abs(pacman[1] - j) < 5) or (estimateEuristicCost(pacmanPos, (i,j)) < 7)):
            avoidPositions.append((i, j))
            for di in range(-1, 2):
                for dj in range(-1, 2):
                    avoidPositions.append((i+di, j+dj))
    while queue:
        distance, curr = heapq.heappop(queue)

        if curr == dotPos:
            break

        if curr in visited:
            continue

        visited.add(curr)

        for di, dj in ways:
            i, j = curr[0] + di, curr[1] + dj
            if  0 <= i < trueM and 0 <= j < trueN and mymaze[i][j] != 1 and (i,j) not in avoidPositions:
                neighbour = (i, j)
                newDistance = distance + 1
                if neighbour not in distances or newDistance < distances[neighbour]:
                    distances[neighbour] = newDistance
                    heapq.heappush(queue, (newDistance, neighbour))

    way = []
    curr = dotPos
    if curr in distances:
        while curr != pacmanPos:
            way.append(curr)
            for di, dj in ways:
                i, j = curr[0] - di, curr[1] - dj
                if (i, j) in distances and distances[curr] == distances[(i, j)] + 1:
                    curr = (i, j)
                    break
        return way[::-1]
    
    closestDist = 1e10
    closestGhost = None
    for ghost in ghostsPosition:
        dist = estimateEuristicCost(pacmanPos, ghost)
        if dist < closestDist:
            closestGhost = ghost
            closestDist = dist
    return [escapeGhost(mymaze, trueM, trueN, pacmanPos, closestGhost)]