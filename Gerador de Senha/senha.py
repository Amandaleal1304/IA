def gerar_senhas_forca_bruta(num_digitos):
  """
  Gera todas as combinações possíveis de senhas com o número de dígitos especificado pelo usuário.

  Args:
    num_digitos: Um inteiro representando o número de dígitos da senha desejada.

  Returns:
    Uma lista de strings, onde cada string é uma possível senha.
  """
  if not isinstance(num_digitos, int) or num_digitos <= 0:
    return "Por favor, digite um número inteiro positivo para a quantidade de dígitos."

  senhas = []
  limite_superior = 10 ** num_digitos
  formato = f"0{num_digitos}d"  # Cria um formato para zfill com o número correto de dígitos

  for i in range(limite_superior):
    senha = format(i, formato)
    senhas.append(senha)
  return senhas

if __name__ == "__main__":
  try:
    quantidade_digitos = int(input("Digite a quantidade de dígitos desejada para as senhas: "))
    possibilidades = gerar_senhas_forca_bruta(quantidade_digitos)

    if isinstance(possibilidades, str):
      print(possibilidades)
    else:
      print(f"\nPossíveis senhas de {quantidade_digitos} dígitos:")
      for senha in possibilidades:
        print(senha)
      print(f"\nTotal de possibilidades geradas: {len(possibilidades)}")

  except ValueError:
    print("Entrada inválida. Por favor, digite um número inteiro.")