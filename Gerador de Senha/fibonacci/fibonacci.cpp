#include <iostream>
#include <windows.h>

using namespace std;

int fibonacciRecursivo(int n)
{
    if (n <= 1)
    {
        return n;
    }
    else
    {
        return fibonacciRecursivo(n - 1) + fibonacciRecursivo(n - 2);
    }
}

int main()
{
    UINT CPAGE_UTF8 = 65001;
    UINT CPAGE_DEFAULT = GetConsoleOutputCP();
    SetConsoleOutputCP(CPAGE_UTF8);

    int num;
    std::cout << "Digite um número inteiro não negativo: ";
    std::cin >> num;

    if (num < 0)
    {
        std::cout << "Número inválido. Digite um número não negativo." << std::endl;
    }
    else
    {
        std::cout << "O " << num << "º número de Fibonacci é: " << fibonacciRecursivo(num) << std::endl;
    }

    cout << endl
         << endl;
    return 0;
}