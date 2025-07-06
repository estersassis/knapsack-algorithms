import time
import asyncio
import resource


class TwoApproxAlgorithm:
    def __init__(self, n, W, items):
        self.n = n
        self.W = W
        self.items = items

        self.best_value = None

        self.execution_time = None
        self.relative_error = None
        self.timeout = False

    async def execute(self):
        start_time = time.process_time()

        total_value = 0
        total_weight = 0

        for w, v, _ in self.items:
            if total_weight + w <= self.W:
                total_weight += w
                total_value += v
            await asyncio.sleep(0)

        max_single_value = max(
            (v for w, v, _ in self.items if w <= self.W),
            default=0
        )

        self.best_value = max(total_value, max_single_value)

        end_time = time.process_time()

        self.execution_time = end_time - start_time
        self.memory_usage = 72  # não aloca memória adicional significativa além de algumas variáveis escalares

        return self