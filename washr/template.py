from washr import parser
from washr.parser import ast
from washr.transformations import transformation_table

class State(object):
    def __init__(self, ctx, parent=None):
        self.ctx = ctx
        self.parent = parent

    def get(self, name, default=None):
        if name in self.ctx:
            return self.ctx[name]

        if self.parent is None:
            return default

        return self.parent.get(name, default)

def _render_inner(block, state):
    output = ""
    for n in block:
        if isinstance(n, ast.BlockNode):
            value = state.get(n.name)
            if not value:
                continue
            if isinstance(value, dict):
                output += _render_inner(n.children, State(value, state))
            elif isinstance(value, list):
                parts = [_render_inner(n.children, State(i, state)) for i in value]
                output += ''.join(parts)
            else:
                output += _render_inner(n.children, state) 
        elif isinstance(n, ast.VariableNode):
            if not state.get(n.name):
                continue

            value = str(state.get(n.name, ""))
            if n.transformation is not None:
                print n.transformation
                value = transformation_table[n.transformation](value)

            output += value
        elif isinstance(n, ast.TextNode):
            output += n.content
    return output

class Template(object):
    def __init__(self, source):
        self._ast = parser.parse(source)

    def render(self, ctx={}, block=None, state=None):
        if state is None:
            state = State(ctx)
        if block is None:
            block = self._ast
        return _render_inner(block.children, state)
