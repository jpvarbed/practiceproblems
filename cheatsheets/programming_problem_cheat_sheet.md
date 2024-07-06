# Tips for Programming Interviews

Some of these are notes from Elements of Programming Interviews from 2016.
In 2024, I went through this [website's problems.](https://takeuforward.org/interviews/blind-75-leetcode-problems-detailed-video-solutions.)
I also like Codewars Katas to just get some basic stuff going.

## Arrays

Consider:
• Use array itself to reduce space
• Write values from the back
• Instead of deleting (which requires moving all entries to the right) consider overwriting it
• Consider reversing the array so the least-significant digit is the first entry
• Be comfortable writing code that operates on subarrays
• It's easy to make off-by-1 errors
• Don't worry about preserving the integrity until it is time to return (sortedness)
• When representing a subset of 1..n allocate an array of size n+1 to simplify indexing
• When operating on 2d arrays, use parallel logic for rows and for columns
Know you library:
• Array is fixed size
• Array<int, 3> A = {1,2,3}
• Vector<int> A = {1 , 2, 3}
• Vector<int> subarray_a(A.begin() +I, A.begin() + j)
• 2d arrays: array<array<int, 2> 3> A = { {1, 2}, {3,4}, {5,6}} vector<vector<int>> A = {{1,2}, {3,4}, {5,6}} 3 rows 2 elements
• Vector uses push_back or emplace_Back
Binary_search, lower_bound, upper_bound, fill, swap, min_element, max_element, reverse, rotate, sort

## Strings

Consider:
• Subtler solutions often use the string itself
• Understand implications of a string type that’s immutable. Array of characters or stringbuilder in java
• Updating mutable strings from the front is slow so see if it's possible to write to the back

## Linked Lists

Consider:
• Use existing nodes to reduce space complexity
• More about cleanly coding what's specified
• Use a dummy head/sentinel to avoid having to check for empty lists
• Update next (and previous) for head and tail
• Algorithms operating on singly linked lists often benefit from using two iterators, one ahead or one advancing quicker

## Stacks And Queues

• Learn when LIFO is useful. Parentheses. Parsing typically benefits from a stack. Function call, undo, memory management.
• FIFO - BFS, task scheduling (round robin), order processing, data buffering (IO Buffers), Producer-consumer problem

## Binary Trees

Hopefully no one ever asks about these. I've never had to think about one.

• A perfect binary tree is a full tree with all leaves at the same depth height h contains 2^h+1 -1 nodes. 2^h are leaves
• A complete binary tree is a tree with all levels except possibly the last filled with nodes as far left as possible. N nodes has height lg n
• A left skewed tree is a tree in which no node has a right child
• A skewed tree has height n
• Consider left-and right-skewed trees when doing complexity analysis. O(h) complexity is O(logn) for balanced and O(n) for skewed trees

## Heaps

Heap (priority queue) is a specialized binary tree. Complete binary tree that satisfy the heap property:
The key at each node is at least as great as the keys stored at its children.

## Searching

• Binary search is key search an interval of real numbers or integers
• If your solution uses sorting and the computation performed after is faster than sorting, look for solutions that do not perform a complete sort.
• Consider time/space tradeoffs such as making multiple passes through the data.

## Hash Tables

• Objects are stored in array locations ("slots") based on the "hash code" of the key.
• The hash code is an integer computed from the key by a hash function.
• Insertion, lookup, and delete have O(1 + n/m) objects / length of array.
• Rehashing is O(n+m).
• Equal keys should have equal hash codes.
• Avoid mutable objects as keys.

## Sorting

• Naïve sorts run in O(n^2) time. Heap, merge and quick run in O(nlogn)
• A well-implemented quick-sort is usually the best choice for sorting
• For less than 10 elts, insertion sort is easier to code and faster.
• Merge sort can be made stable. Add index as an integer rank to the keys to break ties
• If every element is known to be at most k places from its final location, a min-heap can be used to get an O(n log k) algorithm

Two flavors:
1 - use sorting to making subsequent steps simpler.
2 - design a custom sorting routine. For the latter use a structure like a BST, heap or array indexed by values

## Binary Search Tree

Have had to think about these for dbs.

• BSTs offer the ability to search for a key as well as find the min and max elements, look for successor or predecessor of a search key, enumerate the keys in a range in sorted order
• Keys can be added to and deleted from a bst efficiently
• _BST Property_ - The key stored at a node is greater than or equal to the keys stored at the the nodes of its left subtree and less than or equal to the keys stored in the nodes of the right subtree.
• lookup, insertion, and deletion take time proportional to the height of the tree so O(n) but implementations can guarantee O(logn). Red-black trees are widely used in data structure libraries
• Mutable objects will not be updated. Need to delete and re-insert

Consider:
• Can iterate through elements in sorted order in O(n) time regardless of balance
• Combo of BST and a hashtable. Help lookup (still need to delete/insert to update)
• Augment a bst. Number of nodes at a subtree, range of values sorted in the subtree
• Bst property is a global property. A binary tree may have the property that each node's key is greater than the key at its left child and smaller than the key at its right child, but it may not be a BST

## Recursion

Also have never had to do recursion.
Recursion is a method where the solution to a problem depends partially on solutions to smaller instances of related problems.
Greatest common divisor (GCD) if y > x, the GCD of x and y is the GCD of x and y-x O(log max(x,y)) O(n) n is the number of bits needed to represent the inputs. Space complexity is O(n) max call stack

Consider
• Suitable when input is expressed using recursive rules
• Good choice for search, enumeration, and divide-and-conquer
• Alternative to deeply nested iteration loops
• To remove recursion use stack data structure
• If called with same arguments more than once, cache the results (dynamic programming)

## Dynamic Programming

Have used cache. Never dynamic programming in wild.

General technique for solving optimization, search, and counting problems that can be decomposed into subproblems
Consider using dp whenever you have to make choices to arrive at the solution, specifically, when the solution relates to subproblems.
Key to solving a dp problem into subproblems such that:
-the original problem can be solved relatively easily once solutions to the sub-problems are solved
-these subproblem solutions are cached

Maximum subarray
Take L and R. Maximum subarray for A is the maximum of L+r, last entry or L, first entry of r.
Apply DP. Store A[0:i] max sum and keep index. O(n)

Mistake: think of the recursive case by splitting the problem into two equal halves. In most cases, these two subproblems are not sufficient to solve the original problem
Make sure combining solutions to subproblem does yield a solution

Consider:
• When you have to make choices to arrive at the solution
• Applicable to counting and decision problems. Any problem where you can express a solution recursively in terms of the same computation on smaller instances
• Often for efficiency the cache is built "bottom-up" i.e. iteratively
• To save space, cache space maybe recycled once it is known that a set of entries will not be looked up again
• Sometimes recursion can out-perform a bottom-up DP solution e.g. when the solution is found early or subproblems can be pruned through bounding

## Greedy Algorithms and Invariants

An algorithm that computes a solution in steps; at each step the algorithm makes a decision that is locally optimum, and never changes that decision

Consider:
• A greedy algorithm is often the right choice for an optimization problem where there's a natural set of choices to select from
• It's often easiest to conceptualize a greedy algorithm recursively, and then implement it using iteration for higher perf
• It can give insights into the optimum algorithm
• Sometimes the right greedy choice is not obvious

## Graphs

A graph is a set of vertices connected by edges
DAG- directed acyclic graph is a graph with no cycles.
Cycles - paths which contain one or more edges and which begin and end at the same vertex
Sources- vertices which have no incoming edges
Sinks- vertices which have no outgoing edges
Topological ordering- is an ordering of the vertices in which each edge is from a vertex earlier in the ordering to a vertex later in the ordering

Connected- a path exists between u and v
Connected component- maximal set of vertices C such that each pair of vertices in C is a connected in G. Every vertex belongs to exactly 1 connected component
Directed graph is weakly connected- if replacing all directed edges with undirected makes it connected
Connected if for every u,v a u->v or v->u path exists
Strongly connected if u->v and v->u exist

Adjacency list or adjacency matrix
Tree is a special sort of graph, undirected graph that is connected but has no cycles

Ideal for modeling and analyzing relationships between pairs of objects
Consider:
• It's natural to use when the problem involves spatially connected objects.
• Whenever you have to analyze any binary relationship. e.g. interlinked webpages followers
• Analyzing a structure e.g. looking for cycles or connected components. DFS works well
• Optimization. BFS, dijkstra's, minimum spanning tree
BFS/DFS: O(V+E) space O(V) in worst case
BFS can be used to compute distances from the start vertex
DFS can be used to check for the presence of cycles
