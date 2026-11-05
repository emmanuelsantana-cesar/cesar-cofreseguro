
def create(db):
    while True:
        servico = input('Digite o nome do serviço ou SAIR para retornar: ')
        if servico.lower() == 'sair':
            return
        if _is_valid_txt(servico):
            break
        print('Nome inválido, não utilize caracteres especiais: ')

    categories = [(idx, row[0]) for idx, row in enumerate(db.categorias.rows)]
    categories_txt = [f'{idx}-{name}' for idx, name in categories]
    while True:
            p = 'Escolha uma categoria para a senha\n'
            p += '\n'.join(categories_txt)
            p += '\n'
            category = str(input(p))
            if category in [f'{idx}' for idx, _ in categories]:
                break
            print('Categoria inválida')

    while True:
        usr = input('Digite o nome do usuário: ')
        if _is_valid_txt(usr):
            break
        print('Nome inválido, não utilize caracteres especiais')

    week_pwds = [value[0] for value in db.seguranca.rows]
    _pwd_input(week_pwds, int(db.categorias.rows[int(category)][1]))


    while True:
        obs = input('Digite as observações: ')
        if _is_valid_txt(pwd):
            break
        print('Não utilize caracteres especiais')

    row = [servico, usr, pwd, category, obs]
    db.senhas.rows.append(row)
    db.senhas.commit()
        



def read(db):
    servicos = sorted(set([row[0] for row in db.senhas.rows]))
    p = "\nQual servico deseja consultar? \n"
    p += "\n".join([f'{idx}-{servico}' for idx, servico in enumerate(servicos)])
    p += '\n'
    valid_ids = [f'{idx}' for idx in range(len(servicos))]

    while True:
        id_servico = str(input(p))
        if id_servico in valid_ids:
            break
        print("Valor inválido")

    
    pwd_found = [row for row in db.senhas.rows if row[0] == servicos[int(id_servico)]]
    print(f'\nForam encontrada(s) {len(pwd_found)} senha(s) para este serviço')
    for row in pwd_found:
        for col, value in zip(db.senhas.columns, row):
            if col == 'senha':
                value = value[:2] + '*******'
            print(f'{col+':':15} {value:30}')
        print('')

    while True:
        reveal = input('Deseja revelar as senhas? 1-Sim 2-Não\n')
        if reveal in ['1', '2']:
            break
        print("Valor inválido\n")

    if reveal == '1':
         for row in pwd_found:
                for col, value in zip(db.senhas.columns, row):
                    print(f'{col+':':15} {value:30}')
                print('')




def create_category(db):
    try:
        name_col = [row[0] for row in db.categorias.rows]
        while True:
            name = input('Digite o nome da nova categoria ou SAIR para retornar: ')                
            if name.lower() == 'sair':
                return 

            elif not _is_valid_txt(name):
                pass
     
            
            elif name in name_col:
                print('Esta categoria já existe!')
            
            else:
                break

        while True:
            security_lvl = input('Nível de segurança requisitado: 1-Fraco 2-Médio 3-Forte: ')

            if security_lvl in ['1','2','3']:
                break

            print('Valor inválido')

        row = [name, security_lvl]
        db.categorias.rows.append(row)
        db.categorias.commit()
        print('Operação concluída com sucesso!')
    except (ValueError, TypeError) as error:
        print(f"Erro ao executar a operação: {error}")



def update(db):
    p = "\nQual senha deseja modificar ou SAIR para retornar? \n"
    p += "\n".join([f'{idx:5} - Serviço: {row[0][:10]:10}  Usuário: {row[1][:20]:20}  Categoria: {db.categorias.rows[int(row[3])][0][:10]:10}  Observações: {row[4]:20}' for idx, row in enumerate(db.senhas.rows)])
    p += '\n'
    valid_row_ids = [f'{idx}' for idx in range(len(db.senhas.rows))]
    while True:
        row_id = str(input(p))
        if row_id.lower() == 'sair':
            return
        
        if row_id in valid_row_ids:
            break

        print("Valor inválido")

    while True:
        p = '\nQual campo deseja modificar?\n' 
        p += '\n'.join([f'{idx}-{col}' for idx, col in enumerate(db.senhas.columns)])
        p += '\n'
        valid_cols_ids = [f'{idx}' for idx in range(len(db.senhas.columns))]
        while True:
            col_id = str(input(p))            
            if col_id in valid_cols_ids:
                break

            print("Valor inválido")

        if int(col_id) == 2:
            week_pwds = [value[0] for value in db.seguranca.rows]
            pwd_category_id = db.senhas.rows[int(row_id)][3]
            new_value = _pwd_input(week_pwds, int(db.categorias.rows[int(pwd_category_id)][1]))
            

        else:
            while True:
                new_value = str(input("Digite o novo valor: "))
                if _is_valid_txt(new_value):
                    break

        db.senhas.rows[int(row_id)][int(col_id)] = new_value
        db.senhas.commit()
        
        print('Campo atualizado com sucesso!')

        while True:
            flag_repeat = input('Deseja atualizar outro campo? 1-Sim 2-Não ')
            if flag_repeat == '1':
                break

            if flag_repeat == '2':
                return

            print('Valor inválido\n')




def delete(db):
    try:
        p = "\nQual senha deseja excluir ou SAIR para retornar? \n"
        p += "\n".join([f'{idx:5} - Serviço: {row[0]:10}  Usuário: {row[1]:20}  Categoria: {db.categorias.rows[int(row[3])][0]:10}  Observações: {row[4]:20}' for idx, row in enumerate(db.senhas.rows)])
        p += '\n'
        valid_ids = [f'{idx}' for idx in range(len(db.senhas.rows))]
        while True:
            row_id = str(input(p))
            if row_id.lower() == 'sair':
                return
            
            if row_id in valid_ids:
                break

            print("Valor inválido")

        db.categorias.rows.pop(int(row_id))
        db.categorias.commit()
        print('Senha deletada com sucesso!')

    except (ValueError, TypeError) as error:
            print(f"Erro ao executar a operação: {error}")


def _is_valid_txt(txt:str):
    output = True
    unsupported_chars = [',', '\n', '"', "'"]

    if not txt:
        output = False
        print('Entrada em branco\n')
        

    if any([char in txt for char in unsupported_chars]):
        output = False
        print(f'Não utilize os caracteres: [{''.join(unsupported_chars)}]\n')

    return output





def _pwd_input(week_pwds, security_lvl:int):
    while True:
        pwd = input('Digite a senha: ')
        if _is_valid_txt(pwd):
            response = _verify_pwd_strengh(pwd, week_pwds)
            if not response['errors']:
                if  response['security_lvl'] >= security_lvl:
                    break
                p = '\n'
                p += '\n'.join(response['improvements'])
                print(p)
            p = '\n'
            p += '\n'.join(response['errors'])
            print(p)
    return pwd




def _verify_pwd_strengh(pwd:str, week_pwds):
    SPECIAL_CHARS = "!@#$%^&*()"
    errors = []
    improvements = []
    score = 0

    if pwd in week_pwds:
        errors.append("Sua senha é muito comum. Digite outra senha")

    if len(pwd) < 4:
        errors.append("A senha deve conter no mínimo 4 caracteres!")

    elif 6 > len(pwd) >= 4 :
        improvements.append('Senha curta. Aumente a senha para maior segurança')
        score += 1

    elif 8 > len(pwd) >= 6:
        improvements.append('Senha boa mas você pode aumentar para maior segurança')
        score += 2

    else:
        score += 3

    
    if not any([char in pwd for char in SPECIAL_CHARS]):
        improvements.append(f'Adicione ao menos um carater especial para maior segurança: [{SPECIAL_CHARS}]')
    else:
        score += 1


    condition_upper = any([char.isupper()for char in pwd])
    condition_lower = any([char.islower()for char in pwd])
    if (not condition_upper) or (not condition_lower):
        improvements.append(f"A senha deve conter ao menos uma letra maiúscula e uma minúscula para maior segurança")
    else:
        score += 1


    if score <= 2:
        security_lvl = 1
    elif score <= 4:
        security_lvl = 2
    else:
        security_lvl = 3

    response = {
        'errors': errors,
        'improvements': improvements,
        'security_lvl': security_lvl
    }
    return response