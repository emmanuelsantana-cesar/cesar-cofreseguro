from pathlib import Path


class DB:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self._load_tables()

    def __repr__(self):
        return str(self.tables)

    def _load_tables(self):
        self.tables = []
        for file_path in self.root_path.iterdir():
            setattr(self, file_path.stem, Table(file_path))
            self.tables.append(file_path.stem)



class Table:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.repr_with = 30
        self._load_table()

    def __repr__(self):
        output = ''
        for col in self.columns:
            output += f'{col:{self.repr_with}}'

        output += '\n'
        for row in self.rows:
            for value in row:
                output += f'{value[:self.repr_with-3]:{self.repr_with}}'
            output += '\n'

        return output

    def __getitem__(self, key):
        return self.rows[key]



    def _load_table(self):
        with open(self.file_path, 'r', encoding='utf-8-sig') as f:
            header = f.readline()
            content = f.read()

        self.columns = header.split(',')
        self.rows = [row.split(',') for row in  content.split('\n')]




