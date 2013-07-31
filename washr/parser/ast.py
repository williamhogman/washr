from collections import namedtuple
from washr.parser import types

BlockNode = namedtuple("BlockNode", ("name", "children"))
VariableNode = namedtuple("VariableNode", ("name", "transformation"))
TextNode = namedtuple("TextNode", ("content"))

class ExpectedBlockEnd(Exception): pass
class UnexpectedBlockEnd(Exception): pass
class MismatchingBlockEnd(Exception): pass

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
            output += ("{Block:" + n.name + "}" + stringify(n) + "{/Block:" +
                n.name + "}")
        elif isinstance(n, VariableNode):
            output += "{" + n.transformation + n.name + "}"
        elif isinstance(n, TextNode):
            output += n.content
    return output
