from collections import namedtuple

Variable = namedtuple("Variable", ("name", "transformation"))

BlockStart = namedtuple("BlockStart", ("name"))

BlockEnd = namedtuple("BlockEnd", ("name"))
