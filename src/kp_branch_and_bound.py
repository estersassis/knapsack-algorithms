from dataclasses import dataclass, field
import time
from queue import PriorityQueue
import sys


@dataclass(order=True)
class Node:
    level: int = field(compare=False)
    value: float = field(compare=False)
    weight: float = field(compare=False)

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

    def bound(self, node):
        if node.weight >= self.W:
            return 0

        value_bound = node.value
        j = node.level + 1
        total_weight = node.weight

        while j < self.n and total_weight + self.items[j][0] <= self.W:
            total_weight += self.items[j][0]
            value_bound += self.items[j][1]
            j += 1

        if j < self.n:
            value_bound += int((self.W - total_weight) * self.items[j][2])

        return value_bound

    def execute(self):
        start_time = time.process_time()
        max_queue_size = 0

        best_value = 0

        priority_queue = PriorityQueue()
        root = Node(-1, 0, 0)
        priority_queue.put(root)

        while not priority_queue.empty():
            node = priority_queue.get()

            current_size = priority_queue.qsize()
            if current_size > max_queue_size:
                max_queue_size = current_size

            if node.level == self.n - 1:
                if best < node.value:
                    best = node.value
                    continue
            
            next_node = Node(
                node.level + 1,
                node.value + self.items[node.level + 1][1], 
                node.weight + self.items[node.level + 1][0]
            )

            if next_node.weight <= self.W and next_node.value > best_value:
                best_value = next_node.value

            with_node = self.bound(next_node)
            if with_node > best_value:
                priority_queue.put(next_node)

            next_node = Node(
                node.level + 1, 
                node.value, 
                node.weight
            )
            wout_node = self.bound(next_node)
            if wout_node > best_value:
                priority_queue.put(next_node)


        self.best_value = best_value

        end_time = time.process_time()

        self.execution_time = end_time - start_time
        self.memory_usage = sys.getsizeof(node) * max_queue_size

        return self