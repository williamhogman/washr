from washr.template import Template

def test():
    test = Template(
        "{Block:Foo}Blawg  blawg {fooo} lol{PlaintextTitle}{/Block:Foo}"
    )
    print(test.render({
        "fooo": "Hello!",
        "Title": "<h1>This totally is a test</h1>"
    }))

if __name__ == '__main__':
    test()
