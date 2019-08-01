#!/bin/bash
set -e

# Create our user
psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "postgres" <<-EOSQL
	CREATE USER $PPI_USER WITH PASSWORD '$POSTGRES_PASSWORD';
	CREATE DATABASE $PPI_DB;
	GRANT ALL PRIVILEGES ON DATABASE $PPI_DB TO $PPI_USER;
EOSQL

# Create our data tables and relational architecture.
psql -v ON_ERROR_STOP=1 --username "$PPI_USER" --dbname "$PPI_DB" <<-EOSQL
	CREATE SCHEMA ppi;
	CREATE TABLE ppi.sets (
		"id"         	BIGSERIAL PRIMARY KEY,
		"symbol"     	varchar(255) NOT NULL UNIQUE,
		"label"      	text NULL,
		"parent"     	INTEGER NULL DEFAULT NULL,
		"data"       	JSONB NULL,
		FOREIGN KEY (parent) REFERENCES ppi.sets(id)
	);

	CREATE TYPE field_type AS ENUM ('string', 'number', 'currency', 'coordinate', 'object', 'list', 'search', 'bool', 'date', 'time');

	CREATE TYPE field_value AS (
	   "string" TEXT,
	   "number" BIGINT,
	   "currency" MONEY,
		 "coordinate" POINT,
		 "object" JSONB,
		 "list" TEXT[],
		 "search" TSQUERY,
		 "bool" BOOLEAN,
		 "date" DATE,
		 "time" TIME with time zone
	);

	CREATE TABLE ppi.fields (
		"id"         	BIGSERIAL PRIMARY KEY,
		"symbol"     	VARCHAR(255) NOT NULL UNIQUE,
		"label"      	text NULL,
		"primary_set"	INTEGER NULL,
		"type"				field_type NULL DEFAULT 'string',
		"parent"     	INTEGER NULL DEFAULT 0,
		"data"       	JSONB NULL,
		FOREIGN KEY (parent) REFERENCES ppi.fields(id),
		FOREIGN KEY (primary_set) REFERENCES ppi.sets(id)
	);

	CREATE TABLE ppi.field_sets (
		"id"         	BIGSERIAL PRIMARY KEY,
		"field_id" 		INTEGER NULL,
		"set_id" 			INTEGER NULL,
		"order"     	INTEGER NULL,
		"parent"     	INTEGER NULL DEFAULT 0,
		FOREIGN KEY (parent) REFERENCES ppi.field_sets(id),
		FOREIGN KEY (field_id) REFERENCES ppi.fields(id),
		FOREIGN KEY (set_id) REFERENCES ppi.sets(id)
	);

	CREATE TABLE ppi.members (
		"id"         	BIGSERIAL PRIMARY KEY,
		"label"      	text NULL,
		"data"       	JSONB NULL
	);

	CREATE TABLE ppi.roles (
		"id"         	BIGSERIAL PRIMARY KEY,
		"symbol"     	VARCHAR(255) NOT NULL UNIQUE,
		"label"      	text NULL,
		"data"       	JSONB NULL
	);

	CREATE TABLE ppi.accounts (
		"id"         			BIGSERIAL PRIMARY KEY,
		"label"      			text NULL,
		"primary_member"	INTEGER NULL,
		"parent"     			INTEGER NULL DEFAULT 0,
		"data"       			JSONB NULL,
		FOREIGN KEY (parent) REFERENCES ppi.accounts(id),
		FOREIGN KEY (primary_member) REFERENCES ppi.members(id)
	);

	CREATE TABLE ppi.account_members (
		"account_id"	INTEGER NULL,
		"member_id"		INTEGER NULL,
		"role_id"			INTEGER NULL,
		PRIMARY KEY("account_id","member_id","role_id"),
		FOREIGN KEY (account_id) REFERENCES ppi.members(id),
		FOREIGN KEY (member_id) REFERENCES ppi.accounts(id),
		FOREIGN KEY (role_id) REFERENCES ppi.roles(id)
	);

	CREATE TABLE ppi.portfolios (
		"id"         		BIGSERIAL PRIMARY KEY,
		"owner"					INTEGER NULL,
		"field_set_id"  INTEGER NULL,
		"status"   			VARCHAR(255) NULL,
		"parent"     		INTEGER NULL DEFAULT 0,
		"data"       		JSONB NULL,
		FOREIGN KEY (field_set_id) REFERENCES ppi.field_sets(id),
		FOREIGN KEY (owner) REFERENCES ppi.members(id)
	);

	CREATE TABLE ppi.portfolio_screeners (
		"id"						BIGSERIAL PRIMARY KEY,
		"portfolio_id"  INTEGER NOT NULL,
		"timestamp"   	timestamp NULL,
		"data"       		JSONB NULL,
		FOREIGN KEY (portfolio_id) REFERENCES ppi.portfolios(id)
	);

	CREATE TABLE ppi.field_screeners (
		"id"											BIGSERIAL PRIMARY KEY,
		"portfolio_screener_id"  	INTEGER NOT NULL,
		"field_id" 								INTEGER NOT NULL,
		"value"   								field_value NULL,
		FOREIGN KEY (portfolio_screener_id) REFERENCES ppi.portfolio_screeners(id),
		FOREIGN KEY (field_id) REFERENCES ppi.fields(id)
	);
EOSQL
