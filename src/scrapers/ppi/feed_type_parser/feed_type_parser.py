from feed.feed import Feed
from symbol_type.cryptocurrency import CryptocurrencySymbolType
from db.connection import Connection


class FeedTypeParser(Connection):
    # Symbol types are manually entered, so this is a mapping
    # from symbol type id to a class that handles that symbol type's data
    symbol_type_class_mapping = {
        1: CryptocurrencySymbolType()
    }

    def __init__(self):
        Connection.__init__(self)
        self.feeds = []

    def get(self, feed_type_id):
        fields = [
            'feed_id',
            'url',
            'feed_type_id',
            'symbol_type_id'
        ]
        # get all available feeds of provided type
        feeds = Connection.get(self, query_params={
            'tablename': 'feed',
            'fields': fields,
            'where_stmt': [
                {
                    'key': 'feed_type_id',
                    'value': feed_type_id
                }
            ]
        })

        # loop feeds, create a new feed class,
        # and associate with a symbol type class for use in entity processing
        for feed in feeds:
            values = dict(zip(fields, list(feed)))
            new_feed = Feed(**values)
            new_feed.symbol_type_class = self.symbol_type_class_mapping[new_feed.symbol_type_id]
            self.feeds.append(new_feed)
