# Public Perception Index

## Packages required:

These packages can be installed using `pip install` and the name shown below. Just fucking figure it out, jesus.

* beautifulsoup4
* feedparser
* lxml
* psycopg2

## Useful Resources:

* https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
* http://universaldependencies.org/en/dep/
* https://github.com/Aniruddha-Tapas/How-to-use-SyntaxNet
* https://github.com/tensorflow/models/tree/master/research/syntaxnet


## Glossary

* Entity - Article or content to be parsed. Eg single post in a feed
* Class - The entity category. Initial version will only support the “cryptocurrency” class, but will be expanded to support “stocks” and “brands”
* Symbol - The identifiers for a specific item within a class. For example “BTC” is the symbol for Bitcoin within the Cryptocurrency class.
* Syntax - the modified output of syntaxnet and parsey mcparseface on the the entity.
* Feed - the source url for a listing of entities to be parsed.
* Feed Type - the type of feed. Currently working with RSS with plans to support Twitter, Reddit and others (yelp?)
* Source - Who the entity is credited to. Eg nytimes.com for an RSS feed, or @twiter_handle for Twitter feeds.
