from washr.parser import grammar, ast


def test():
    test = "{Block:Foo}Blawg  blawg {fooo} lol{/Block:Foo}"
    tokens = grammar.parse(test)
    tree = ast.parse(tokens)
    print(tree)

if __name__ == '__main__':
    test()
