"""
Module for reading the tumblr meta tags.
"""
import html5lib

__all__ = ("parse_variables", "default_values")

# The following are meta prefixes, everything else is irrelevant
meta_prefixes = [
    'color',
    'image',
    'font',
    'text',
    'if',
    'select'
]

# Appearently we need to namespace this...
meta_tag = "{http://www.w3.org/1999/xhtml}meta"


# Returns an iterator consisting of two tuples (name, value)
def _read_for_metas(root):
    # Iterate over all meta tags
    for el in root.iter(meta_tag):
        if "name" in el.attrib and "value" in el.attrib:
            yield (el.attrib["name"], el.attrib["value"])


def _read_metas(src):
    document = html5lib.parse(src)
    return _read_for_metas(document)


# Parses the name of a meta tag according to the tumblr format
def _parse_name(name):
    sep = name.find(":")

    # Unparseable
    if sep == -1:
        return None

    prefix = name[:sep]
    suffix = name[sep + 1:]

    # Invalid name
    if prefix not in meta_prefixes:
        return None

    return prefix, suffix


def _expand_metas(metas):
    """Turns the (name, value) tuples into (type, name, value) tuples"""
    for name, value in metas:
        pname = _parse_name(name)
        if pname is not None:
            yield pname + (value,)


def parse_variables(src):
    """Parse a document for tumblr meta tags

    Parses the meta an html document for meta tags returning a dict
    with variable names, type and values
    """
    metas = _expand_metas(_read_metas(src))

    res = {}

    sels = []

    for (t, n, v) in metas:
        if t == "select":
            sels.append((n, v))
            old_t, old_v = res.get(n, (None, None))
            if isinstance(old_v, list):
                old_v.append(v)
            else:
                res[n] = (t, [v])
        else:
            res[n] = (t, v)
    return res


def default_values(variables):
    """Takes a variables structure and creates a dict with name -> defaultvalue

    This is useful for rendering template with default.
    """
    res = {}
    for k, (t, v) in variables.items():

        if t == "select":
            res[k] = v[0]
        else:
            res[k] = v
    return res


if __name__ == '__main__':
    test = """
    <meta name='color:foo' value='derp' />
    <meta name='select:cat' value='tabby'>
    <meta name='select:cat' value='black'>
    """
    res = parse_variables(test)
    print(res)

    print(default_values(res))
