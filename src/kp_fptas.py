import time
import asyncio


class FPTASAlgorithm:
    def __init__(self, n, W, items, epsilon):
        self.n = n
        self.W = W
        self.items = items
        self.epsilon = epsilon

        self.best_value = None

        self.execution_time = None
        self.relative_error = None
        self.timeout = False

    async def execute(self):
        start_time = time.process_time()

        values = [item[1] for item in self.items]   # v
        weights = [item[0] for item in self.items]  # w
        
        vmax = max(values)
        K = (self.epsilon * vmax) / self.n
        
        scaled_values = [int(v // K) for v in values]
        
        max_scaled_value = sum(scaled_values)
        
        dp = [float('inf')] * (max_scaled_value + 1)
        dp[0] = 0
        
        for i in range(self.n):
            for v in range(max_scaled_value, scaled_values[i]-1, -1):
                if dp[v - scaled_values[i]] + weights[i] <= self.W:
                    dp[v] = min(dp[v], dp[v - scaled_values[i]] + weights[i])
                await asyncio.sleep(0)
            await asyncio.sleep(0)
        
        for v in range(max_scaled_value, -1, -1):
            if dp[v] <= self.W:
                best_scaled_value = v
                break
            await asyncio.sleep(0)
        
        approx_value = best_scaled_value * K
        self.best_value = approx_value

        end_time = time.process_time()

        self.execution_time = end_time - start_time
        dp_size = len(dp)
        self.memory_usage = (dp_size * 24)

        return self