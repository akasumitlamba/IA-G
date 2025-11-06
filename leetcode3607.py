"""
3607. Power Grid Maintenance

Problem (shortened):
You are given c power stations (IDs 1..c) and n bidirectional connections between them. Stations that are connected (directly or indirectly) form a power grid (connected component).

Initially all stations are online. You receive queries of two types:
  [1, x] => maintenance check requested for station x:
            - If x is online -> x resolves the check (answer x)
            - If x is offline -> the operational station with the smallest id in x's grid resolves it
              If no operational station remains in that grid, answer -1.
  [2, x] => station x goes offline (becomes non-operational) but remains part of the grid (connectivity unchanged)

Return the answers to all type-1 queries in order.

Constraints:
 1 <= c <= 10^5
 0 <= n <= min(10^5, c*(c-1)/2)
 1 <= queries.length <= 2*10^5

Example:
 c = 5
 connections = [[1,2],[2,3],[3,4],[4,5]]
 queries = [[1,3],[2,1],[1,1],[2,2],[1,2]]
 Output: [3,2,3]

This file contains a clear, commented, step-by-step solution that builds connected components using
Union-Find (disjoint set union), stores candidate online nodes per component in a min-heap,
and answers queries by checking online status and popping stale/offline nodes from the heap.

Time complexity (amortized): roughly O((c + q) * alpha(c) + total_heap_operations * log c)
where q = number of queries and alpha is inverse-Ackermann (very small). Space O(c).
"""

from collections import defaultdict
import heapq
from typing import List


class Solution:
    def processQueries(self, c: int, connections: List[List[int]], queries: List[List[int]]) -> List[int]:
        """
        Process the queries described in the problem statement.

        Approach (step-by-step):
        1. Use Union-Find (disjoint set) to compute connected components of the c nodes.
           - parent[i] is the representative (root) of node i's component.
        2. For each node i (1..c), push i into a min-heap associated with its component root.
           - We keep all node ids in the heap; when a node goes offline we do not remove it from the heap
             immediately (that would be expensive). Instead, when answering queries we lazily pop
             offline/stale elements from the heap top until the minimal id is actually online.
        3. Maintain an array `online` where online[i] == 1 means node i is currently online; 0 otherwise.
        4. For each query:
           - If it's type 1 (maintenance check x):
               a) If x is online -> return x.
               b) Else -> look at the heap for component(find(x)). Pop while the heap has elements
                           and the top is offline (stale). If heap becomes empty -> return -1.
                           Otherwise return the top (smallest online id in the component).
           - If it's type 2 (take x offline): set online[x] = 0. Do NOT remove from heap now.

        The key trick is lazy deletion from per-component min-heaps to keep operations efficient.
        """

        # --- 1) Build Union-Find parent array ---
        parent = list(range(c + 1))  # 1-based indexing, parent[0] unused

        def find(x: int) -> int:
            # Iterative find with path compression
            while x != parent[x]:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x: int, y: int) -> None:
            rx, ry = find(x), find(y)
            if rx != ry:
                # attach ry under rx (no rank heuristics needed for correctness)
                parent[ry] = rx

        # Union all given connections
        for u, v in connections:
            union(u, v)

        # --- 2) Prepare a min-heap for each component containing its node ids ---
        components = defaultdict(list)  # root_id -> heap(list) of node ids
        for i in range(1, c + 1):
            root = find(i)
            heapq.heappush(components[root], i)

        # --- 3) Track online/offline state ---
        online = [1] * (c + 1)  # 1 if online, 0 if offline; 1-based indexing

        results: List[int] = []

        # --- 4) Process queries ---
        for typ, x in queries:
            if typ == 1:
                # maintenance check
                if online[x] == 1:
                    # x is online and resolves the check by itself
                    results.append(x)
                else:
                    # x is offline: find smallest online node in its component
                    root = find(x)
                    heap = components[root]

                    # lazy removal: pop any top elements that are currently offline
                    while heap and online[heap[0]] == 0:
                        heapq.heappop(heap)

                    if heap:
                        results.append(heap[0])
                    else:
                        results.append(-1)
            else:
                # typ == 2: take x offline
                online[x] = 0

        return results


if __name__ == '__main__':
    # Example 1
    c = 5
    connections = [[1, 2], [2, 3], [3, 4], [4, 5]]
    queries = [[1, 3], [2, 1], [1, 1], [2, 2], [1, 2]]
    print('Example 1 output ->', Solution().processQueries(c, connections, queries))

    # Example 2
    c = 3
    connections = []
    queries = [[1, 1], [2, 1], [1, 1]]
    print('Example 2 output ->', Solution().processQueries(c, connections, queries))
