# Knapsack Problem (Problema da Mochila 0/1)

Este trabalho investiga o desempenho de algoritmos para o Problema da Mochila 0/1, no contexto da disciplina Algoritmos II do curso de Ciência da Computação da Universidade Federal de Minas Gerais (UFMG). Foram utilizados algoritmos clássicos e aproximativos para solução do problema, incluindo: Branch and Bound, algoritmo 2-aproximativo, e o FPTAS (Fully Polynomial Time Approximation Scheme) em diferentes valores de precisão.

Observação: Esse projeto já contém instâncias retiradas dos sites http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/ e https://www.kaggle.com/datasets/sc0v1n0/large-scale-01-knapsack-problems. Os resultados do processamento das mesmas também já estão presentes para fins de análise. 

---

## **Instruções de Execução**

### **Execução com Valores Padrão**
Para executar o programa utilizando os valores padrão para as pastas e arquivos:
```bash
$ python3 main.py
```

---

### **Execução Personalizada**
Para controlar o caminho das pastas e arquivos, você pode usar as seguintes tags:
```bash
$ python3 main.py -p kp_instances -o processed_folder -r results_folder -opt kp_instances/optimum
```

**Explicação das Tags:**
- `-p` ou `--path`: Define o caminho da pasta que contém as instâncias TSP.
- `-o` ou `--output`: Define a pasta onde os arquivos processados serão armazenados.
- `-r` ou `--results`: Define a pasta onde os resultados serão salvos.
- `-opt` ou `--optimal`: Define a pasta onde estão os valores ótimos
- `--file`: Define um arquivo específico a ser processado, caso não seja usado, todos os arquivos da pasta definida no `--path` serão processadas.
---

### **Tag para Retornar os Arquivos à Pasta de Origem**
Se desejar garantir que os arquivos voltem para a pasta de origem após o processamento, utilize a seguinte tag:
```bash
$ python3 main.py --move-back
```

---

### **Ajuda e Informações Adicionais**
Para mais informações sobre as tags e opções disponíveis, utilize:
```bash
$ python3 main.py -h
```

---

## **Requisitos**
- Python 3.x instalado no sistema.

## **Autores**

- Ester Sara Assis Silva - estersarasilva@gmail.com
- Julia Paes de Viterbo -juliapaesv@gmail.com
