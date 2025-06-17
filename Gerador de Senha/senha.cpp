#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include <cmath>

using namespace std;

vector<string> gerarSenhasForcaBruta(int numDigitos) {
    vector<string> senhas;

    if (numDigitos <= 0) {
        cerr << "Erro: A quantidade de dígitos deve ser um número positivo." << endl;
        return senhas;
    }

    long long limiteSuperior = static_cast<long long>(pow(10, numDigitos));

    for (long long i = 0; i < limiteSuperior; ++i) {
        string senha = to_string(i);
        while (senha.length() < numDigitos) {
            senha = "0" + senha;
        }
        senhas.push_back(senha);
    }

    return senhas;
}

int main() {
    int quantidadeDigitos;

    cout << "Digite a quantidade de digitos desejada para as senhas: ";
    cin >> quantidadeDigitos;

    vector<string> possibilidades = gerarSenhasForcaBruta(quantidadeDigitos);

    if (!possibilidades.empty()) {
        cout << "\nPossiveis senhas de " << quantidadeDigitos << " digitos:" << endl;
        for (const string& senha : possibilidades) {
            cout << senha << endl;
        }
        cout << "\nTotal de possibilidades geradas: " << possibilidades.size() << endl;
    }

    return 0;
}