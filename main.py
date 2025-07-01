from dataclasses import dataclass, field
from decimal import Decimal, getcontext
import heapq

getcontext().prec = 10


@dataclass(order=True)
class Node:
    priority: Decimal
    level: int = field(compare=False)
    value: Decimal = field(compare=False)
    weight: Decimal = field(compare=False)
    bound: Decimal
    s: list = field(compare=False, default_factory=list)


def bnb_knapsack(items, W, n):
    root = Node(
        priority=0, 
        level=0, 
        value=0, 
        weight=0, 
        bound=W*items[0][2], 
        s=[]
    )

    queue = []
    heapq.heappush(queue, root)

    best = 0

    while queue:
        node = heapq.heappop(queue)
        if node.level == n-1:
            if best < node.value:
                best = node.value
                sol = node.s
                continue
        elif node.bound > best:
            with_node = (
                node.value + items[node.level][1] + 
                (W - node.weight - items[node.level][0])* 
                items[node.level + 1][2]
            )

            wout_node = (
                node.value + (W - node.weight)*items[node.level + 1][2]
            )

            if node.weight + items[node.level][0] <= W and with_node > best:
                heapq.heappush(queue, 
                    Node(
                        priority=-with_node,
                        level=node.level + 1, 
                        value=node.value + items[node.level][1], 
                        weight=node.weight + items[node.level][0], 
                        bound=with_node, 
                        s=node.s + [node.level]
                    )
                )
            if wout_node > best:
                heapq.heappush(queue, 
                    Node(
                        priority=-wout_node,
                        level=node.level + 1,
                        value=node.value,
                        weight=node.weight,
                        bound=wout_node,
                        s=node.s
                    )
                )
    return best, sol

def read_knapsack_file(filepath):
    with open(filepath, 'r') as f:
        parts = f.readline().strip().split()
        n = int(parts[0])
        wmax = Decimal(parts[1])

        items = []
        for _ in range(n):
            parts = f.readline().strip().split()
            v = Decimal(parts[0])
            w = Decimal(parts[1])
            items.append((w, v, v/w))

    return n, wmax, items

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