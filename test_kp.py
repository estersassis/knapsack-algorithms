import os
import math
from src.kp_two_approx import TwoApproxAlgorithm
from src.kp_branch_and_bound import BranchAndBoundAlgorithm
from src.kp import KnapsackProblem

instances_dir = "kp_instances/low-dimensional"
optimum_dir = "kp_instances/low-dimensional-optimum"

# lista de arquivos
instance_files = sorted(os.listdir(instances_dir))

for inst_file in instance_files:
    instance_path = os.path.join(instances_dir, inst_file)
    optimum_path = os.path.join(optimum_dir, inst_file)

    # lê a instância
    problem = KnapsackProblem(instance_path, optimum_path)

    # lê o ótimo
    with open(optimum_path) as f:
        expected = float(f.readline().strip())

    # roda o branch-and-bound
    alg = BranchAndBoundAlgorithm(
        problem.n, problem.W, problem.items
    )
    alg.execute()

    # comparação
    if math.isclose(alg.best_value, expected, rel_tol=1e-5, abs_tol=1e-5):
        print(f"[OK] {inst_file}: {alg.best_value}")
    else:
        print(f"[ERRO] {inst_file}: obtido {alg.best_value}, esperado {expected}")
