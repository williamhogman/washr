from washr.parser import grammar, ast

def test():
    test = "{Block:Foo}Blawg  blawg {fooo} lol{/Block:Foo}"
    tokens = grammar.parse(test)
    tree = ast.parse(tokens)
    print(tree)
    output = ast.stringify(tree)
    print(output)
    assert(output == test)

if __name__ == '__main__':
    test()
