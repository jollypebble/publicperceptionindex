import feedparser
from feed.feed import Feed
from entity.entity import Entity
from feed_type_parser import FeedTypeParser


class NewsFeedTypeParser(FeedTypeParser):
    # Feed type is manually entered,
    # so this is a hard-coded value
    feed_type_id = 1

    def __init__(self):
        FeedTypeParser.__init__(self)
        self.get(self.feed_type_id)
        self.scrape()

    # Loop feeds and parse RSS, assumes all news feeds are RSS
    def scrape(self):
        for feed in self.feeds:
            data = feedparser.parse(feed.url)
            feed.entities = self.construct_entities(data, feed)

    # Loop through all the entries in the parsed RSS
    # and init a new Entity class for each
    def construct_entities(self, data, feed):
        entities = [];

        for entity in data['entries'][0:1]:
            # add entity to entity manifest
            new_entity = Entity(
                title=entity.title,
                date=entity.published,
                description=entity.summary,
                url=entity.link
            )
            entities.append(new_entity)
            # search entity title for symbols
            feed.symbol_type_class.set_relationship(new_entity, 'This is an article about BTC')

        return entities;
