from pathlib import Path
from core.db import DB
from core.menu import render_options_view, get_actions

root = Path(r'data')
db = DB(root_path=root)

if __name__ == "__main__":
    while True:
        actions = get_actions()
        valid_actions = [f'{key}' for key in actions.keys()]
        
        while True:
            print('\n')
            options_view = render_options_view()
            option_key = input(options_view)
            if option_key in valid_actions:
                break
            print('Opção inválida')
            

        if option_key == '0':
            print('Encerrando...')
            break

        else:
            aciton_func = actions[int(option_key)]['func']
            aciton_func(db)


