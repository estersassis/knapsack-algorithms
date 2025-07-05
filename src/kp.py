import math
import time
import threading
from src.kp_branch_and_bound import BranchAndBoundAlgorithm
from src.kp_fptas import FPTASAlgorithm
from src.kp_two_approx import TwoApproxAlgorithm


class KnapsackProblem:
    def __init__(self, file_path: str, optimal_file):
        self.file_path = file_path
        self.optimal_file = optimal_file
        self.timeout = 300.0

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
    
    def run_algorithms(self):
        self.branch_and_bound_algorithm = BranchAndBoundAlgorithm(
            self.n, self.W, self.items
        )
        epsilons = [0.8, 0.5, 0.1]
        self.fptas_algorithms = {
            eps: FPTASAlgorithm(self.n, self.W, self.items, epsilon=eps)
            for eps in epsilons
        }
        self.two_approx_algorithm = TwoApproxAlgorithm(
            self.n, self.W, self.items
        )

        threads = []

        def bb_target():
            print("Starting BranchAndBoundAlgorithm...")
            self.branch_and_bound_algorithm.execute()
            print("BranchAndBoundAlgorithm finished.")

        threads.append(threading.Thread(target=bb_target))

        # fptas
        for eps, algo in self.fptas_algorithms.items():
            def fptas_target(algo=algo, eps=eps):
                print(f"Starting FPTASAlgorithm ε={eps}...")
                algo.execute()
                print(f"FPTASAlgorithm ε={eps} finished.")
            threads.append(threading.Thread(target=fptas_target))
        
        def tp_target():
            print("Starting TwoApproxAlgorithm...")
            self.two_approx_algorithm.execute()
            print("TwoApproxAlgorithm finished.")

        threads.append(threading.Thread(target=tp_target))

        # start
        for t in threads:
            t.start()

        # join
        for t in threads:
            t.join(timeout=self.timeout)

        # timeout check
        if threads[0].is_alive():
            print(f"BranchAndBoundAlgorithm timed out after {self.timeout} seconds")
            self.branch_and_bound_algorithm.timeout = True
            threads[0].join()

        for i, eps in enumerate(epsilons, start=1):
            if threads[i].is_alive():
                print(f"FPTASAlgorithm ε={eps} timed out after {self.timeout} seconds")
                self.fptas_algorithms[eps].timeout = True
                threads[i].join()
        
        if threads[0].is_alive():
            print(f"TwoApproxAlgorithm timed out after {self.timeout} seconds")
            self.branch_and_bound_algorithm.timeout = True
            threads[0].join()

    def calculate_relative_error(self):
        with open(self.optimal_file, 'r') as file:
            optimal_value = float(file.readline().strip())

        if self.branch_and_bound_algorithm and not self.branch_and_bound_algorithm.timeout:
            self.branch_and_bound_algorithm.relative_error = (
                (optimal_value - self.branch_and_bound_algorithm.best_value) / optimal_value
            )

        for eps, algo in self.fptas_algorithms.items():
            if algo and not algo.timeout:
                algo.relative_error = (
                    (optimal_value - algo.best_value) / optimal_value
                )
        
        if self.two_approx_algorithm and not self.two_approx_algorithm.timeout:
            self.two_approx_algorithm.relative_error = (
                (optimal_value - self.two_approx_algorithm.best_value) / optimal_value
            )

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
