from __future__ import print_function
from washr.template import Template
from washr import server
import sys

if len(sys.argv) < 4:
    print("Usage:", sys.argv[0], "<template_path> <api_key> <hostname>")
    sys.exit(0)
with open(sys.argv[1]) as f:
    template = Template(f.read())
server.setup(
    sys.argv[2],
    sys.argv[3],
    template
)
server.app.run(port=8000)
