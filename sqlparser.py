from pyparsing import Literal, Word, CaselessKeyword as Keyword, delimitedList, Optional, alphas, nums, alphanums, Forward, oneOf, QuotedString, ZeroOrMore, ParseException, Group, Combine, LineStart, LineEnd, printables

createToken = Keyword("create")
databaseToken = Keyword("database")
tableToken = Keyword("table")
ifneToken = Keyword("if") + Keyword("not") + Keyword("exists")
nnToken = Keyword("not") + Keyword("null")
collateToken = Keyword("collate")
dcsToken = Keyword("default") + Keyword("character") + Keyword("set")
useToken = Keyword("use")
defaultToken = Keyword("default")
autoincrementToken = Keyword("auto_increment")
keyToken = Keyword("key")
primaryToken = Keyword("primary")
insertToken = Keyword("insert")
intoToken = Keyword("into")
valuesToken = Keyword("values")

ident = Word( alphas, alphanums + "_$" ) | QuotedString('"') | QuotedString("`")

columnName = Group(delimitedList( ident, "."))
tableName = Group(delimitedList( ident, "."))
dataType = Word(alphas) + Optional(Literal("(") + Word(nums) + Literal(")")) + ZeroOrMore(nnToken ^ autoincrementToken ^ (defaultToken + QuotedString("'")))

columnDescription = Group(ident + dataType)
keyDescription = Group(keyToken + (ident) + Literal("(") + ident + Literal("(") + Word(nums) + Literal(")") + Literal(")"))
primaryKeyDescription = Group(primaryToken + keyToken + Literal("(") + ident + Literal(")"))

createTableStmt = createToken + tableToken + ifneToken + ident + Literal("(") + delimitedList(columnDescription ^ keyDescription ^ primaryKeyDescription) + Literal(")") + Optional(autoincrementToken + Literal("=") + Word(nums))

createDataBaseStmt = createToken + databaseToken + ident + dcsToken + Word(alphanums) + collateToken + ident

useStmt = useToken + ident

comment = LineStart() + Literal("--") + Word(printables) + LineEnd()

value = Literal("(") + delimitedList(Word(nums) ^ QuotedString("'",multiline=True)) + Literal(")")

insertStmt = insertToken + intoToken + ident + Literal("(") + delimitedList(ident) + Literal(")") + valuesToken + delimitedList(value)

statement = ((createTableStmt ^ createDataBaseStmt ^ useStmt ^ insertStmt)  + Literal(";")) ^ comment


sql = ZeroOrMore(statement)
