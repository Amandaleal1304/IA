#include <iostream>
#include <vector>
#include <random>
#include <numeric>
#include <limits>
#include <algorithm>
#include <windows.h>//acentuação
#define CYAN    "\033[36m"
#define RESET   "\033[0m"

using namespace std;

// Definição das moedas disponíveis (em centavos para evitar ponto flutuante)
const vector<int> COIN_DENOMINATIONS = { 20, 11, 5, 1}; // 1 real, 50 centavos, 25c, 10c, 5c, 1c

// Representa uma solução possível com um conjunto de moedas
struct Solution {
    vector<int> counts; // Quantidade de cada moeda
    int num_coins;      // Total de moedas usadas
    int total_value;    // Valor total representado por esta solução

    Solution(size_t n = 0) : counts(n), num_coins(0), total_value(0) {}

    // Atualiza as métricas de valor total e número total de moedas
    void update_metrics(int target) {
        total_value = 0;
        for (size_t i = 0; i < counts.size(); ++i) {
            total_value += counts[i] * COIN_DENOMINATIONS[i];
        }

        num_coins = accumulate(counts.begin(), counts.end(), 0);

        if (total_value != target) {
            // Penaliza soluções inválidas
            num_coins = numeric_limits<int>::max();
        }
    }
};

// Algoritmo guloso para encontrar uma solução rápida
Solution greedy_change(int amount) {
    Solution solution(COIN_DENOMINATIONS.size());

    for (size_t i = 0; i < COIN_DENOMINATIONS.size(); ++i) {
        solution.counts[i] = amount / COIN_DENOMINATIONS[i];
        amount %= COIN_DENOMINATIONS[i];
    }

    solution.update_metrics(amount);
    return solution;
}

// Geração aleatória de soluções para o algoritmo genético
Solution random_solution(int amount, mt19937 &rng) {
    uniform_int_distribution<int> dist(0, 10);
    Solution solution(COIN_DENOMINATIONS.size());

    int remaining = amount;

    for (size_t i = 0; i < COIN_DENOMINATIONS.size(); ++i) {
        if (remaining <= 0) break;

        int max_count = remaining / COIN_DENOMINATIONS[i];
        int count = min(dist(rng), max_count);
        solution.counts[i] = count;
        remaining -= count * COIN_DENOMINATIONS[i];
    }

    solution.update_metrics(amount);
    return solution;
}

// Mutação de uma solução
void mutate(Solution &sol, int amount, mt19937 &rng) {
    uniform_int_distribution<int> index_dist(0, COIN_DENOMINATIONS.size() - 1);
    int idx = index_dist(rng);

    if (sol.counts[idx] > 0) sol.counts[idx]--;
    else sol.counts[idx]++;

    sol.update_metrics(amount);
}

// Algoritmo genético para minimizar o número de moedas
Solution genetic_algorithm(int amount, int population_size = 100, int generations = 2000) {
    mt19937 rng(random_device{}());

    vector<Solution> population;
    for (int i = 0; i < population_size; ++i) {
        population.push_back(random_solution(amount, rng));
    }

    Solution best = greedy_change(amount);

    for (int gen = 0; gen < generations; ++gen) {
        sort(population.begin(), population.end(), [](const Solution &a, const Solution &b) {
            return a.num_coins < b.num_coins;
        });

        if (population[0].num_coins < best.num_coins) {
            best = population[0];
        }

        // Seleciona os melhores e gera mutações
        for (int i = population_size / 2; i < population_size; ++i) {
            population[i] = population[i - population_size / 2];
            mutate(population[i], amount, rng);
        }
    }

    return best;
}

// Função principal
int main() {
    UINT CPAGE_UTF8 = 65001;
    UINT CPAGE_DEFAULT = GetConsoleOutputCP();
     SetConsoleOutputCP(CPAGE_UTF8);
 

    double troco_input;
    cout << "Digite o valor do troco (ex: 0.15 para 15 centavos): ";
    cin >> troco_input;

    // Trabalhar em centavos para evitar problemas com ponto flutuante
    int troco = static_cast<int>(round(troco_input * 100));

    cout << "\n--- Solução com Algoritmo Guloso ---\n";
    Solution guloso = greedy_change(troco);
    // cout << "Total de moedas usadas: " << guloso.num_coins << endl;
    for (size_t i = 0; i < guloso.counts.size(); ++i) {
        if (guloso.counts[i] > 0)
            cout << CYAN << guloso.counts[i]  << RESET << " moeda(s) de " << CYAN << COIN_DENOMINATIONS[i] << RESET<< " centavos\n";
    }

    cout << "\n--- Solução com Algoritmo Genético ---\n";
    Solution genetico = genetic_algorithm(troco);
    // cout << "Total de moedas usadas: " << genetico.num_coins << endl;
    for (size_t i = 0; i < genetico.counts.size(); ++i) {
        if (genetico.counts[i] > 0)
            cout << CYAN << genetico.counts[i] << RESET << " moeda(s) de " << CYAN << COIN_DENOMINATIONS[i] << RESET << " centavos\n";
    }

    return 0;
}

