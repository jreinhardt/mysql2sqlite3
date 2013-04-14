import unittest
from sqlparser import *

class ParsingTests(unittest.TestCase):
	def test_dataType(self):
		dataType.parseString("int(11) NOT NULL auto_increment")

	def test_columnDescription(self):
		columnDescription.parseString('"ip" text NOT NULL')
		columnDescription.parseString('"id" int(11) NOT NULL auto_increment')
		columnDescription.parseString(""""date" datetime NOT NULL default '0000-00-00 00:00:00'""")

	def test_columnDescriptionList(self):
		delimitedList(columnDescription,",").parseString("""
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  "date" datetime NOT NULL default '0000-00-00 00:00:00',
  "request_method" text NOT NULL,
  "request_uri" text NOT NULL,
  "server_protocol" text NOT NULL,
  "http_headers" text NOT NULL,
  "user_agent" text NOT NULL,
  "request_entity" text NOT NULL,
  "key" text NOT NULL"""
		)

	def test_keyDescription(self):
		keyDescription.parseString('KEY "user_agent" ("user_agent"(10)) ')
		primaryKeyDescription.parseString(' PRIMARY KEY  ("id") ')
		keyDescription.parseString(' KEY "ip" ("ip"(15)) ')

	def test_keyDescriptionList(self):
		delimitedList(keyDescription ^ primaryKeyDescription,",").parseString("""
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15)),
  KEY "user_agent" ("user_agent"(10))"""
		)

	def test_keyColumnDescriptionList(self):
		delimitedList(keyDescription ^ primaryKeyDescription ^ columnDescription,",").parseString("""
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  "date" datetime NOT NULL default '0000-00-00 00:00:00',
  "request_method" text NOT NULL,
  "request_uri" text NOT NULL,
  "server_protocol" text NOT NULL,
  "http_headers" text NOT NULL,
  "user_agent" text NOT NULL,
  "request_entity" text NOT NULL,
  "key" text NOT NULL,
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15)),
  KEY "user_agent" ("user_agent"(10))"""
		)

	def test_createTableStmt(self):
		createTableStmt.parseString("""
CREATE TABLE IF NOT EXISTS "bad_behavior" (
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15))
) AUTO_INCREMENT=1 ;"""
		)

		createTableStmt.parseString("""
CREATE TABLE IF NOT EXISTS "bad_behavior" ( "id" int(11) NOT NULL auto_increment, "ip" text NOT NULL, "date" datetime NOT NULL default '0000-00-00 00:00:00', "request_method" text NOT NULL, "request_uri" text NOT NULL, "server_protocol" text NOT NULL, "http_headers" text NOT NULL, "user_agent" text NOT NULL, "request_entity" text NOT NULL, "key" text NOT NULL, PRIMARY KEY  ("id"), KEY "ip" ("ip"(15)), KEY "user_agent" ("user_agent"(10)) ) ;"""
		)

if __name__ == '__main__':
	unittest.main()
