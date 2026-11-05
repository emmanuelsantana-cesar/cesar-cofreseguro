
from pathlib import Path
from core.db import DB


root = Path(r'data')
db = DB(root_path=root)


# Listar as tabelas
print(db.tables)

# Acessar uma tabela. O conteúdo da tabela é uma matriz.
print(db.senhas)

# Acessar o cabeçalho da tabela
print(db.senhas.columns)

# Acessar uma linha específica da tabela
print(db.senhas[0])

# Acessar um elemento específico da tabela
print(db.senhas[0][0])



# Acessar um elemento específico da tabela
print(db.senhas.columns)
