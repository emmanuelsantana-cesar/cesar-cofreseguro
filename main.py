
from pathlib import Path
from ext.db import DB


root = Path(r'data')
db = DB(root_path=root)


# Lista as tabelas
print('Lista as tabelas')
print(db.tables)

# Lista as tabelas
print('Lista as tabelas')
print(db.tables)