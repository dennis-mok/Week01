# -*- coding: utf-8 -*-
"""COMP9418_W01_Graph_Representation_Traversal_MST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/dennis-mok/Week01/blob/main/COMP9418_W01_Graph_Representation_Traversal_MST.ipynb

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/UNSW-COMP9418/Week01/blob/main/COMP9418_W01_Graph_Representation_Traversal_MST.ipynb)

# Graph Representation, Traversal and MST

**COMP9418-21T3, W01 Tutorial**

- Instructor: Gustavo Batista
- School of Computer Science and Engineering, UNSW Sydney
- Notebook designed by Gustavo Batista and Jeremy Gillen
- Last Update 18th August 2021
"""



"""In this week's tutorial, we will review some concepts an algorithms for graph representation, traversal and Minimum Spanning Trees (MST) that will be useful during the course.

## Technical prerequisites

We will use Jupyter Notebooks in the practical part of the tutorials. There are three main ways to run these notebooks:

1. *Google Colab*. The links available in WebCMS will open the course notebooks in [Google Colab](https://colab.research.google.com/). Google Colab has all the packages necessary to run these notebooks, so no installation is required. **This is our prefered approach**.

2. *CSE VLAB*. We have installed the necessary packages in the CSE computers. You have to copy the notebook to your CSE account in VLAB to execute them. There are two possibilities to access VLAB. The most recommended is installing a [VNC software](https://taggi.cse.unsw.edu.au/FAQ/Really_quick_guide_to_VLAB/) in your computer. Alternatively, you can access these computers through a web interface using [CSE VLAB Gateway](https://vlabgateway.cse.unsw.edu.au/).

3. *Your computer*. If you do not have Jupyter installed in your computer, we recommend installing [Anaconda](https://www.anaconda.com/distribution). Anaconda conveniently installs Python, the Jupyter Notebook, and other commonly used packages for scientific computing and data science. To render a graphical visualization of some graphs in this notebook, you also need to [install Graphviz](http://www.graphviz.org/download). If you have conda installed in your computer, you can try the command ```conda install python-graphviz``` directly. From our experience, Graphviz is a little troublesome to install in some systems. For instance, ```conda install python-graphviz``` often does not work on Linux systems and we did not have any success using ```pip3 install graphviz``` on most systems, so do *not* use ```pip3```.

Once we have done all that, we import Graphviz, and heapq modules for later use.
"""

# Visualise our graph
import graphviz
# Priority queue for Prim algorithm
import heapq as pq


"""## Graph class

To keep our code clean and put all of the graph related functions in one place,
we can wrap this graph data structure in a class.
"""

class Graph:
    def __init__(self, adj_list=None):
        self.adj_list = dict()
        if adj_list is not None:
            self.adj_list = adj_list.copy() # dict with graph's adjacency list
        self.colour = dict()

class Graph(Graph):
    def show(self, directed=True, positions=None):
        """
        Prints a graphical visualisation of the graph usign GraphViz
        arguments:
            `directed`, True if the graph is directed, False if the graph is undirected
            `pos: dictionary`, with nodes as keys and positions as values
        return:
            GraphViz object
        """
        if directed:
            dot = graphviz.Digraph(engine="neato", comment='Directed graph')
        else:
            dot = graphviz.Graph(engine="neato", comment='Undirected graph', strict=True)        
        dot.attr(overlap="false", splines="true")
        for v in self.adj_list:
            if positions is not None:
                dot.node(str(v), pos=positions[v])
            else:
                dot.node(str(v))
        for v in self.adj_list:
            for w in self.adj_list[v]:
                dot.edge(str(v), str(w))

        return dot

"""## Depth-first search

Let's implement the DFS search. We will provide the code for you. Later on, you will extend it to implement other algorithms. We will use a colouring scheme for nodes. 

Initially, all nodes are "white" indicating they are not processed yet. When we first visit a node, we recolour it as "grey". Finally, the node becomes "black" when we have processed all its outgoing edges, and we are ready to backtrack to the previous node.
"""

class Graph(Graph):
    def _dfs_r(self, v): # This is the main DFS recursive function
        """
        argument 
        `v`, next vertex to be visited
        `colour`, dictionary with the colour of each node
        """
        print('Visiting: ', v)
        self.colour[v] = 'grey' # Visited vertices are coloured 'grey'
        for w in self.adj_list[v]: # Let's visit all outgoing edges from v
            if self.colour[w] == 'white': # To avoid loops, we check if the next vertex hasn't been visited yet
                self._dfs_r(w)
        self.colour[v] = 'black' # When we finish the for loop, we know we have visited all nodes from v. It is time to turn it 'black'

    def dfs(self, start): # This is an auxiliary DFS function to create and initialize the colour dictionary
        """
        argument 
        `start`, starting vertex
        """    
        self.colour = {node: 'white' for node in self.adj_list.keys()} # Create a dictionary with keys as node numbers and values equal to 'white'
        self._dfs_r(start)
        return self.colour # We can return colour dictionary. It is useful for some operations, such as detecting connected components

"""A modification of the algorithm can make sure it searches all nodes, even if they are disconnected from other nodes. The idea is to re-start the recursive DFS search for each white node until all nodes become black."""

class Graph(Graph):
    def dfs_all(self): # This is an auxiliary DFS function to create and initialize the colour dictionary
        """
        argument 
        `start`, starting vertex
        """    
        self.colour = {node: 'white' for node in self.adj_list.keys()} # Create a dictionary with keys as node numbers and values equal to 'white'
        for start in self.colour.keys():
            if self.colour[start] == 'white':
                self._dfs_r(start)


"""## Finding Cycles in Directed Graphs

Our second task is to determine if a graph has cycles. During a DFS, a cycle can be found by testing if we have reached a grey node. Usually, we stop when we first observe a cycle. Therefore, we need to modify the DFS procedure to return a boolean.

### Exercise

Now, it is your turn, modify the code bellow to detect cycles in directed graphs.
"""

class Graph(Graph):
    # This is the main recursive function
    def _find_cycle_r(self, v):
        """
        argument 
        `v`, next vertex to be visited
        """      
        print('Visiting: ', v)
        
        # insert your code here
        # print a debug message such as
        # print(v, w, 'Cycle detected')
        # when you detect a cycle. 

        self.colour[v] = 'grey' # Visited vertices are coloured 'grey'
        for w in self.adj_list[v]: # Let's visit all outgoing edges from v
            if self.colour[w] == 'grey':
                print(v, w, 'Cycle detected')
                return True

            elif self.colour[w] == 'white': # To avoid loops, we check if the next vertex hasn't been visited yet
                self._find_cycle_r(w)
        self.colour[v] = 'black' # When we finish the for loop, we know we have visited all nodes from v. It is time to turn it 'black'

        return False

    # This is an auxiliary function to create and initialize the colour dictionary    
    def find_cycle(self):
        """
        argument 
        `v`, starting vertex
        """        
        self.colour = dict([(node, 'white') for node in self.adj_list.keys()])
        for start in self.colour.keys():
            if self.colour[start] == 'white':
                if self._find_cycle_r(start):
                    return True
                else:
                    return self._find_cycle_r(start)
"""
# Topological Sort

The topological sort can be obtained by merely inserting the nodes into a stack when they become black. We use the stack to reverse the order of the nodes when printing the result. By doing so, the edges are directed from left to right.

## Exercise

Let's implement the topological sort. It is an almost trivial modification of your DFS procedure. We have started the code for you creating a stack to store the sorted nodes.
"""

class Graph(Graph):
    # This is the recursive function that visits the nodes according to depth-first search and appends the black nodes 
    # to the end of a `stack` list.
    def _topological_sort_r(self, v):
        """
        argument 
        `v`, current vertex
        """
        
        # TODO: Fill in this function
        self.colour[v] = 'grey' # Visited vertices are coloured 'grey'
        for w in self.adj_list[v]: # Let's visit all outgoing edges from v
            if self.colour[w] == 'white': # To avoid loops, we check if the next vertex hasn't been visited yet
                self._topological_sort_r(w)
        self.colour[v] = 'black' # When we finish the for loop, we know we have visited all nodes from v. It is time to turn it 'black'
        self.stack.append(v)
        
        
    # This is main function that prepares for the recursive function. It first colours all nodes as 'white' and call the
    # recursive function for an arbitrary node. When the recursive function returns, if we have any remaining 'white'
    # nodes, we call the recursive function again for these nodes.
    def topological_sort(self):
        """
        argument 
        `G`, an adjacency list representation of a graph
        return a list with the topological order of the graph G
        """
        # We start with an empty stack
        self.stack = []
        # Colour is dictionary that associates node keys to colours. The colours are 'white', 'grey' and 'black'.
        self.colour = {node: 'white' for node in self.adj_list.keys()}
        # We call the recursive function to visit a first node. When the function returns, if there are any white 
        # nodes remaining, we call the function again for these white nodes
        for start in self.adj_list.keys():
            # If the node is 'white' we call the recursive function to vists the nodes connected to it in DFS order
            if self.colour[start] == 'white':
                # This is a call to topologicalSort_r
                self._topological_sort_r(start)
        # We need to reverse the list, we use a little trick with list slice
        return self.stack[::-1]

"""# Transpose Graph

Transposition is an operation over a directed graph $G$ that results in another directed graph on the same set of vertices with all of the edges reversed. The following figure illustrates this process, with a graph $G$ on the left side and its transpose $G^T$ on the right side:

![Transpose graph](img/Transpose_graph.png "Transpose Graph")


## Exercise

Implement the transpose operation over our graph representation. Take a graph as input and produce its transpose as output.
"""

class Graph(Graph):
    def transpose(self):
        """
        argument 
        `G`, an adjacency list representation of a graph
        """      
        gt = dict((v, []) for v in self.adj_list)
        # TODO
        for v in self.adj_list:
            to_v = self.adj_list[v]
            for t in to_v:
                gt[t].append(v)

        return Graph(gt)

"""# Minimum Spanning Trees

Minimum spanning tree (MST) is an operation on weighted undirected graphs. We receive a graph $G=(V,E)$ and we should return the spanning tree of $G$ that has a minimum cost.

A spanning tree is a graph with the same set of vertices $V$ of $G$, but with potentially fewer edges. A spanning tree is a graph with no cycles. If $G$ has $n$ edges, its spanning tree must have $n-1$ edges.

The minimum spanning tree is the spanning tree whose sum of edge weights is the smallest among all spanning trees.

The next figure shows a weighted undirect graph is its corresponding MST.

![MST](img/spanning_tree.png "MST")

Let's start by augmenting our graph representation to allow weighted edges, and adding methods to allow us to easily add nodes and edges to the graph. For later convenience, we will also add functions to remove nodes, iterate over all nodes, and get the children of a node.
"""

class Graph(Graph):
    def __init__(self, adj_list=None):
        self.adj_list = dict()
        if adj_list is not None:
            self.adj_list = adj_list.copy() # dict with graph's adjacency list
        self.colour = dict()
        self.edge_weights = dict() # maps a tuple (node1, node2) to a number

    def __len__(self):
        '''
        return the number of nodes in the graph
        '''
        return len(self.adj_list.keys())

    def __iter__(self):
        '''
        Let a user iterate over the nodes of the graph, like:
        for node in graph:
            print(node)
        '''
        return iter(self.adj_list.keys())
    
    def children(self, node):
        '''
        Return a list of children of a node
        '''
        return self.adj_list[node]

    def add_node(self, name):
        '''
        This method adds a node to the graph.
        '''
        if name not in self.adj_list:
            self.adj_list[name] = []

    def remove_node(self, name):
        '''
        This method removes a node, and any edges to or from the node
        '''
        for node in self.adj_list.keys():
            if name in self.adj_list[node]:
                self.adj_list[node].remove(name)
        del self.adj_list[name]

    def add_edge(self, node1, node2, weight=1, directed=True):
        '''
        This function adds an edge. If directed is false, it adds an edge in both directions
        '''
        # in case they don't already exist, add these nodes to the graph
        self.add_node(node1)
        self.add_node(node2)
        
        self.adj_list[node1].append(node2)
        self.edge_weights[(node1,node2)] = weight
        
        if not directed:
            self.adj_list[node2].append(node1)
            self.edge_weights[(node2,node1)] = weight


"""## Exercise

Now, let's implement the Prim algorithm. The general idea is to start the search from a node `s`. Initially, only nodes directly connected to `s` are considered. We use a priority queue to sort these nodes according to the edge weight. The priority queue is implementated with a binary heap data structure using Python's [heapq](https://docs.python.org/3/library/heapq.html) module. The node `u` with the smallest cost connecting to `s` is removed from the priority queue and inserted into the MST. The search expands to include the vertices that directly connect to `u`. These nodes are inserted into the priority queue, and the procedure repeats according to the following algorithm:

![Prim](img/Prim.png "MST")

Notice that `S` maintains the nodes currently in the MST. It is crucial to avoid inserting the same node twice since it would create a cycle. 

We have created a stub for you. You need to complete the gaps where there is an ellipsis.
"""

class Graph(Graph):
    def prim(self, start):
        """
        argument 
        `start`, start vertex
        """      
        # Intialise set 'visited' with vertex s
        visited = {start}
        # Initialise priority queue Q with an empty list
        Q = []
        # Initilise list tree with empty Graph object. This object will have the MST at the end of the execution
        tree = Graph()
        # Initialise the priority queue Q with outgoing edges from s
        for e in self.adj_list[start]:
            # There is a trick here. Python prioriy queues accept tuples but the first entry of the tuple must be the priority value
            edge = (start, e)
            weight = self.edge_weights[edge]
            pq.heappush(Q, (weight, start, e))
        while len(Q) > 0:
            # Remove element from Q with the smallest weight
            weight, v, u = pq.heappop(Q)
            # If the node is already in 'visited' we cannot include it in the MST since it would create a cycle
            if u not in visited:
                # Let's grow the MST by inserting the vertex in visited
                visited.add(u)
                # Also we insert the edge in tree
                tree.add_edge(v, u, weight=weight,directed=False)
                # We iterate over all outgoing edges of u
                for e in self.adj_list[u]:
                    # We are interested in edges that connect to vertices not in 'visited' and with smaller weight than known values stored in a
                    if e not in visited:
                        # Edge e is of interest, let's store in the priority queue for future analysis
                        edge = (u, e)
                        w = self.edge_weights[edge]
                        pq.heappush(Q, (w, u, e))        
        return tree



