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

class Template(object):
    def __init__(self, source):
        self._ast = parser.parse(source)

    def render(self, ctx={}, block=None, state=None):
        if state is None:
            state = State(ctx)
        if block is None:
            block = self._ast
        output = ""
        for n in block.children:
            if isinstance(n, ast.BlockNode):
                value = state.get(n.name)
                if not value:
                    continue
                if isinstance(value, dict):
                    output += self.render(block=n, state=State(value, state))
                elif isinstance(value, list):
                    output += ''.join([self.render(
                        block=n, state=State(i, state)
                    ) for i in value])
                else:
                    output += self.render(block=n, state=state) 
            elif isinstance(n, ast.VariableNode):
                if not state.get(n.name):
                    continue
                value = str(state.get(n.name, ""))
                if n.transformation is None:
                    output += value
                else:
                    transformator = transformation_table[n.transformation]
                    output += transformator(value)
            elif isinstance(n, ast.TextNode):
                output += n.content
        return output
