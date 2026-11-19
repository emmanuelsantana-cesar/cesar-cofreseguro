# Cofre Seguro

Aplicativo de terminal para cadastrar e administrar senhas, organizar credenciais por categoria, consultar um relatório de segurança e fazer perguntas sobre os dados com um agente de IA.

## Requisitos e execução

- Python e as dependências listadas em `requirements.txt`.
- Para usar o agente de IA, é necessária uma chave da API Groq configurada na variável de ambiente `GROQ_API_KEY` (por exemplo, em um arquivo `.env` na raiz do projeto).

Instale as dependências e inicie o programa na pasta do projeto:

```bash
pip install -r requirements.txt
python app.py
```

O programa apresenta um menu numerado. Digite o número da operação e siga as instruções no terminal. Digite `0` para encerrar.

## Funcionalidades

1. **Cadastrar senha**: informe o serviço, escolha uma categoria, informe o usuário, a senha e as observações. A data do cadastro é preenchida pelo programa. A senha precisa ter pelo menos quatro caracteres, não pode estar na lista de senhas comuns carregada pelo projeto e deve atender ao nível de segurança definido para a categoria. O programa sugere melhorias quando necessário. `SAIR` retorna ao menu durante a entrada do serviço.
2. **Consultar senhas**: escolha um serviço da lista. As credenciais correspondentes são exibidas com as senhas mascaradas; em seguida, escolha `1` para revelá-las ou `2` para mantê-las ocultas.
3. **Atualizar uma senha**: selecione um registro e um campo para alterar. A data não é editável por esta opção. Ao alterar a senha, são aplicadas as mesmas verificações de força e do nível da categoria. É possível atualizar mais de um campo na mesma operação.
4. **Deletar uma senha**: selecione o registro pelo índice mostrado. A exclusão remove o registro inteiro, apesar de a mensagem do menu se referir a uma senha. `SAIR` retorna ao menu.
5. **Cadastrar categorias**: informe um nome e um nível requerido: `1` (Fraco), `2` (Médio) ou `3` (Forte). Categorias com nomes já existentes não são aceitas. `SAIR` retorna ao menu.
6. **Relatório de segurança**: mostra o total de credenciais, quantas são classificadas como fracas, as senhas repetidas e o tempo em dias desde a data registrada para cada credencial. Senhas exibidas no relatório ficam mascaradas. O código não apresenta uma contagem separada de senhas comuns.
7. **Agente de IA Groq**: permite perguntar sobre os registros de senhas ou sobre o histórico de logs. Antes de iniciar, confirme com `s`. Digite `sair` para encerrar a conversa. Para consultar logs, comece a pergunta com `log` (por exemplo, `log quais serviços aparecem no histórico?`). Sem `GROQ_API_KEY`, o agente não pode consultar a API.

## Armazenamento e privacidade

Os dados são carregados dos arquivos CSV em `data/` e as operações de cadastro, atualização e exclusão gravam alterações nesses arquivos. Faça cópias de segurança deles se precisar preservar os dados.

Ao usar o agente, o programa avisa que os dados sairão do computador e pede confirmação. Nas perguntas sobre credenciais, envia os campos dos registros exceto o campo `senha`, além da classificação de força calculada. Quando a pergunta começa com `log`, envia o cabeçalho e as linhas do arquivo de logs; esse histórico pode conter os textos das perguntas anteriores. O projeto também registra prompts no log. Portanto, não inclua informações sensíveis na pergunta.

## Informações não especificadas

Os arquivos do projeto não descrevem um procedimento de recuperação de dados, criptografia dos CSVs ou autenticação de usuários. O manual não assume que essas proteções estejam disponíveis.
