from string import Template
from db.connection import Connection
from symbol.symbol import Symbol

class SymbolType(Connection):

    def __init__(self):
        Connection.__init__(self)
        self.url = ''
        self.type_name = ''
        self.symbols = []
        self.pattern = Template(
            '(?<!\w)('
            '${fullNameLower}|'
            '${fullNameTitle}|'
            '${symbolLower}|'
            '${symbolUpper}|'
            ')(?!\w)'
        )

    def get(self, symbol_type_id):
        fields = [
            'symbol_id',
            'symbol_type_id',
            'symbol',
            'name',
            'full_name',
            'meta',
        ]
        symbols = Connection.get(self, query_params={
            'tablename': 'symbol',
            'fields': fields,
            'where_stmt': [
                {
                    'key': 'symbol_type_id',
                    'value': symbol_type_id
                }
            ]
        })

        for symbol in symbols:
            values = dict(zip(fields, list(symbol)))
            self.symbols.append(Symbol(**values))
