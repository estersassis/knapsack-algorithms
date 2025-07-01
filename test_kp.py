import os
import math
from main import read_knapsack_file, bnb_knapsack

instances_dir = "instances_01_KP/low-dimensional"
optimum_dir = "instances_01_KP/low-dimensional-optimum"

# lista de arquivos
instance_files = sorted(os.listdir(instances_dir))

for inst_file in instance_files:
    instance_path = os.path.join(instances_dir, inst_file)
    optimum_path = os.path.join(optimum_dir, inst_file)

    # lê a instância
    n, wmax, items = read_knapsack_file(instance_path)
    items.sort(key=lambda x: x[2], reverse=True)

    # lê o ótimo
    with open(optimum_path) as f:
        expected = float(f.readline().strip())

    # roda o branch-and-bound
    best, sol = bnb_knapsack(items, wmax, n)

    # comparação
    if math.isclose(best, expected, rel_tol=1e-5, abs_tol=1e-5):
        print(f"[OK] {inst_file}: {best}")
    else:
        print(f"[ERRO] {inst_file}: obtido {best}, esperado {expected}")
