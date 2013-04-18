#Copyright (c) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
#of the Software, and to permit persons to whom the Software is furnished to do
#so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyparsing import Literal, Word, CaselessKeyword as Keyword, delimitedList, Optional, alphas, nums, alphanums, Forward, oneOf, QuotedString, ZeroOrMore, ParseException, Group, Combine, LineStart, LineEnd, printables, StringEnd, CharsNotIn, White

def convert_datatypes(toks):
	if toks[0] == 'int' or toks[0] == 'mediumint' or toks[0] == 'bigint':
		return ["integer"] + toks[2:]
	if toks[0] == "enum":
		return ["varchar(255)"] + toks[3:]

def rebuild_createtable(toks):
	ts = toks.asList()
	return ts[0] + [", ".join([" ".join(t) for t in ts[1:-1]])] + ts[-1]		

def rebuild_insert(toks):
	ts = toks.asList()
	res = []
	prefix = ts[0][:4] + [", ".join(ts[0][4:-2])] + ts[0][-2:]
	for vs in ts[1:]:
		value = [vs[0] + ", ".join(vs[1:-1]) + vs[-1]]
		res += prefix + value + [";\n"]
	return res
createToken = Keyword("CREATE")
databaseToken = Keyword("DATABASE")
tableToken = Keyword("TABLE")
ifneToken = Keyword("IF") + Keyword("NOT") + Keyword("EXISTS")
nullToken = Keyword("NULL")
nnToken = Keyword("NOT") + nullToken
collateToken = Keyword("COLLATE")
dcsToken = Keyword("DEFAULT") + Keyword("CHARACTER") + Keyword("SET")
useToken = Keyword("USE")
defaultToken = Keyword("DEFAULT")
unsignedToken = Keyword("UNSIGNED")
autoincrementToken = Keyword("AUTO_INCREMENT")
autoincrementToken.setParseAction(lambda toks: ["PRIMARY KEY AUTOINCREMENT"])
keyToken = Keyword("KEY")
primaryToken = Keyword("PRIMARY")
uniqueToken = Keyword("UNIQUE")
insertToken = Keyword("INSERT")
intoToken = Keyword("INTO")
valuesToken = Keyword("VALUES")

ident = Word(alphas, alphanums + "_$" ) ^ QuotedString('"') ^ QuotedString("`")
ident.setParseAction(lambda toks: ['"%s"' % toks[0]])
string = QuotedString("'",multiline=True)
string.setParseAction(lambda toks: ["'%s'" % toks[0]])

columnName = delimitedList( ident, ".",combine=True)
tableName = delimitedList( ident, ".",combine=True)
dataType = Word(alphas) + Combine(Optional(Literal("(") + (Word(nums) ^ delimitedList(string,combine=True)) + Literal(")"))) + ZeroOrMore(nnToken ^ autoincrementToken ^ (defaultToken + (string ^ nullToken)) ^ unsignedToken.suppress() )
dataType.setParseAction(convert_datatypes)

columnDescription = Group(ident + dataType)
keyDescription = Optional(primaryToken ^ uniqueToken) + keyToken + Optional(ident) + Literal("(") + delimitedList(ident + Optional(Literal("(") + Word(nums) + Literal(")"))) + Literal(")")

createTableStmt = Group(createToken + tableToken + ifneToken + ident + Literal("(")) + delimitedList(columnDescription ^ keyDescription.suppress()) + Group(Literal(")")) + Optional(autoincrementToken + Literal("=") + Word(nums)).suppress()
createTableStmt.setParseAction(rebuild_createtable)


createDataBaseStmt = Group(createToken + databaseToken + ident +  dcsToken + Word(alphanums)+ collateToken + ident)

useStmt = Group(useToken + ident)

comment = LineStart() + CharsNotIn("\n") + LineEnd()

value = Group(Literal("(") + delimitedList(Word(nums) ^ string) + Literal(")"))

insertPrefix = Group(insertToken + intoToken + ident + Literal("(") + delimitedList(ident) + Literal(")") + valuesToken)

insertStmt = insertPrefix + delimitedList(value)
insertStmt.setParseAction(rebuild_insert)

statement = ((createTableStmt ^ createDataBaseStmt.suppress() ^ useStmt.suppress() ^ insertStmt)  + Literal(";").setParseAction(lambda: [";\n"])) ^ comment.suppress() ^ White().suppress()

sql = ZeroOrMore(statement)
