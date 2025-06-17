#include <iostream>
#include <iomanip>
#include <cmath>

using namespace std;

int main() {
    int numDigitos;

    cout << "Digite a quantidade de dígitos desejada para as senhas: ";
    cin >> numDigitos;

    if (numDigitos <= 0) {
        cerr << "Erro: A quantidade de dígitos deve ser um número positivo." << endl;
        return 1;
    }

    long long limiteSuperior = static_cast<long long>(pow(10, numDigitos));

    cout << "\nPossíveis senhas de " << numDigitos << " dígitos:" << endl;

    for (long long i = 0; i < limiteSuperior; ++i) {
        cout << setfill('0') << setw(numDigitos) << i << endl;
    }

    cout << "\nTotal de possibilidades geradas: " << limiteSuperior << endl;

    return 0;
}