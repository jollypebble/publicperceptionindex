import urllib, json
from string import Template
from db.connection import Connection

class SymbolExchangeRateScraper(Connection):
    def __init__(self):
        Connection.__init__(self)
        exchanges = self.get_exchanges()
        for exchange in exchanges:
            source = self.request_source(exchange[2])
            symbol_exchange_rates = json.loads(source)
            for sym in symbol_exchange_rates:
                # TODO: Load correct endpoint field names by exchange
                args = {
                    'tablename': 'symbol',
                    'conditional': 'AND',
                    'where_stmt': [
                        {
                            'key':'symbol',
                            'value':sym['symbol'],
                            'operator':'='
                        },
                        {
                            'key':'symbol_type_id',
                            'value':exchange[1],
                            'operator':'='
                        }
                    ]
                }
                exists = Connection.exists(self, args)
                # Add symbol to table if it does not exist.
                if ( not exists ) :
                    Connection.set(self, query_params={
                        'tablename': 'symbol',
                        'fields': {
                            'symbol_type_id': exchange[1],
                            'symbol': sym['symbol'],
                            'name': sym['id'],
                            'meta': '',
                            'full_name': sym['name']
                        }
                    })

                # Get our symbol id
                # TODO: We need to grab this symbol id from an object cache.
                # See https://trello.com/c/nivVoxpF
                symbol_id = Connection.get(self, query_params={
                    'tablename': 'symbol',
                    'where_stmt': [
                        {
                            'key':'symbol',
                            'value':sym['symbol'],
                            'operator':'='
                        },
                        {
                            'key':'symbol_type_id',
                            'value':exchange[1],
                            'operator':'='
                        }
                    ],
                    'fields': [
                        'symbol_id'
                    ]
                })

                # Insert most recent exchange rate.
                if ( sym['last_updated'] ):
                    Connection.set(self, query_params={
                        'tablename': 'symbol_exchange_rate_lookup',
                        'fields': {
                            'exchange_id': exchange[0],
                            'symbol_id': symbol_id[0][0],
                            'rate': sym['price_usd'],
                            'date': Connection.convert_timestamp_to_datetime(self, sym['last_updated'])
                        }
                    })

    # @todo load source JSON once into memory via a separate class
    def request_source(self,sourceUrl):
        response = urllib.urlopen(sourceUrl)
        return response.read()

    def get_exchanges(self):
        args = {
            'tablename': 'exchange',
            'fields': [
                'exchange_id',
                'symbol_type_id',
                'url',
                'name'
            ]
        }
        return self.get(args)


SymbolExchangeRateScraper()
