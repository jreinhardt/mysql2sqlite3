import unittest
from pyparsing import ParseResults
from sqlparser import *

class ParsingTests(unittest.TestCase):
	def test_dataType(self):
		dataType.parseString("int(11) NOT NULL auto_increment",parseAll=True)
		dataType.parseString("mediumint(9) NOT NULL auto_increment",parseAll=True)
		dataType.parseString("varchar(255) NOT NULL default ''",parseAll=True)
		dataType.parseString("bigint(20) unsigned NOT NULL auto_increment",parseAll=True)
		dataType.parseString("varchar(255) default NULL",parseAll=True)


	def test_ident(self):
		ident.parseString('"eimer"',parseAll=True)
		ident.parseString('eimer',parseAll=True)
		ident.parseString('`eimer`',parseAll=True)

	def test_columnDescription(self):
		columnDescription.parseString('"ip" text NOT NULL',parseAll=True)
		columnDescription.parseString('"id" int(11) NOT NULL auto_increment',parseAll=True)
		columnDescription.parseString(""""date" datetime NOT NULL default
 '0000-00-00 00:00:00'""",parseAll=True)
		columnDescription.parseString('"comment_ID" bigint(20) unsigned NOT NULL auto_increment',parseAll=True)
		columnDescription.parseString('"comment_author" tinytext NOT NULL',parseAll=True)
		columnDescription.parseString(""""comment_approved" enum('0','1','spam') NOT NULL default '1'""",parseAll=True)


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
  "key" text NOT NULL""",parseAll=True)

	def test_keyDescription(self):
		keyDescription.parseString('KEY "user_agent" ("user_agent"(10)) ',parseAll=True)
		keyDescription.parseString('PRIMARY KEY  ("id") ',parseAll=True)
		keyDescription.parseString('KEY "ip" ("ip"(15)) ',parseAll=True)
		keyDescription.parseString('UNIQUE KEY "id" ("id")',parseAll=True)
		keyDescription.parseString('KEY "link_id" ("link_id","category_id")',parseAll=True)
		keyDescription.parseString('KEY "domain" ("domain"(50),"path"(5))',parseAll=True)

	def test_keyDescriptionList(self):
		delimitedList(keyDescription,",").parseString("""
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15)),
  KEY "user_agent" ("user_agent"(10))""",parseAll=True)

	def test_keyColumnDescriptionList(self):
		delimitedList(keyDescription ^ columnDescription,",").parseString("""
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
  KEY "user_agent" ("user_agent"(10))""",parseAll=True)

	def test_createTableStmt(self):
		createTableStmt.parseString("""CREATE TABLE IF NOT EXISTS "bad_behavior" (
  "id" int(11) NOT NULL auto_increment,
  "ip" text NOT NULL,
  PRIMARY KEY  ("id"),
  KEY "ip" ("ip"(15))
) AUTO_INCREMENT=1""",parseAll=True)

		createTableStmt.parseString("""
CREATE TABLE IF NOT EXISTS "bad_behavior" ( "id" int(11) NOT NULL auto_increment, "ip" text NOT NULL, "date" datetime NOT NULL default '0000-00-00 00:00:00', "request_method" text NOT NULL, "request_uri" text NOT NULL, "server_protocol" text NOT NULL, "http_headers" text NOT NULL, "user_agent" text NOT NULL, "request_entity" text NOT NULL, "key" text NOT NULL, PRIMARY KEY  ("id"), KEY "ip" ("ip"(15)), KEY "user_agent" ("user_agent"(10)) )""",parseAll=True)

	def test_comments(self):
		comment.parseString("-- Eimer",parseAll=True)

		ZeroOrMore(comment ^ White()).parseString("""
-- phpMyAdmin SQL Dump

-- version 2.8.2.4
-- http://www.phpmyadmin.net""")

	def test_insert(self):
		insertStmt.parseString("""
INSERT INTO `wp_11_bad_behavior` (`id`, `ip`, `date`, `request_method`, `request_uri`, `server_protocol`, `http_headers`, `user_agent`, `request_entity`, `key`) VALUES (7, '127.0.0.1', '2000-00-00 00:00:00', 'GET', '/robots.txt', 'HTTP/1.0', 'GET /robots.txt HTTP/1.0\nHost: test.de\nAccept-Encoding: x-gzip, gzip\nUser-Agent: NutchCVS (Nutch; http://lucene.apache.org/nutch/bot.html; nutch-agent@lucene.apache.org)\n', 'NutchCVS (Nutch; http://lucene.apache.org/nutch/bot.html; nutch-agent@lucene.apache.org)', '', '17f4e8c8')""",parseAll=True)

	def test_value(self):
		value.parseString("""
(7, '127.0.0.1', '2000-00-00 00:00:00', 'GET', '/robots.txt', 'HTTP/1.0', 'GET /robots.txt HTTP/1.0\nHost: test.de\nAccept-Encoding: x-gzip, gzip\nUser-Agent: NutchCVS (Nutch; http://lucene.apache.org/nutch/bot.html; nutch-agent@lucene.apache.org)\n', 'NutchCVS (Nutch; http://lucene.apache.org/nutch/bot.html; nutch-agent@lucene.apache.org)', '', '17f4e8c8')""",parseAll=True)


if __name__ == '__main__':
	unittest.main()
