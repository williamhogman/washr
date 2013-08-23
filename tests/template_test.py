from washr.template import Template, State
from washr.parser import ast
from mock import sentinel, patch, Mock

def test_state_get():
    state = State({"foo": sentinel.get})
    assert state.get("foo") == sentinel.get

def test_state_get_none_default():
    state = State({})
    assert state.get("foo") == None

def test_state_value_default():
    state = State({})
    assert state.get("bar", sentinel.default) == sentinel.default

def test_state_nested():
    inner_state = State({"foo": sentinel.nested})
    state = State({}, inner_state)
    assert state.get("foo") == sentinel.nested

def test_tri_nested_state():
    inner_inner_state = State({"foo": sentinel.nested})
    inner_state = State({}, inner_inner_state)
    state = State({}, inner_state)

    assert state.get("foo") == sentinel.nested


@patch("washr.parser.parse", return_value=sentinel.ast)
def test_template_compiles(parse_mock):
    t = Template(sentinel.code)

    parse_mock.assert_was_called_once_with(sentinel.code)
    
    assert t._ast == sentinel.ast


ast_fixture = ast.BlockNode("root", [
    ast.VariableNode(sentinel.x, None),
    ast.VariableNode(sentinel.x, sentinel.transform),
    ast.TextNode("text"),
    ast.BlockNode(sentinel.y, [
        ast.VariableNode(sentinel.x, None),
        ast.VariableNode(sentinel.y, None),
        ast.TextNode("loop_text")
    ])
])

context_fixture = {
    sentinel.x: "plainx",
    sentinel.y: [
        {sentinel.x: "xloop1", sentinel.y: "loop1"},
        {sentinel.x: "xloop2", sentinel.y: "loop2"}
    ]
}

@patch("washr.parser.parse", return_value=ast_fixture)
def test_render(parse_mock):
    t = Template(sentinel.whatever)

    transformation = Mock(return_value="transformx")
    tntable = {sentinel.transform: transformation}
    
    with patch.dict("washr.template.transformation_table", tntable):
        res = t.render(context_fixture)

    transformation.assert_called_once_with("plainx")

    exp = "".join([
        "plainx",
        "transformx",
        "text"
        "xloop1",
        "loop1",
        "loop_text",
        "xloop2",
        "loop2",
        "loop_text"
    ])

    assert res == exp

    
    

    
    
    