#include <iostream>
#include <vector>
#include <random>
#include <limits> // Para numeric_limits

// --- SUPOSIÇÕES ---
// 1. A função objetivo `f(X)` é um placeholder. Você deve substituí-la pela sua função real.
// 2. O critério de parada é um número máximo de iterações.
// 3. A dimensão 'n' do vetor de soluções é definida.
// 4. A distribuição normal para 'Z' é com média 0 e desvio padrão 1 (pode ser ajustado).
// ------------------

// Classe para representar um indivíduo (solução)
struct Individual {
    std::vector<double> genes; // O vetor X
    double fitness;            // O valor da função objetivo f(X)

    Individual(int n) : genes(n, 0.0), fitness(0.0) {}
};

// !!! FUNÇÃO OBJETIVO: VOCÊ DEVE IMPLEMENTAR ESTA FUNÇÃO !!!
// Esta é uma função de exemplo (minimização).
// Substitua por sua função objetivo real que recebe um vetor de 'double'
// e retorna um 'double' (o valor da função para aquele vetor).
double objectiveFunction(const std::vector<double>& x) {
    // Exemplo: Função de Sphere (para minimização)
    // f(x) = sum(x_i^2)
    double sum_sq = 0.0;
    for (double val : x) {
        sum_sq += val * val;
    }
    return sum_sq;
}

int main() {
    // --- Parâmetros do Algoritmo ---
    const int n = 5; // Dimensão do vetor de soluções (X e Z)
    const int max_iterations = 1000; // Critério de parada: número máximo de iterações

    // Configuração para geração de números aleatórios com distribuição normal
    std::random_device rd;
    std::mt19937 generator(rd());
    // Média 0.0, Desvio Padrão 1.0. Você pode ajustar o desvio padrão para controlar a "mutação".
    std::normal_distribution<double> distribution(0.0, 1.0);

    // 1. COMEÇO (t = 0)
    int t = 0;

    // 2. Crie uma solução inicial X
    Individual current_solution(n);
    // Inicializa X com valores aleatórios (ex: entre -5 e 5)
    std::uniform_real_distribution<double> uniform_dist(-5.0, 5.0);
    for (int i = 0; i < n; ++i) {
        current_solution.genes[i] = uniform_dist(generator);
    }
    current_solution.fitness = objectiveFunction(current_solution.genes);

    std::cout << "Algoritmo Primordial das Estratégias Evolutivas\n";
    std::cout << "Solução inicial (X): ";
    for (double val : current_solution.genes) {
        std::cout << val << " ";
    }
    std::cout << " -> Fitness: " << current_solution.fitness << "\n";

    // 3. Repita até que um critério de parada seja satisfeito (DO)
    while (t < max_iterations) {
        // 1. Crie com distribuição normal um vetor Z com n valores.
        std::vector<double> Z(n);
        for (int i = 0; i < n; ++i) {
            Z[i] = distribution(generator);
        }

        // 2. Faça Y! = X + Z
        Individual candidate_solution(n);
        for (int i = 0; i < n; ++i) {
            candidate_solution.genes[i] = current_solution.genes[i] + Z[i];
        }

        // Calcule o fitness de Y!
        candidate_solution.fitness = objectiveFunction(candidate_solution.genes);

        // 3. If (f(Y!) <= f(X)) então. (Assumindo minimização, ou seja, menor fitness é melhor)
        if (candidate_solution.fitness <= current_solution.fitness) {
            // 4. X = Y!
            current_solution = candidate_solution;
            // std::cout << "  Iteração " << t << ": Nova solução melhor encontrada. Fitness: " << current_solution.fitness << "\n";
        } else {
            // 5. Else (faz nada, X permanece o mesmo)
            // std::cout << "  Iteração " << t << ": Solução não melhorou. Fitness: " << current_solution.fitness << "\n";
        }
        // 6. Endif

        // 7. t = t + 1
        t++;

        // Opcional: Imprimir progresso a cada N iterações
        if (t % 100 == 0) {
            std::cout << "  Iteração " << t << ": Melhor Fitness até agora: " << current_solution.fitness << "\n";
        }
    } // 8. END DO

    // FIM
    std::cout << "\n--- Algoritmo Finalizado ---\n";
    std::cout << "Melhor Solução Final (X): ";
    for (double val : current_solution.genes) {
        std::cout << val << " ";
    }
    std::cout << " -> Fitness Final: " << current_solution.fitness << "\n";

    return 0;
}