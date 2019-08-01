from config import auth
import psycopg2
from psycopg2.sql import SQL, Identifier, Literal
from string import Template
import utils
import datetime

class Connection:
    connection = False

    def __init__(self, set_query=''):
        Connection.connection = Connection.connection if Connection.connection else self.get_connection()
        Connection.connection.autocommit = True

        self.set_query = "INSERT INTO {0} ({1}) VALUES ({2});"
        self.get_query = "SELECT {0} FROM {1} WHERE {2};"
        self.update_query = "UPDATE {0} SET {1} = {2} WHERE {3};"
        self.count_query = "SELECT COUNT(1) as num FROM {0} WHERE {1};"

    def get_connection(self):
        conn_string = Template("host=${host} dbname=${dbname} user=${user} password=${password}")
        connect_config = conn_string.substitute(auth['database'])
        return psycopg2.connect(connect_config)

    def build_where(self, query_params):
        where_stmt = [];
        key = Literal(1)
        value = Literal(1)
        conditional = 'AND' if not utils.exists('conditional', query_params) else query_params['conditional']
        operator = '='

        if ('where_stmt' in query_params and query_params['where_stmt']):
            for part in query_params['where_stmt']:
                operator = operator if not part['operator'] else part['operator']
                if ( part['key'] and part['value'] ):
                    key = Identifier(part['key'])
                    value = Literal(part['value'])
                where_stmt.append(SQL(operator).join([key, value]))
        else:
            where_stmt.append(SQL(operator).join([key, value]))

        conditional += ' '
        return SQL(conditional).join(where_stmt)

    def build_comma_separated(self, array, type=Identifier):
        parts = [];
        for value in array:
            parts.append(type(value))
        return SQL(', ').join(parts)

    def resolve_query(self, query, fetch=False):
        result = False;
        # make cursor, execute query, close cursor
        cursor = Connection.connection.cursor()
        cursor.execute(query)
        if (fetch):
            result = cursor.fetchall()

        cursor.close()
        return result

    def update(self, query_params):
        tablename = query_params['tablename']
        # join fields and values
        fields = self.build_comma_separated(list(query_params['fields'].keys()));
        values = self.build_comma_separated(
            list(query_params['fields'].values()),
            Literal
        );

        # Build our where statement
        where_stmt = self.build_where(query_params);

        # create query string
        query = SQL(self.update_query).format(
            Identifier(tablename),
            fields,
            values,
            where_stmt
        );
        print 'Executing SQL: '
        print query.as_string(Connection.connection)
        self.resolve_query(query)

    def set(self, query_params):
        tablename = query_params['tablename']
        # join fields
        fields = self.build_comma_separated(list(query_params['fields'].keys()));
        values = self.build_comma_separated(
            list(query_params['fields'].values()),
            Literal
        );

        # create query string
        query = SQL(self.set_query).format(Identifier(tablename), fields, values);
        print 'Executing SQL: '
        print query.as_string(Connection.connection)
        self.resolve_query(query)

    def get(self, query_params):
        tablename = query_params['tablename']
        # Build our where statement
        where_stmt = self.build_where(query_params);
        # join fields
        fields = self.build_comma_separated(query_params['fields']);
        # create query string
        query = SQL(self.get_query).format(fields, Identifier(tablename), where_stmt);

        print 'Executing SQL: '
        print query.as_string(Connection.connection)
        return self.resolve_query(query, True)

    def exists( self, query_params ):
        tablename = query_params['tablename']
        # Build our where statement
        where_stmt = self.build_where(query_params);

        query = SQL(self.get_query).format(Literal('*'),Identifier(tablename), where_stmt);
        cursor = Connection.connection.cursor()
        cursor.execute(query)
        cursor.fetchone()
        count = cursor.rownumber
        cursor.close()
        return count

    def convert_timestamp_to_datetime(self, ts):
        return datetime.datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
