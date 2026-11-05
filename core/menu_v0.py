dicionario = {}



print(" - Menu: 1 - Cadastrar:2 - Consultar: 3 - Atualizar: 4 - Excluir: 5 - Listar: 0 - Sair ")


while True:

 escolha = int(input("Digite a opção desejada: "))
 if escolha == 1:
  cadastro = input("Escreva o codigo do produto: ")
  nome = input("Escreva o nome do produto: ")
  dicionario [cadastro] = nome

 elif escolha == 2:
  consulta = input("Digite o codigo: ")
  print(dicionario.get(consulta, "codigo invalido!"))

 elif escolha == 3:
  atualizar = input("Digite o codigo: ")
  if atualizar in dicionario:
    novo_nome = input("Digite o novo nome: ")
    dicionario[atualizar] = novo_nome

 elif escolha == 4:
  excluir = input("Digite o codigo pra excluir: ")
  if excluir in dicionario:
    del(dicionario[excluir])

 elif escolha == 5:
  for chave, valor in dicionario.itens():
    print(f"{chave} - {valor}")

 elif escolha == 0:
  break

 else:
  print("Opção invalida!")