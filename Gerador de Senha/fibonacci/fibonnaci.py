def fibonacci_recursivo(n):
  """
  Calcula o n-ésimo número de Fibonacci usando recursão.

  Args:
    n: Um inteiro não negativo.

  Returns:
    O n-ésimo número de Fibonacci.
  """
  if n <= 1:
    return n
  else:
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2)

if __name__ == "__main__":
  num = int(input("Digite um número inteiro não negativo: "))
  if num < 0:
    print("Número inválido. Digite um número não negativo.")
  else:
    resultado = fibonacci_recursivo(num)
    print(f"O {num}º número de Fibonacci é: {resultado}")