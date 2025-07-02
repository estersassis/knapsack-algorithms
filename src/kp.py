import math
import time
from src.kp_branch_and_bound import BranchAndBoundAlgorithm

class KnapsackProblem:
    def __init__(self, file_path: str, optimal_file):
        self.file_path = file_path
        self.optimal_file = optimal_file
        self.instance = None
        self.timeout = 300.0

        self.n = None
        self.W = None
        self.items = None

        self.branch_and_bound_algorithm = None

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
        import threading

        self.branch_and_bound_algorithm = BranchAndBoundAlgorithm(
            self.n, self.W, self.items
        )

        def target():
            print("Starting BranchAndBoundAlgorithm...")
            self.branch_and_bound_algorithm.execute()
            print("BranchAndBoundAlgorithm finished.")

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=self.timeout)

        if thread.is_alive():
            print(f"BranchAndBoundAlgorithm timed out after {self.timeout} seconds")
            self.branch_and_bound_algorithm.timeout = True
            thread.join()  # força finalizar a thread

    def calculate_relative_error(self):
        try:
            with open(self.optimal_file, 'r') as file:
                optimal_value = float(file.readline().strip())
        except FileNotFoundError:
            if self.branch_and_bound_algorithm.timeout == False:
                self.branch_and_bound_algorithm.relative_error = -1
            return

        if optimal_value <= 0:
            if self.branch_and_bound_algorithm.timeout == False:
                self.branch_and_bound_algorithm.relative_error = -1
            return

        if self.branch_and_bound_algorithm.timeout == False:
            self.branch_and_bound_algorithm.relative_error = (
                (optimal_value - self.branch_and_bound_algorithm.best_value) / optimal_value
        )

    
    def generate_result_file(self, file_name, results_folder):
        self.calculate_relative_error()

        with open(f"{results_folder}/{file_name}.result", 'w') as file:
            file.write(f"Instance: {self.instance}\n")
            
            for algorithm_name, algorithm_obj in {
                "Branch and Bound Algorithm": self.branch_and_bound_algorithm
            }.items():
                if algorithm_obj is not None:
                    file.write(f"\n--- {algorithm_name} ---\n")
                    if algorithm_obj.timeout:
                        file.write(f"Best Value: NA\n")
                        file.write(f"Execution Time: NA\n")
                        file.write(f"Memory Usage: NA\n")
                        file.write(f"Relative Error: NA\n")
                    else:
                        file.write(f"Best Value: {algorithm_obj.best_value}\n")
                        file.write(f"Execution Time: {algorithm_obj.execution_time:.4f} seconds\n")
                        file.write(f"Memory Usage: {algorithm_obj.memory_usage} bytes\n")
                        file.write(f"Relative Error: {algorithm_obj.relative_error:.4f}\n")