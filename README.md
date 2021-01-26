# 8-puzzle
8 puzzle solver using BFS, DFS, IDDFS and A-star algorithm

*It is assumed that goal state is:*
    
     0 1 2
     3 4 5
     6 7 8
#### Usage
You can run `main.py` with the name of algorithm - which is `ast` for A*, `bfs`, or `dfs`, or `ids` for iterative deepening dfs - as the first argument and initial state as the second one:
```
$ python main.py bfs 1,2,5,3,4,0,6,7,8
$ python main.py dfs 1,2,5,3,4,0,6,7,8
$ python main.py ids 1,2,5,3,4,0,6,7,8
$ python mian.py ast 1,2,5,3,4,0,6,7,8
```
Solution and details will be saved to ```{alg-name}_output.txt```.
