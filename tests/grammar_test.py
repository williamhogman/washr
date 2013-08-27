import pytest

from washr.parser import grammar, types

var_foo = types.Variable("foo", None)
var_bar = types.Variable("bar", None)

block_baz = types.BlockStart("baz")
block_end_baz = types.BlockEnd("baz")

parser_fixtures = {
    "Normal string": ("foo", ["foo"]),
    "String with {": ("{foo", ["{foo"]),
    "Empty {} is not a var": ("{}", ["{}"]),
    "Lone {": ("{", ["{"]),
    "Lone }": ("}", ["}"]),
    "block: by itself": ("block:", ["block:"]),
    "Lone :": (":", [":"]),
    "Variable foo": ("{foo}", [var_foo]),
    "Double wrapped in {}": ("{{foo}}", ["{", var_foo, "}"]),
    "Asymmetric double wrapping": ("{{foo}", ["{", var_foo]),
    "2 vars": ("{foo}{bar}", [var_foo, var_bar]),
    "Open block": ("{block:baz}", [block_baz]),
    "End block": ("{/block:baz}", [block_end_baz]),
    "Inconsistent caps block": ("{bLocK:baz}", [block_baz]),
    "Inconsistent caps block end": ("{/bLocK:baz}", [block_end_baz]),
    "complete block": ("{block:baz}{/block:baz}", [block_baz, block_end_baz]),
}

parser_f_ids = parser_fixtures.keys()


@pytest.mark.parametrize(("inp", "exp"), parser_fixtures.values(), ids=parser_f_ids)
def test_grammar_quirks(inp, exp):
    res = grammar.parse(inp)
    assert len(res) == len(exp)
    for res_part, exp_part in zip(res, exp):
        assert res_part == exp_part
