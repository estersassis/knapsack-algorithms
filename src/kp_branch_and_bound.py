from dataclasses import dataclass, field
import time
import tracemalloc
import heapq


@dataclass(order=True)
class Node:
    priority: float
    level: int = field(compare=False)
    value: float = field(compare=False)
    weight: float = field(compare=False)
    bound: float
    s: list = field(compare=False, default_factory=list)

class BranchAndBoundAlgorithm:
    def __init__(self, n, W, items):
        self.n = n
        self.W = W
        self.items = items

        self.solution = None
        self.best_value = None

        self.execution_time = None
        self.relative_error = None
        self.timeout = False

    def execute(self):
        tracemalloc.start()
        start_time = time.process_time()
        root = Node(
            priority=0, 
            level=0, 
            value=0, 
            weight=0, 
            bound=self.W*self.items[0][2], 
            s=[]
        )

        queue = []
        heapq.heappush(queue, (root.priority, root.level, root))

        best = 0

        while queue:
            _, _, node = heapq.heappop(queue)
            if node.level == self.n - 1:
                if best < node.value:
                    best = node.value
                    sol = node.s
                    continue
            elif node.bound > best:
                with_node = (
                    node.value + self.items[node.level][1] + 
                    (self.W - node.weight - self.items[node.level][0])* 
                    self.items[node.level + 1][2]
                )

                wout_node = (
                    node.value + (self.W - node.weight)*self.items[node.level + 1][2]
                )

                if node.weight + self.items[node.level][0] <= self.W and with_node > best:
                    next_node = Node(
                        priority=-with_node,
                        level=node.level + 1, 
                        value=node.value + self.items[node.level][1], 
                        weight=node.weight + self.items[node.level][0], 
                        bound=with_node, 
                        s=node.s + [node.level]
                    )
                    heapq.heappush(queue, (next_node.priority, next_node.level, next_node))

                if wout_node > best:
                    next_node = Node(
                        priority=-wout_node,
                        level=node.level + 1,
                        value=node.value,
                        weight=node.weight,
                        bound=wout_node,
                        s=node.s
                    )
                    heapq.heappush(queue, (next_node.priority, next_node.level, next_node))
        
        self.best_value = best
        self.solution = sol

        end_time = time.process_time()
        self.execution_time = end_time - start_time

        current, peak = tracemalloc.get_traced_memory()
        self.memory_usage = peak / (1024 * 1024)  # em megabytes
        tracemalloc.stop()

        return self



# import sys

# if len(sys.argv) < 2:
#     print("Uso: python seu_script.py arquivo")
#     sys.exit(1)

# filename = sys.argv[1]

# n, wmax, items = read_knapsack_file(filename)

# items.sort(key=lambda x: x[2], reverse=True)
# print("Itens: ", items)


# best, sol = bnb_knapsack(items, wmax, n)

# print("Melhor valor:", best)
# print("Itens escolhidos (índices):", sol)