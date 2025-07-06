import argparse
from src.runner import KnapsackProblemRunner
import asyncio


def parse_args():
    parser = argparse.ArgumentParser(description="Process Knapsack Problem files.")
    parser.add_argument(
        "-p", "--process-folder", type=str, default="kp_instances/large_scale",
        help="Folder containing files to process (default: kp_instances/large_scale)"
    )
    parser.add_argument(
        "-o", "--processed-folder", type=str, default="kp_processed_instances/large_scale",
        help="Folder to store processed files (default: kp_processed_instances/large_scale)"
    )
    parser.add_argument(
        "-r", "--results-folder", type=str, default="kp_results/large_scale",
        help="Folder to store results (default: kp_results/large_scale)"
    )
    parser.add_argument(
        "-opt", "--optimal-folder", type=str, default="kp_instances/large_scale-optimum",
        help="Path to the folder containing optimal values (default: kp_instances/large_scale-optimum)"
    )
    parser.add_argument(
        "--move-back", action="store_true",
        help="Move all files from processed folder back to process folder after processing"
    )
    parser.add_argument(
        "--file", type=str,
        help="Process a single file instead of all"
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    runner = KnapsackProblemRunner(
        folder_to_process=args.process_folder,
        processed_folder=args.processed_folder,
        results_folder=args.results_folder,
        optimal_folder=args.optimal_folder
    )

    asyncio.run(runner.run_for_all_files(specific_file=args.file))

    if args.move_back:
        runner.move_back_processed_files()