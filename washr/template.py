from washr.parser import ast, grammar
from washr.transformations import transformation_table


class Template(object):
    def __init__(self, source):
        self._ast = ast.parse(grammar.parse(source))

    def render(self, ctx, block=None):
        if block is None:
            block = self._ast
        output = ""
        for n in block.children:
            if isinstance(n, ast.BlockNode):
                output += self.render(ctx, n)
            elif isinstance(n, ast.VariableNode):
                if n.transformation is None:
                    output += ctx.get(n.name, "")
                else:
                    transformator = transformation_table[n.transformation]
                    output += transformator(ctx.get(n.name, ""))
            elif isinstance(n, ast.TextNode):
                output += n.content
        return output
