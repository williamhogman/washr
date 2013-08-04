from collections import namedtuple
from washr.parser import types

BlockNode = namedtuple("BlockNode", ("name", "children"))
VariableNode = namedtuple("VariableNode", ("name", "transformation"))
TextNode = namedtuple("TextNode", ("content"))


class ExpectedBlockEnd(Exception):
    """Raised when the parser expects a block end up can't find it"""


class UnexpectedBlockEnd(Exception):
    """Raised when the parser finds a BlockEnd when it doesn't expect it"""


class MismatchingBlockEnd(Exception):
    """When an BlockEnd with a name not matching the current block is found"""


def parse(tokens):
    root_node = BlockNode("root", [])
    blocks = [root_node]

    for t in tokens:
        if type(t) == str:
            blocks[-1].children.append(TextNode(t))
        elif type(t) == types.Variable:
            blocks[-1].children.append(VariableNode(t.name, t.transformation))
        elif type(t) == types.BlockStart:
            blocks.append(BlockNode(t.name, []))
        elif type(t) == types.BlockEnd:
            if len(blocks) == 1:
                raise UnexpectedBlockEnd(t.name)
            if t.name != blocks[-1].name:
                raise MismatchingBlockEnd(t.name)
            last_block = blocks.pop()
            blocks[-1].children.append(last_block)

    if len(blocks) != 1:
        raise ExpectedBlockEnd(blocks[-1].name)

    return root_node


def stringify(block):
    output = ""
    for n in block.children:
        if isinstance(n, BlockNode):
            fmt = "{{Block:{0}}}{1}{{/Block:{0}}}"
            output += fmt.format(n.name, stringify(n))
        elif isinstance(n, VariableNode):
            fmt = "{{{0}{1}}}"
            output += fmt.format(n.transformation or "", n.name)
        elif isinstance(n, TextNode):
            output += n.content
    return output
