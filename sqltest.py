from pyparsing import ParseException
from sqlparser import * 

def test(parser, string):
	try:
		tokens = parser.parseString( string )
	except ParseException, err:
		print string,"->"
		print " "*err.loc + "^\n" + err.msg
		print err
		print

test(dataType,"int(11) NOT NULL auto_increment")
test(columnDescription,'"ip" text NOT NULL')
test(columnDescription,'"id" int(11) NOT NULL auto_increment')
test(columnDescription,""""date" datetime NOT NULL default '0000-00-00 00:00:00'""")
test(delimitedList(columnDescription,","),"""
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  "date" datetime NOT NULL default '0000-00-00 00:00:00',
  "request_method" text NOT NULL,
  "request_uri" text NOT NULL,
  "server_protocol" text NOT NULL,
  "http_headers" text NOT NULL,
  "user_agent" text NOT NULL,
  "request_entity" text NOT NULL,
  "key" text NOT NULL,""")
test(keyDescription,'KEY "user_agent" ("user_agent"(10)) ')


test(primaryKeyDescription,' PRIMARY KEY  ("id") ')
test(keyDescription,' KEY "ip" ("ip"(15)) ')
test(delimitedList(keyDescription | primaryKeyDescription,","), """
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15)),
  KEY "user_agent" ("user_agent"(10))
""")

test(delimitedList(keyDescription | columnDescription,","),"""
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
  KEY "user_agent" ("user_agent"(10))
""")


test(createTableStmt,"""
CREATE TABLE IF NOT EXISTS "bad_behavior" (
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15))
) AUTO_INCREMENT=1 ;
""")

test(createTableStmt,"""
CREATE TABLE IF NOT EXISTS "bad_behavior" ( "id" int(11) NOT NULL auto_increment, "ip" text NOT NULL, "date" datetime NOT NULL default '0000-00-00 00:00:00', "request_method" text NOT NULL, "request_uri" text NOT NULL, "server_protocol" text NOT NULL, "http_headers" text NOT NULL, "user_agent" text NOT NULL, "request_entity" text NOT NULL, "key" text NOT NULL, PRIMARY KEY  ("id"), KEY "ip" ("ip"(15)), KEY "user_agent" ("user_agent"(10)) ) ;
""")


