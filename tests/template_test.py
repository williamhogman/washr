from washr.template import Template, State

def test_state_get():
    state = State({"foo": "bar"})
    assert state.get("foo") == "bar"

def test_state_get_none_default():
    state = State({})
    assert state.get("foo") == None

def test_state_value_default():
    state = State({})
    assert state.get("bar", 1) == 1

def test_state_nested():
    inner_state = State({"foo": 10})
    state = State({}, inner_state)
    assert state.get("foo") == 10

def test_tri_nested_state():
    inner_inner_state = State({"foo": 10})
    inner_state = State({}, inner_inner_state)
    state = State({}, inner_state)

    assert state.get("foo") == 10
