from collections import namedtuple
from washr.parser import types

BlockNode = namedtuple("BlockNode", ("name", "children"))
VariableNode = namedtuple("VariableNode", ("name"))
TextNode = namedtuple("TextNode", ("content"))

class IllegalBlockEnd(Exception):
    pass

def parse(tokens):
    root_node = BlockNode("root", [])
    blocks = [root_node]
    
    for t in tokens:
        if type(t) == str:
            blocks[-1].children.append(TextNode(t))
        elif type(t) == types.Variable:
            blocks[-1].children.append(VariableNode(t.name))
        elif type(t) == types.BlockStart:
            blocks.append(BlockNode(t.name, []))
        elif type(t) == types.BlockEnd:
            if len(blocks) < 2 or t.name != blocks[-1].name:
                raise IllegalBlockEnd
            last_block = blocks.pop()
            blocks[-1].children.append(last_block)

    return root_node
