"""Module implementing the Variable transformations"""

import cgi
import json

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

def plaintext(value):
    return cgi.escape(value, True)

def javascript(value):
    return json.dumps(value)

def javascript_plaintext(value):
    return javascript(plaintext(value))

def url(value):
    return urlencode(value)

def rgb(value):
    assert value[0] == "#"
    fmt = "rgb({0},{1},{2})"

    # Three hex digits
    if len(value) == 4:
        vals = (int(digit+digit, 16) for digit in value[1:])
        return fmt.format(*vals)
    elif len(value) == 7:
        # two hex digits each
        parts = (value[1:3], value[3:5], value[5:7])
        vals = (int(part, 16) for part in parts)
        return fmt.format(*vals)
    else:
        raise RuntimeError("wrong format")

transformation_table = {
    "Plaintext": plaintext,
    "JS": javascript,
    "JSPlaintext": javascript_plaintext,
    "URLEncoded": url,
    "RGB": rgb
}
