import urllib, json, re, os
from symbol_type import SymbolType
from mock_data.coin_data import coin_data
from db.connection import Connection


class CryptocurrencySymbolType(SymbolType, Connection):
    # we manually enter symbol types,
    # so this value is hard-coded
    symbol_type_id = 1

    def __init__(self):
        SymbolType.__init__(self)
        Connection.__init__(self)
        self.get(self.symbol_type_id)

    def set_relationship(self, entity, search_text):
        for coin in self.symbols:
            # Compile regex
            regex = re.compile(
                self.pattern.substitute(
                    fullNameLower=coin.full_name.lower(),
                    fullNameTitle=coin.full_name.title(),
                    symbolLower=coin.symbol.lower(),
                    symbolUpper=coin.symbol.upper()
                ),
                re.S
            )
            # Search provided text for symbols
            result = regex.search(search_text)

            if (result):
                # set relationship between entity_id and symbol_id, if found
                Connection.set(self, query_params={
                    'tablename': 'entity_symbol_lookup',
                    'fields': {
                        'entity_id': entity.id,
                        'symbol_id': coin.symbol_id,
                    }
                })
