from washr.parser.grammar import parse


def test():
    test = "{Block:Foo}Blawg  blawg {fooo} lol{/Block:Foo}"
    res = parse(test)
    print(res)

if __name__ == '__main__':
    test()
