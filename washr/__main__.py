from washr.template import Template


def test():
    test = Template(
        """{Block:Foo}
            Blawg  blawg {fooo} lol{PlaintextTitle}
            {Block:Test}
                <p>{Content}</p>
            {/Block:Test}
            {Block:Posts}
                <h1>{Title}</h1>
            {/Block:Posts}
        {/Block:Foo}"""
    )
    print(test.render({
        "fooo": "Hello!",
        "Title": "<h1>This totally is a test</h1>",
        "Foo": True,
        "Test": {
            "Content": "Hello guys!"
        },
        "Posts": [{
            "Title": "An article"
        }, {
            "Title": "Another article"
        }]
    }))


if __name__ == '__main__':
    test()
