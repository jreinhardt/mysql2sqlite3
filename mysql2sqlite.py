import pyparsing
from sqlparser import *
from sys import argv

comment = comment.suppress()

if len(argv) < 2:
	print "Usage mysqldump.sql"
inp = open(argv[1]).read()
stmts = sql.parseString(inp)

out = open(argv[1] + ".sqlite3.sql","w")
out.write(" ".join(stmts))
