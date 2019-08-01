import lxml, requests, copy, json
from pythonMcparseface import pyparseface
from bs4 import BeautifulSoup
from urlparse import urlparse
from default_syntax_dict import default_syntax_dict
from db.connection import Connection


class Entity(Connection):

    def __init__(self, title, date, description, url, metadata={}):
        Connection.__init__(self)
        url_parts = urlparse(url)

        self.id = 0;
        self.title = title
        self.date = date
        self.url = url
        self.source = url_parts.netloc
        self.metadata = metadata
        self.description = description
        # self.scrape_meta_tags(['description'])
        self.syntax_tree = {}
        # self.construct_syntax_tree()

        self.set()

    def set(self):
        entity_id = Connection.set(self, query_params={
            'tablename': 'entity',
            'returning': ['entity_id'],
            'fields': {
                'title': self.title,
                'url': self.url,
                'publish_date': self.date,
                'description': self.description,
                'meta_data': json.dumps(self.metadata),
                'syntax_tree': json.dumps(self.syntax_tree),
                'entity_type_id': 0, # @todo make this a real entity type ID
            }
        })
        print entity_id[0]
        self.id = entity_id[0]

    def set_syntax_tree(self):
        Connection.set(self, query_params={
            'tablename': 'entity_syntax',
            'fields': {
                'entity_id': self.id,
                'pos': pos,
                'word': word,
                'distance_measure_string': distance_measure_string
            }
        })

    # Use title and description to generate syntax tree
    def construct_syntax_tree(self):
        titleTree = self.parse_syntax(self.title)
        return self.format_syntax_tree(
            titleTree,
            copy.deepcopy(default_syntax_dict)
        )

    # Retreive content attribute from <meta> tags with given properties from entity HTML
    def scrape_meta_tags(self, properties):
        response = requests.get(self.url)
        encoding = response.encoding if 'charset' in response.headers.get('content-type', '').lower() else None
        html_source = BeautifulSoup(response.content, 'html.parser', from_encoding=encoding)

        # Build selector
        selector_parts = [];
        for prop in properties:
            selector_parts.append('meta[property="%(prop)s"]' % locals())
            selector_parts.append('meta[name="%(prop)s"]' % locals())

        # Return value of content attribute from from first tag found
        tags = html_source.head.select(','.join(selector_parts))
        if (tags and len(tags)):
            return tags[0]['content']

        return False

    # Strip out any html tags and unicode characters
    def strip_html(self, text):
        text = BeautifulSoup(text, 'lxml').get_text()
        return ''.join([i if ord(i) < 128 else ' ' for i in text])

    # Parse using syntaxnet
    def parse_syntax(self, text):
        try:
            return pyparseface.parse_sentence(text)
        except UnicodeEncodeError as e:
            print 'Failed to parse text: {0}'.format(e)

    # Split up syntax tree into a more useful dictionary
    def format_syntax_tree(self, source_tree, target):
        parts_of_speech = target.keys()

        # Some have no children
        if (not source_tree):
            return target

        for part in source_tree:
            target = self.format_syntax_tree(
                source_tree[part],
                target
            )
            word, pos, dep = part.split(' ')

            # This could be a comma or something, return if it's not a valid part of speech
            if (pos not in parts_of_speech):
                continue

            target[pos]['values'].append(word)
            target[pos]['deps'].append(dep)

        return target
