import urllib, json, re, os
from symbol_type import SymbolType
from symbol import Symbol
from mock_data.coin_data import coin_data


class CryptocurrencySymbolType(SymbolType):
    # @todo load source JSON once into memory via a separate class
    def request_source(self):
        self.source = coin_data
        self.class_name = 'cryptocurrency'

    def find_coin(self):
        for coin in self.source:
            # Test regex
            regex = re.compile(
                self.pattern.substitute(
                    fullNameLower=coin['name'].lower(),
                    fullNameTitle=coin['name'].title(),
                    nameLower=coin['symbol'].lower(),
                    nameUpper=coin['symbol'].upper()
                ),
                re.S
            )
            result = regex.search(self.title)

            # if found, add to symbols
            if (result):
                self.symbols.append(
                    Symbol(
                        symbol_type_type=self.class_name
                        name=coin['symbol']
                        full_name=coin['name']
                        alt_name=coin['id']
                    )
                )
