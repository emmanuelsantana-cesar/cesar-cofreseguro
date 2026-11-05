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
    ENCODING = 'utf-8-sig'
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
        with open(self.file_path, 'r', encoding=self.ENCODING) as f:
            header = f.readline()
            content = f.read()

        self.columns = header.replace('\n', '').split(',')
        self.rows = [row.split(',') for row in content.split('\n') if row]


    def commit(self):
        header = [','.join(self.columns)+'\n']

        rows = [','.join(row) for row in self.rows]
        rows = ['\n'.join(rows)]

        with open(self.file_path, 'w', encoding='utf-8-sig') as f:
            f.writelines(header + rows)




