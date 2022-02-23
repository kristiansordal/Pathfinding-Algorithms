# Pathfinding Algorithms

This is a collection (so far only one) of pathfinding algorithms. A pathfinding algorithm is an algorithm which finds the shortest path betweem two points on a grid or a graph.

## Contents

In this repository you will find different collections of pathfinding algorithms, visualized with Pygame. For now I've only implemented Dijkstra's pathfinding algorithm.

### How it works

When you run the script, a window will appear, and you will be prompted with a selection between two different gamemodes. In both gamemodes, you will be able to use your mouse to draw walls and mazes.

**Weighted Mode**: This works by assigning different "weights" to each node in the grid, darker colors have heigher weights, lighter colors have lighter weights. You can think of it as the resitance it takes to go through each node.

**Unweighted Mode**: Here the nodes have no assigned weight, the point of this gamemode is to draw your own walls, to see how the algorithm reacts.

### TODO

I'm planning on implementing a maze generator, as it would be very intresting to see the algorithm solve a randomly generated maze.
