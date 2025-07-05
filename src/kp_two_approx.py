import time
import tracemalloc


class TwoApproxAlgorithm:
    def __init__(self, n, W, items):
        self.n = n
        self.W = W
        self.items = items

        self.best_value = None

        self.execution_time = None
        self.relative_error = None
        self.timeout = False

    def execute(self):
        tracemalloc.start()
        start_time = time.process_time()

        total_value = 0
        total_weight = 0

        # etapa gulosa
        for w, v, _ in self.items:
            if total_weight + w <= self.W:
                total_weight += w
                total_value += v

        # maior item isolado que cabe
        max_single_value = max(
            (v for w, v, _ in self.items if w <= self.W),
            default=0
        )

        # retorna o melhor dos dois
        self.best_value = max(total_value, max_single_value)

        end_time = time.process_time()
        self.execution_time = end_time - start_time

        current, peak = tracemalloc.get_traced_memory()
        self.memory_usage = peak / (1024 * 1024)  # em megabytes
        tracemalloc.stop()

        return self