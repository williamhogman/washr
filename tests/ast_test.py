import pytest

from washr.parser import ast, types

def test_parse_empty():
    res = ast.parse([])
    assert res == ast.BlockNode("root", [])


@pytest.fixture
def unbalanced_tokens():
    return [
        types.BlockStart("Foo"),
        "foo",
        types.BlockEnd("derp"),
        types.BlockEnd("Foo"),
    ]


def test_parse_unbalanced_simple(unbalanced_tokens):
    with pytest.raises(ast.MismatchingBlockEnd):
        ast.parse(unbalanced_tokens)


@pytest.fixture
def early_end():
    return [types.BlockEnd("derp")]


def test_early_end(early_end):
    with pytest.raises(ast.UnexpectedBlockEnd):
        ast.parse(early_end)

@pytest.fixture
def close_root_node():
    return [types.BlockEnd("root")]

def test_close_root_node(close_root_node):
    with pytest.raises(ast.UnexpectedBlockEnd):
        ast.parse(close_root_node)


@pytest.fixture
def unclosed_block():
    return [types.BlockStart("foo")]


def test_unclosed_block(unclosed_block):
    with pytest.raises(ast.ExpectedBlockEnd):
        ast.parse(unclosed_block)


@pytest.fixture
def simple_tree_tokens():
    return [
        types.BlockStart("Foo"),
        "Hello",
        types.BlockEnd("Foo"),
    ]


@pytest.fixture
def simple_tree():
    return ast.BlockNode("root", [
        ast.BlockNode("Foo", [
            ast.TextNode("Hello")
        ])
    ])


@pytest.fixture
def simple_tree_str():
    return "{block:Foo}Hello{/block:Foo}"


def test_simple_tree(simple_tree_tokens, simple_tree):
    res = ast.parse(simple_tree_tokens)
    assert res == simple_tree


def test_stringify_simple_tree(simple_tree, simple_tree_str):
    res = ast.stringify(simple_tree)
    assert res == simple_tree_str
