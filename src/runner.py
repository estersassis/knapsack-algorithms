import os
import shutil
from src.kp import KnapsackProblem


class KnapsackProblemRunner:
    def __init__(self, folder_to_process="kp", processed_folder="processed", results_folder="results", optimal_folder="optimal"):
        self.folder_to_process = folder_to_process
        self.processed_folder = processed_folder
        self.results_folder = results_folder
        self.optimal_folder = optimal_folder

        os.makedirs(self.folder_to_process, exist_ok=True)
        os.makedirs(self.processed_folder, exist_ok=True)
        os.makedirs(self.results_folder, exist_ok=True)
    
    def process_file(self, file_name):
        file_path = os.path.join(self.folder_to_process, file_name)
        print(f"Processing {file_path}...")

        optimal_file_path = os.path.join(self.optimal_folder, file_name)

        try:
            problem = KnapsackProblem(file_path, optimal_file_path)
            problem.run_algorithms()
            problem.generate_result_file(file_name, self.results_folder)
            shutil.move(file_path, os.path.join(self.processed_folder, file_name))
            print(f"Finished processing {file_name}.")
        except Exception as e:
            shutil.move(file_path, os.path.join(self.processed_folder, file_name))
            print(f"Error processing {file_name}: {e}. Skipping to next file.")

    def run_for_all_files(self):
        files = sorted(
            os.listdir(self.folder_to_process),
            key=lambda x: int(os.path.splitext(x)[0].split("_")[-1])
        )

        for file_name in files:
            self.process_file(file_name)
        
    def move_back_processed_files(self):
        files = os.listdir(self.processed_folder)
        for file_name in files:
            src_path = os.path.join(self.processed_folder, file_name)
            dest_path = os.path.join(self.folder_to_process, file_name)
            shutil.move(src_path, dest_path)