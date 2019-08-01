import pprint
from pythonMcparseface import pyparseface
from scrapers.symbol_exchange_rate_scraper import SymbolExchangeRateScraper

pp = pprint.PrettyPrinter(indent=2)

rate_scraper = SymbolExchangeRateScraper()

symbolType = CryptocurrencySymbolType()
symbolType.get()

#from feed_type_parser.news import NewsFeedTypeParser

#pp = pprint.PrettyPrinter(indent=2)

#parser = NewsFeedTypeParser()
