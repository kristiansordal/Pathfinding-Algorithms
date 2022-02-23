from collections import defaultdict
from dataclasses import dataclass
import pygame as pg
import numpy as np
import heapq

w = 1000     
h = 1000
screen = pg.display.set_mode((w ,h))

RED = ((200,45,21))
BLACK = ((0,0,0))
gridColors = [((9, 235, 238)), ((25, 206, 235)), ((40, 172, 234)), ((16, 142, 233)), ((25, 115, 209)), ((19, 92, 197)), ((12, 59, 170)), ((6, 25, 147)), ((1, 2, 128))]

pg.init()
pg.font.init()
pg.display.set_caption('Dijkstra\'s pathfinding algorithm')

menuText = pg.font.SysFont('Consolas', 32).render('Please select your gamemode', True, (0,0,0))
weightedMode = pg.font.SysFont('Consolas', 32).render('Weighted Grid', True, (0,0,0))
unWeightedMode = pg.font.SysFont('Consolas', 32).render('Unweighted Grid', True, (0,0,0))

clock = pg.time.Clock()
FPS = 144 
blockSize = 10 
cornerPos = [[(x, y) for x in range(0, w, blockSize)] for y in range(0, h , blockSize)]

@dataclass
class Grid():
    def draw_grid(blockSize, initialState):

        for row, x in zip(initialState, range(0, w, blockSize)):
            for col, y in zip(row, range(0, h, blockSize)):
                for k, color in enumerate(gridColors):
                    if col == k:
                        rect = pg.Rect(x, y, blockSize, blockSize)
                        pg.draw.rect(screen, color, rect, blockSize)

    def dijkstra(initialState):
        height, width = len(cornerPos), len(cornerPos[0])
        start = (0,0)
        end = (width - 1, height - 1) 
        queue = [(0, start)]
        shortestPath = []
        origin = np.ones((width, height)) * np.nan

        minDist = defaultdict(lambda:np.infty, {start: 0})
        visited = set() 

        while queue:
            distance, node = heapq.heappop(queue)

            if node == end:
                Grid.draw_grid(blockSize, initialState)
                x = np.int(end[0])
                y = np.int(end[1])
                shortestPath.append([end[0], end[1]])

                while x > 0.0 or y > 0.0:
                    xxyy = np.unravel_index(np.int(origin[np.int(x),np.int(y)]), (height, width))
                    x, y = xxyy[0], xxyy[1]
                    shortestPath.append([np.int(x), np.int(y)])

                    if x == start[0] and y == start[1]:
                        shortestPath.append([0,0])
                        break
                
                for x, y in reversed(shortestPath):
                    rect = pg.Rect(x*blockSize, y * blockSize, blockSize, blockSize)
                    pg.draw.rect(screen, RED, rect, blockSize)
                    pg.display.update()
                    pg.time.wait(25)
                    clock.tick(FPS)
                
                pg.time.wait(10000)
                break

            if node in visited:
                continue

            visited.add(node)
            row, col = node
            rect = pg.Rect(row*blockSize, col * blockSize, blockSize, blockSize)
            pg.draw.rect(screen, RED, rect, blockSize)
            pg.display.update()
            # clock.tick(FPS)

            for neighbor in Grid.get_neighbors(row, col, height, width):
                if neighbor in visited:
                    continue 
            
                nextRow, nextCol = neighbor
                newDist = distance + initialState[nextRow][nextCol] 
                origin[nextRow][nextCol] = np.ravel_multi_index([row, col], (width, height))

                if newDist < minDist[neighbor]:
                    minDist[neighbor] = newDist
                    heapq.heappush(queue, (newDist, neighbor))

    def get_neighbors(row, col, height, width):
        dir = ((1,0),(-1,0),(0,1),(0,-1))
        for dirRow, dirCol in dir:
            rowIterator, colIterator = (row + dirRow, col + dirCol)
            if 0 <= rowIterator < width and 0 <= colIterator < height:
                yield rowIterator, colIterator
    
    def draw_on_click(initialState):
        pos = pg.mouse.get_pos()
        button = pg.mouse.get_pressed()
        if button[0] == True:
            for i, cornerList in enumerate(cornerPos):
                for j, corner in enumerate(cornerList):
                    if (i < len(cornerPos) and j < len(corner)) and (corner[0] <= pos[0]  <= cornerPos[i][j+1][0]) and (pos[1] <= cornerPos[i][j+1][1]):
                        x = cornerPos[i][j][0]
                        y = cornerPos[i-1][j][1]
                        break
                    elif (corner[0] < pos[0] < w) and (corner[1] < pos[1] < h):
                        x = corner[0]
                        y = corner[1]
                else: continue
                break
            cell = pg.Rect(x,y, blockSize, blockSize)
            initialState[int(x/blockSize)][int(y/blockSize)] = 1000000000 
            pg.draw.rect(screen, BLACK, cell)

@dataclass
class Startscreen():
    def menu():
        screen.fill((255,255,255))
        weightedRect = pg.Rect(100, 500, 300, 100)
        unWeightedRect = pg.Rect(600, 500, 300, 100)
        pg.draw.rect(screen, RED, weightedRect)
        pg.draw.rect(screen, RED, unWeightedRect)
        buttonWeighted = weightedMode.get_rect(center = weightedRect.center)
        buttonUnWeighted = unWeightedMode.get_rect(center = unWeightedRect.center)
        screen.blit(menuText, (275, 300))
        screen.blit(weightedMode, buttonWeighted) 
        screen.blit(unWeightedMode, buttonUnWeighted)

    def select_mode(pos):
        if 100 <= pos[0] <= 400 and 500 <= pos[1] <= 600:
            initialState = np.random.randint(1,9, size=(w, h))
            initialState[0][0] = 0
            return initialState, True
        
        elif 600 <= pos[0] <= 900 and 500 <= pos[1] <= 600:
            initialState = np.zeros((w, h))
            initialState[0][0] = 0
            return initialState, True
        
        else: return None, False

def main():
    done = False
    play = False
    modeSelected = False

    while not done:
        if modeSelected == False:
            Startscreen.menu()
            pg.display.update()

        for e in pg.event.get():
            if e.type == pg.KEYDOWN and e.key == pg.K_s: play = True
            if e.type == pg.MOUSEBUTTONUP and e.button == 1 and modeSelected == False:
                mousePos = pg.mouse.get_pos()
                initialState, modeSelected = Startscreen.select_mode(mousePos)

        else: 
            if modeSelected == True:
                Grid.draw_grid(blockSize, initialState)
                Grid.draw_on_click(initialState)
                pg.display.update()

                if play == True:
                    Grid.dijkstra(initialState)
                    pg.display.update()

if __name__ == '__main__':
    main()