from pyparsing import (Literal, CharsNotIn, alphanums,
                       Word, ZeroOrMore, Forward,
                       Optional, CaselessLiteral)

from washr.parser.types import Variable, BlockStart, BlockEnd


left_edge = Literal("{")

right_edge = Literal("}")

block_token = CaselessLiteral("block:")

end_token = Literal("/")

text = CharsNotIn("{}")

identifier = Word(alphanums + "-")

transformation_keyword = (
    Literal("Plaintext") ^ Literal("JS") ^
    Literal("JSPlaintext") ^ Literal("URLEncoded") ^ Literal("RGB")
).setResultsName("transformation")


variable = (left_edge + Optional(transformation_keyword) +
            identifier.setResultsName("name") + right_edge)

variable.setParseAction(lambda x: Variable(x.name, x.transformation or None))

theme_part = Forward()

block_ident = block_token + identifier.setResultsName("name")

block_begin = left_edge + block_ident + right_edge

block_begin.setParseAction(lambda x: BlockStart(x.name))

block_end = left_edge + end_token + block_ident + right_edge

block_end.setParseAction(lambda x: BlockEnd(x.name))

theme_part << (variable ^ text ^ block_begin ^ block_end)

theme = ZeroOrMore(theme_part).leaveWhitespace()


def parse(source):
    return theme.parseString(source)
