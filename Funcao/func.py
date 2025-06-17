import random
import math
import sympy # Importar a biblioteca SymPy

# --- Global Precedence for __repr__ ---
PRECEDENCE = {
    '+': 10,
    '-': 10,
    '*': 20,
    '/': 20,
}

# --- 1. Definição da Estrutura da Árvore (Indivíduo) ---
class Node:
    """
    Representa um nó na árvore de expressão.
    Pode ser um operador (+, -, *, /) ou um terminal (x, constantes).
    """
    def __init__(self, value, children=None):
        self.value = value  # O valor do nó (operador ou terminal)
        self.children = children if children is not None else [] # Lista de nós filhos (operandos)

    def __repr__(self):
        """
        Representação mais legível (infix) da árvore, considerando a precedência de operadores.
        ATENÇÃO: Este método NÃO realiza simplificação algébrica (como expandir (x-2)*(x-3) para x^2-5x+6).
        Ele apenas tenta reduzir parênteses redundantes com base nas regras de precedência.
        """
        if not self.children: # Se não tem filhos, é um terminal
            return str(self.value)
        
        current_op_precedence = PRECEDENCE.get(self.value, 0) 

        if len(self.children) == 2: # Operadores binários
            left_child_node = self.children[0]
            right_child_node = self.children[1]

            left_child_str = left_child_node.__repr__()
            right_child_str = right_child_node.__repr__()

            left_child_op_precedence = PRECEDENCE.get(left_child_node.value, 100) 
            right_child_op_precedence = PRECEDENCE.get(right_child_node.value, 100)

            if left_child_op_precedence < current_op_precedence:
                left_child_str = f"({left_child_str})"

            if right_child_op_precedence < current_op_precedence or \
               (right_child_op_precedence == current_op_precedence and \
                (self.value == '-' or self.value == '/')): 
                right_child_str = f"({right_child_str})"
            
            elif self.value == '/' and right_child_node.value in ['*', '/']:
                 right_child_str = f"({right_child_str})"

            return f"{left_child_str} {self.value} {right_child_str}"
        
        elif len(self.children) == 1: 
            return f"{self.value}({self.children[0].__repr__()})"
        
        return f"({self.value} {' '.join(map(str, self.children))})"


    def evaluate(self, x_val): # Renomeado para x_val para evitar conflito com sympy.Symbol('x')
        """
        Avalia a expressão da árvore para um dado valor de 'x'.
        """
        if self.value == 'x':
            return float(x_val) 
        elif isinstance(self.value, (int, float)):
            return float(self.value) 
        else: # É um operador
            child_results = [child.evaluate(x_val) for child in self.children]
            
            if self.value == '+':
                return child_results[0] + child_results[1]
            elif self.value == '-':
                return child_results[0] - child_results[1]
            elif self.value == '*':
                return child_results[0] * child_results[1]
            elif self.value == '/':
                if abs(child_results[1]) < 1e-6: 
                    return 1.0 
                return child_results[0] / child_results[1]
            else:
                raise ValueError(f"Operador desconhecido: {self.value}")

    def get_all_nodes(self, nodes_list=None):
        """
        Retorna uma lista de todos os nós na árvore (percorrido em pré-ordem).
        Útil para seleção de pontos de cruzamento/mutação.
        """
        if nodes_list is None:
            nodes_list = []
        nodes_list.append(self)
        for child in self.children:
            child.get_all_nodes(nodes_list)
        return nodes_list
    
    def copy(self):
        """Cria uma cópia profunda (recursiva) da árvore."""
        if not self.children:
            return Node(self.value)
        return Node(self.value, [child.copy() for child in self.children])

# --- 2. Conjuntos de Funções (Operadores) e Terminais (Variáveis/Constantes) ---
OPERATORS = ['+', '-', '*', '/']
TERMINALS = ['x'] + list(range(-10, 11)) 

ARITY = {
    '+': 2,
    '-': 2,
    '*': 2,
    '/': 2,
}

# --- 3. Geração de Árvores Aleatórias (População Inicial) ---
def generate_random_tree(max_depth, method='full', current_depth=0):
    """
    Gera uma árvore de expressão aleatória para um indivíduo da população.
    """
    is_terminal_node = (current_depth >= max_depth -1) or \
                       (method == 'grow' and random.random() < 0.6 and current_depth > 0) 

    if is_terminal_node:
        return Node(random.choice(TERMINALS))
    else:
        op = random.choice(OPERATORS)
        children = []
        for _ in range(ARITY[op]):
            children.append(generate_random_tree(max_depth, method, current_depth + 1))
        return Node(op, children)

# --- 4. Função de Aptidão (Fitness Function) ---
def calculate_fitness(individual, data_points):
    """
    Calcula a aptidão (fitness) de um indivíduo (árvore).
    """
    total_error = 0.0
    for x_val, y_expected in data_points:
        try:
            y_calculated = individual.evaluate(x_val)
            if math.isinf(y_calculated) or math.isnan(y_calculated):
                 return float('inf') 
            total_error += abs(y_calculated - y_expected) 
        except Exception as e:
            return float('inf') 
    return total_error

# --- 5. Operadores Genéticos ---
def select_parent(population, fitnesses, tournament_size=5):
    """
    Seleção por Torneio: Escolhe 'tournament_size' indivíduos aleatoriamente
    da população e retorna o que possui a menor aptidão (melhor erro).
    """
    contenders_indices = random.sample(range(len(population)), tournament_size)
    best_contender_index = contenders_indices[0] 

    for i in contenders_indices:
        if fitnesses[i] < fitnesses[best_contender_index]:
            best_contender_index = i
            
    return population[best_contender_index]

def crossover(parent1, parent2):
    """
    Cruzamento (Crossover): Troca subárvores entre dois pais.
    Cria dois novos indivíduos (filhos).
    """
    child1 = parent1.copy()
    child2 = parent2.copy()

    nodes1 = child1.get_all_nodes()
    nodes2 = child2.get_all_nodes()

    crossover_point1 = random.choice(nodes1[1:] if len(nodes1) > 1 else nodes1)
    crossover_point2 = random.choice(nodes2[1:] if len(nodes2) > 1 else nodes2)

    def replace_node_in_tree(root, old_node, new_node):
        if root is old_node: 
            return new_node
        for i, child in enumerate(root.children):
            if child is old_node:
                root.children[i] = new_node
                return root
            res = replace_node_in_tree(child, old_node, new_node)
            if res is not child: 
                root.children[i] = res
                return root
        return root

    child1 = replace_node_in_tree(child1, crossover_point1, crossover_point2.copy())
    child2 = replace_node_in_tree(child2, crossover_point2, crossover_point1.copy())
        
    return child1, child2

def mutate(individual, max_depth_new_subtree=3):
    """
    Mutação: Substitui uma subárvore aleatória por uma nova subárvore gerada aleatoriamente.
    """
    mutated_individual = individual.copy()
    all_nodes = mutated_individual.get_all_nodes()
    
    mutation_point = random.choice(all_nodes)
    
    new_subtree = generate_random_tree(max_depth=max_depth_new_subtree, method='grow')
    
    if mutated_individual is mutation_point:
        mutated_individual = new_subtree
    else:
        for node in all_nodes:
            if mutation_point in node.children:
                idx = node.children.index(mutation_point)
                node.children[idx] = new_subtree
                break
        
    return mutated_individual

# --- SymPy Integration: Função para converter a árvore Node em expressão SymPy ---
x_sym = sympy.Symbol('x') # Definir o símbolo 'x' para SymPy

def tree_to_sympy_expr(node):
    """
    Converte um objeto Node (árvore de expressão) em uma expressão SymPy.
    """
    if node.value == 'x':
        return x_sym
    elif isinstance(node.value, (int, float)):
        return sympy.Float(node.value) # Use sympy.Float para constantes
    else: # É um operador
        child_exprs = [tree_to_sympy_expr(child) for child in node.children]
        
        if node.value == '+':
            return child_exprs[0] + child_exprs[1]
        elif node.value == '-':
            return child_exprs[0] - child_exprs[1]
        elif node.value == '*':
            return child_exprs[0] * child_exprs[1]
        elif node.value == '/':
            # SymPy lida com divisão por zero simbolicamente, mas podemos dar uma proteção
            if child_exprs[1] == 0:
                return sympy.Float('inf') # Retorna infinito simbólico para evitar divisão por zero literal
            return child_exprs[0] / child_exprs[1]
        else:
            raise ValueError(f"Operador SymPy desconhecido: {node.value}")


# --- 6. Algoritmo Principal de Programação Genética ---
def genetic_programming(data_points, 
                       population_size=100, 
                       max_generations=50, 
                       max_tree_depth=5,
                       tournament_size=5,
                       crossover_rate=0.8,
                       mutation_rate=0.1,
                       elitism_count=1):
    """
    Executa o algoritmo de Programação Genética para encontrar a função
    que melhor se ajusta aos 'data_points' (pares de entrada/saída).
    """
    print("Iniciando Programação Genética para Engenharia Reversa de Funções...")

    population = []
    for _ in range(population_size // 2):
        population.append(generate_random_tree(max_tree_depth, method='full'))
    for _ in range(population_size - (population_size // 2)):
        population.append(generate_random_tree(max_tree_depth, method='grow'))
    
    best_individual_overall = None 
    best_fitness_overall = float('inf') 

    for generation in range(max_generations):
        fitnesses = [calculate_fitness(ind, data_points) for ind in population]

        current_best_index = fitnesses.index(min(fitnesses))
        current_best_individual = population[current_best_index]
        current_best_fitness = fitnesses[current_best_index]

        print(f"Geração {generation + 1}: Melhor Aptidão = {current_best_fitness:.4f}")

        if current_best_fitness < best_fitness_overall:
            best_fitness_overall = current_best_fitness
            best_individual_overall = current_best_individual.copy() 
            
            if best_fitness_overall < 1e-6: 
                print("\nFunção perfeita (ou muito próxima) encontrada! Encerrando...")
                break

        new_population = []

        sorted_population_with_fitness = sorted(zip(population, fitnesses), key=lambda x: x[1])
        for i in range(elitism_count):
            new_population.append(sorted_population_with_fitness[i][0].copy())

        while len(new_population) < population_size:
            parent1 = select_parent(population, fitnesses, tournament_size)
            parent2 = select_parent(population, fitnesses, tournament_size)

            child1, child2 = parent1.copy(), parent2.copy() 

            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            
            if random.random() < mutation_rate:
                child1 = mutate(child1, max_depth_new_subtree=3)
            new_population.append(child1) 
            
            if len(new_population) < population_size and child2:
                if random.random() < mutation_rate:
                    child2 = mutate(child2, max_depth_new_subtree=3)
                new_population.append(child2)
        
        population = new_population 

    print("\n--- Processo de Programação Genética Finalizado ---")
    print(f"Melhor função encontrada (Erro: {best_fitness_overall:.4f}):")
    if best_individual_overall:
        print(f"  Representação da Árvore (Gerada por GP): {best_individual_overall}")

        # --- NOVA SEÇÃO: Simplificação com SymPy ---
        try:
            sympy_expr = tree_to_sympy_expr(best_individual_overall)
            simplified_expr = sympy.expand(sympy_expr) # Expande para forma polinomial
            print(f"  Função Simplificada (por SymPy): f(x) = {simplified_expr}")
            # Se quiser uma forma mais "bonita" ou LaTeX:
            # print(f"  Função Simplificada (LaTeX): $f(x) = {sympy.latex(simplified_expr)}$")
        except Exception as e:
            print(f"  Erro ao simplificar a função com SymPy: {e}")
            print("  Verifique se o SymPy está instalado (pip install sympy) e se a expressão é válida.")
        # --- FIM DA NOVA SEÇÃO ---

    else:
        print("  Nenhuma função válida foi encontrada.")

    print("\nTestando a melhor função encontrada com os dados de entrada:")
    if best_individual_overall:
        for x_val, y_expected in data_points:
            try:
                y_calculated = best_individual_overall.evaluate(x_val)
                print(f"  Entrada: {x_val} | Esperado: {y_expected} | Calculado: {y_calculated:.4f} | Erro: {abs(y_calculated - y_expected):.4f}")
            except Exception:
                print(f"  Entrada: {x_val} | Erro ao calcular para a função encontrada.")
    else:
        print("  Não é possível testar sem uma função encontrada.")

    return best_individual_overall, best_fitness_overall

# --- Dados do Problema (Pares de Entrada/Saída) ---
# A função alvo que queremos "reverter" é: f(x) = (x - 2) * (x - 3) = x^2 - 5x + 6
target_data = [
    (0, 6),
    (1, 2),
    (2, 0),
    (3, 0),
    (4, 2),
    (5, 6),
    (6, 12),
    (7, 20),
    (8, 30),
    (9, 42),
    (10, 56)
]

# --- Execução da Programação Genética ---
if __name__ == "__main__":
    best_function_found, final_error = genetic_programming(
        data_points=target_data,
        population_size=1000,      
        max_generations=250,      
        max_tree_depth=3,         
        tournament_size=7,        
        crossover_rate=0.85,      
        mutation_rate=0.15,       
        elitism_count=3           
    )