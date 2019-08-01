# Insert Sets
psql -v ON_ERROR_STOP=1 --username "$PPI_USER" --dbname "$PPI_DB" <<-EOSQL
  INSERT INTO ppi.sets (id, symbol, label, parent)
  VALUES
    (0,'field set', 'Field Set',NULL),
    (1,'accounts','Accounts',NULL),
    (2,'members','Members',1),
    (3,'roles','Member Roles',2),
    (10,'diagrams','Diagrams',NULL),
    (20,'sheets','Sheets',NULL),
    (30,'stocks','Stocks',NULL),
    (40,'etfs','ETF''s',NULL),
    (50,'bonds','Bonds',NULL),
    (60,'commodities','Commodities',NULL),
    (70,'crypto','Cryptocurrencies',NULL)
EOSQL

# Insert Fields
psql -v ON_ERROR_STOP=1 --username "$PPI_USER" --dbname "$PPI_DB" <<-EOSQL
  INSERT INTO ppi.fields (id, symbol, label, primary_set)
  VALUES
    (0, 'default_field', 'Default', 0),
EOSQL
