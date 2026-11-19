import pandas as pd
from core.log import logger
from core.crud import verify_pwd_strengh


def security_report(db):
    """
    O sistema deve apresentar um resumo da situação do usuário: quantas credenciais existem,
    quantas são fracas, quantas estão repetidas, quantas apareceram na lista de senhas comuns, e
    há quanto tempo cada uma não é alterada.
    """
    
    logger.info(
        "Execução de Relatório de Segurança",
        extra={"service": "Auditoria"}
    )
    
    df_categorias = db.categorias.to_pdf().reset_index(names='categoria').astype(str)
    df_senhas = db.senhas.to_pdf()
    df_senhas = df_senhas.merge(
        df_categorias,
        how='left',
        on=['categoria']
    )
    df_senhas['data'] = pd.to_datetime(df_senhas['data'])
    df_senhas['dias_ultima_atualizacao'] = (pd.Timestamp.today().normalize() - df_senhas['data']).dt.days
    df_senhas['nivel_seguranca'] = df_senhas.senha.apply(lambda x: verify_pwd_strengh(x, db.seguranca.rows)['security_lvl'])



    total_senhas = len(df_senhas)
    total_senhas_fracas = len(df_senhas.loc[df_senhas.nivel_seguranca == 1])
    total_senhas_repetidas = len(df_senhas.loc[df_senhas.senha.duplicated(keep='first')])

    print('\n' + '*'*24)
    print('*RELATÓRIO DE SEGURANÇA*')
    print('*'*24 + '\n')
    print(f'Há um total de {total_senhas} salvas\n')
    print(f'Há um total de {total_senhas_fracas} senha(s) fraca(s)')
    for _, row in df_senhas.loc[df_senhas.nivel_seguranca == 1].iterrows():
        txt = [
            f'{"Categoria:":15} {row['name']:30}',
            f'{"Serviço:":15} {row['servico']:30}',
            f'{"Usuário:":15} {row['usuario']:30}',
            f'{"Senha:":15} {row['senha'][:2] + '*******':30}',
        ]
        print('\n'.join(txt))
        print('\n')

    print(f'Há um total de {total_senhas_repetidas} senha(s) repetida(s)')
    for _, row in df_senhas.loc[df_senhas.senha.duplicated(keep=False)].iterrows():
        txt = [
            f'{"Categoria:":15} {row['name']:30}',
            f'{"Serviço:":15} {row['servico']:30}',
            f'{"Usuário:":15} {row['usuario']:30}',
            f'{"Senha:":15} {row['senha'][:2] + '*******':30}',
        ]
        print('\n'.join(txt))
        print('\n')

    print(f'Tempo desde a última atualização de senhas')
    for idx, row in df_senhas.iterrows():
        txt = [
            f'{"Categoria:":20} {row['name']:30}',
            f'{"Serviço:":20} {row['servico']:30}',
            f'{"Usuário:":20} {row['usuario']:30}',
            f'{"Senha:":20} {row['senha'][:2] + '*******':30}',
            f'{"Última atualização:":20} {row['dias_ultima_atualizacao']:2} dia(s)',
        ]
        print('\n'.join(txt) + '\n')

    print('*'*24)
    print('*'*24 + '\n')

