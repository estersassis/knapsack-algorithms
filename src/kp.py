import math
import time
import asyncio
from src.kp_branch_and_bound import BranchAndBoundAlgorithm
from src.kp_fptas import FPTASAlgorithm
from src.kp_two_approx import TwoApproxAlgorithm
from concurrent.futures import ProcessPoolExecutor, TimeoutError


class KnapsackProblem:
    def __init__(self, file_path: str, optimal_file):
        self.file_path = file_path
        self.optimal_file = optimal_file
        self.timeout = 1800

        self.n = None
        self.W = None
        self.items = None

        self.branch_and_bound_algorithm = None
        self.fptas_algorithms = {}
        self.two_approx_algorithm = None

        self.read_items()

    def read_items(self):
        with open(self.file_path, 'r') as f:
            parts = f.readline().strip().split()
            self.n = int(parts[0])
            self.W = float(parts[1])

            self.items = []
            for _ in range(self.n):
                parts = f.readline().strip().split()
                v = float(parts[0])
                w = float(parts[1])
                self.items.append((w, v, v/w))
        
        self.items.sort(key=lambda x: x[2], reverse=True)
    
    from concurrent.futures import ProcessPoolExecutor, TimeoutError

    async def run_algorithms(self):
        async def execute_with_timeout(algorithm_instance, name):
            try:
                print(f"Starting {name}...")
                start_time = time.perf_counter()
                await asyncio.wait_for(algorithm_instance.execute(), timeout=self.timeout)
                print(f"{name} completed in {time.perf_counter() - start_time:.2f} seconds")
            except asyncio.TimeoutError:
                print(f"{name} timeout after {self.timeout} seconds")
                algorithm_instance.timeout = True

        self.branch_and_bound_algorithm = BranchAndBoundAlgorithm(self.n, self.W, self.items)
        epsilons = [0.8, 0.5, 0.1]
        self.fptas_algorithms = {
            eps: FPTASAlgorithm(self.n, self.W, self.items, epsilon=eps)
            for eps in epsilons
        }
        self.two_approx_algorithm = TwoApproxAlgorithm(self.n, self.W, self.items)

        print("Running algorithms...")

        await asyncio.gather(
            execute_with_timeout(self.branch_and_bound_algorithm, "BranchAndBound"),
            execute_with_timeout(self.fptas_algorithms[0.8], "FPTAS ε=0.8"),
            execute_with_timeout(self.fptas_algorithms[0.5], "FPTAS ε=0.5"),
            execute_with_timeout(self.fptas_algorithms[0.1], "FPTAS ε=0.1"),
            execute_with_timeout(self.two_approx_algorithm, "TwoApprox"),
        )

    def calculate_relative_error(self):
        with open(self.optimal_file, 'r') as file:
            optimal_value = float(file.readline().strip())

        # branch and bound
        if self.branch_and_bound_algorithm and not self.branch_and_bound_algorithm.timeout:
            bv = self.branch_and_bound_algorithm.best_value
            if bv is not None:
                self.branch_and_bound_algorithm.relative_error = (
                    (optimal_value - bv) / optimal_value
                )
            else:
                self.branch_and_bound_algorithm.relative_error = None

        # fptas
        for eps, algo in self.fptas_algorithms.items():
            if algo and not algo.timeout:
                bv = algo.best_value
                if bv is not None:
                    algo.relative_error = (optimal_value - bv) / optimal_value
                else:
                    algo.relative_error = None

        # twoapprox
        if self.two_approx_algorithm and not self.two_approx_algorithm.timeout:
            bv = self.two_approx_algorithm.best_value
            if bv is not None:
                self.two_approx_algorithm.relative_error = (
                    (optimal_value - bv) / optimal_value
                )
            else:
                self.two_approx_algorithm.relative_error = None

    def generate_result_file(self, file_name, results_folder):
        self.calculate_relative_error()

        with open(f"{results_folder}/{file_name}.result", 'w') as file:
            file.write(f"Instance: {file_name}\n")
            
            for algorithm_name, algorithm_obj in {
                "Branch and Bound Algorithm": self.branch_and_bound_algorithm,
                **{f"FPTAS Algorithm (ε={eps})": algo for eps, algo in self.fptas_algorithms.items()},
                "Two Approx Algorithm": self.two_approx_algorithm,
            }.items():
                if algorithm_obj is not None:
                    file.write(f"\n--- {algorithm_name} ---\n")
                    if algorithm_obj.timeout:
                        file.write(f"Best Value: NA\n")
                        file.write(f"Execution Time: NA\n")
                        file.write(f"Memory Usage: NA\n")
                        file.write(f"Relative Error: NA\n")
                    else:
                        file.write(f"Best Value: {algorithm_obj.best_value:.4f}\n")
                        file.write(f"Execution Time: {algorithm_obj.execution_time:.4f} seconds\n")
                        file.write(f"Memory Usage: {algorithm_obj.memory_usage} bytes\n")
                        file.write(f"Relative Error: {algorithm_obj.relative_error:.4f}\n")
