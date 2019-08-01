class Feed:

    def __init__(self, feed_id, url, feed_type_id, symbol_type_id):
        self.entities = []
        self.feed_id = feed_id
        self.feed_type_id = feed_type_id
        self.url = url
        self.symbol_type_id = symbol_type_id;
        self.symbol_type_class = {}
