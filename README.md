Non-Partisan Travelling Senator Problem
=====
The non-partisan travelling senator problem has the same goals as the traveling salesman problem (to find the ordering of cities that minimizes the distance traveled to those cities) with the addition of some constraints outlined below.

In the non-partisan travelling senator problem (NPTSP), each city also has a color, either RED or BLUE,
and the path cannot visit more than three cities of the same color consecutively. You still want the
cheapest such path that visits every city exactly once.
More specifically, you are given a complete, undirected, weighted graph on N cities. The cities are labeled
from 1 to N. The graph is given to you in adjacency matrix format, that is you will recieve an N ×N matrix,
where the entry in the ith row and jth column represents the edge weight between city i and city j. You are
also given a string of length N representing the colors of the cities. The ith character of the string is R if
the city is red, and B otherwise.

Constraints:
	The number of verticies will be an even integer from 1 and 50, inclusive
	The edge weights will be an integer between 1 and 100, inclusive.

To run the program, simply run ```python solution.py numInputs``` where numInputs is the number of instances of TSP you want to solve for (you can see these in the /instances directory)