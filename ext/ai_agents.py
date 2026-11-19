import os
from dotenv import load_dotenv
from groq import Groq
from core.log import logger
from core.crud import verify_pwd_strengh

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "openai/gpt-oss-120b"
LIMITE_CARACTERES = 20000

def talk_to_agent(db):
    while True:
        confirmacao = input('Seus dados vão sair do computador. Continuar? (s/n) ')
        if confirmacao == 'n':
            return
        
        if confirmacao == 's':
            logger.info(
                "Iniciado serviço de Agente de IA",
                extra={"service": "Agente de IA"}
            )
            if not GROQ_API_KEY:
                print("\nA chave da API não está configurada.")
                print("Veja as instruções no início do arquivo agente.py.")
            else:
                print(f"Digite 'sair' para encerrar.")
                while True:
                    print(f'Digite "log" no começo da pergunta para acessar o histórico de utilização')
                    pergunta = input("\nPergunta > ").strip()
                    logger.info(
                        pergunta,
                        extra={"service": "Prompt de IA"}
                    )
                    if pergunta.lower() == "sair":
                        logger.info(
                            "Saindo do serviço de Agente de IA...",
                            extra={"service": "Agente de IA"}
                        )
                        break

                    if 'log' in pergunta.lower()[:5]:
                        is_log=True
                    else:
                        is_log=False
                    conteudo = _content_to_agent(db, is_log)
                    resposta = falar_com_agente_texto(conteudo, pergunta, "CofreSeguro")
                    print(resposta)
                return
        else:
            print('Valor inválido')


def _content_to_agent(db, is_log=False):
    if is_log:
        header = [col for col in db.log.columns]
        rows = [','.join(row) for row in db.log.rows]

    else:
        header = [col for col in db.senhas.columns if 'senha' not in col] + ['forca_senha']
        row_contents = [
            [value for value, col in zip(row, db.senhas.columns) if 'senha' not in col]
            for row in db.senhas.rows
        ]

        pwd_lvls = [
            [verify_pwd_strengh(row[2], db.seguranca.rows)['security_lvl_name']]
            for row in db.senhas.rows
        ]


        rows = [
            ','.join(row + pwd_classification)
            for row, pwd_classification in zip(row_contents, pwd_lvls)
        ]
    content = ','.join(header) + '\n'
    content += '\n'.join(rows)
    return content




def falar_com_agente_texto(conteudo, pergunta, nome_sistema="CofreSeguro", streaming=False):
    if not pergunta or not pergunta.strip():
        print("\n[Agente] Nenhuma pergunta foi digitada.")
        return None

    if not conteudo or not conteudo.strip():
        print("\n[Agente] Não há dados para enviar. Cadastre alguns registros antes.")
        return None

    if len(conteudo) > LIMITE_CARACTERES:
        print(f"\n[Agente] Os dados têm {len(conteudo)} caracteres, acima do limite de "
              f"{LIMITE_CARACTERES}.")
        print("         Envie apenas os registros necessários para a pergunta.")
        return None

    cliente = _criar_cliente()
    if cliente is None:
        return None

    prompt = _montar_prompt(conteudo, pergunta.strip(), nome_sistema)

    try:
        print("\nConsultando o agente...")
        completion = cliente.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_completion_tokens=1024,
            top_p=0.9,
            stream=streaming,
        )

        print("\n" + "=" * 70)
        print("AGENTE:")
        print("=" * 70)

        if streaming:
            resposta = ""
            for pedaco in completion:
                texto = pedaco.choices[0].delta.content or ""
                print(texto, end="", flush=True)
                resposta += texto
            print()
        else:
            resposta = completion.choices[0].message.content
            print(resposta)

        print("=" * 70)
        return resposta

    except Exception as erro:
        _explicar_erro(erro)
        return None




def _montar_prompt(conteudo, pergunta, nome_sistema):
    """Junta as instruções, os dados e a pergunta num único texto."""
    return f"""Você é um assistente inteligente do sistema {nome_sistema}.

Seu papel é analisar os dados fornecidos e responder perguntas do usuário de forma clara, objetiva e útil.

DADOS DO SISTEMA:
---
{conteudo}
---

PERGUNTA DO USUÁRIO: {pergunta}

INSTRUÇÕES PARA SUA RESPOSTA:
1. Responda SEMPRE em português do Brasil
2. Baseie sua resposta APENAS nos dados fornecidos acima
3. Se os dados não contêm informação suficiente, diga isso claramente
4. Seja objetivo e direto, sem repetir a pergunta nem fazer preâmbulos longos
5. Use formatação clara (listas, números) quando apropriado
6. Se identificar padrões interessantes nos dados, mencione-os

Responda agora:"""



def _criar_cliente():
    """Cria o cliente da Groq. Devolve o cliente ou None se houver problema."""
    if Groq is None:
        print("\n[Agente] A biblioteca groq não está instalada.")
        print("         Instale com: pip install groq")
        return None

    if not GROQ_API_KEY:
        print("\n[Agente] A chave da API não foi configurada.")
        print("         Crie o arquivo .env (copie o .env.example) e cole sua chave nele.")
        print("         Veja as instruções no início do arquivo agente.py.")
        return None

    try:
        return Groq(api_key=GROQ_API_KEY)
    except Exception as erro:
        print(f"\n[Agente] Erro ao inicializar o cliente: {erro}")
        return None



def _explicar_erro(erro):
    """Mostra uma mensagem compreensível para os erros mais comuns da API."""
    texto = str(erro).lower()

    if "api_key" in texto or "authentication" in texto or "401" in texto:
        print("\n[Agente] Erro de autenticação: a chave é inválida ou expirou.")
        print("         Gere uma nova chave em https://console.groq.com/keys")
    elif "rate_limit" in texto or "429" in texto:
        print("\n[Agente] Limite de requisições excedido. Aguarde alguns minutos.")
    elif "quota" in texto or "exceeded" in texto:
        print("\n[Agente] Limite de uso da conta gratuita atingido.")
    elif "connection" in texto or "timeout" in texto:
        print("\n[Agente] Sem conexão com o serviço. Verifique a internet.")
    else:
        print(f"\n[Agente] Erro ao consultar a API: {erro}")