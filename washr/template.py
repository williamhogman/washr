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

    def derive(self, ext):
        return State(ext, self)

def _render_variable_node(node, state):
    if not state.get(node.name):
        return None

    value = str(state.get(node.name, ""))
    if node.transformation is not None:
        value = transformation_table[node.transformation](value)

    return value

def _render_inner(block, state):
    output = []
    for n in block:
        if isinstance(n, ast.BlockNode):
            value = state.get(n.name)
            if not value:
                continue
            if isinstance(value, dict):
                output.append(_render_inner(n.children, state.derive(value)))
            elif isinstance(value, list):
                parts = [_render_inner(n.children, state.derive(i)) for i in value]
                output.append(''.join(parts))
            else:
                output.append(_render_inner(n.children, state))
        elif isinstance(n, ast.VariableNode):
            value = _render_variable_node(n, state)
            if value:
                output.append(value)
        elif isinstance(n, ast.TextNode):
            output.append(n.content)

    return ''.join(output)

class Template(object):
    def __init__(self, source):
        self._ast = parser.parse(source)

    def render(self, ctx={}):
        return _render_inner(self._ast.children, State(ctx))
