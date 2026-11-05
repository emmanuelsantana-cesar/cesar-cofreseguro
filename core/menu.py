from core.crud import create, read, update, delete, create_category
import sys

def get_actions():
    return {
        1: {
            'name': '1 - Cadastrar Senha',
            'func': create
        },
        2: {
            'name': '2 - Consultar Senhas',
            'func': read
        },
        3: {
            'name': '3 - Atualizar uma senha',
            'func': update
        },
        4: {
            'name': '4 - Deletar uma senha',
            'func': delete
        },
        5: {
            'name': '5 - Cadastrar categorias',
            'func': create_category
        },
        0: {
            'name': '0 - Sair',
            'func': None
        }
    }


def render_options_view():
    actions = get_actions()
    action_names = [action['name'] for action in actions.values()]

    output = 'Escolha uma opçao:'
    output += '\n'
    output += '\n'.join(action_names) 
    output += '\n'
    return output

