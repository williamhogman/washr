from pyparsing import Literal, CharsNotIn, alphas, Word, ZeroOrMore, Forward

from washr.parser.types import Variable, BlockStart, BlockEnd

import collections


left_edge = Literal("{")

right_edge = Literal("}")

block_token = Literal("Block:")

end_token = Literal("/")

text = CharsNotIn("{}")

identifier = Word(alphas)


variable = left_edge + identifier.setResultsName("name") + right_edge

variable.setParseAction(lambda x: Variable(x.name))

theme_part = Forward()

block_ident = block_token + identifier.setResultsName("name")

block_begin = left_edge + block_ident + right_edge

block_begin.setParseAction(lambda x: BlockStart(x.name))

block_end = left_edge + end_token + block_ident + right_edge

block_end.setParseAction(lambda x: BlockEnd(x.name))

theme_part << (variable ^ text ^ block_begin ^ block_end)

theme = ZeroOrMore(theme_part)


def parse(source):
    return theme.parseString(source)
