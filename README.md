# OpenSeesParser (OpsParser)

[![Documentation Status](https://readthedocs.org/projects/opsparser/badge/?version=latest)](https://opsparser.readthedocs.io/en/latest/index.html)
[![PyPI version](https://badge.fury.io/py/opsparser.svg)](https://badge.fury.io/py/opsparser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/opsparser)](https://pepy.tech/project/opsparser)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/yourusername/opsparser/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](https://makeapullrequest.com)

OpenSeesParser (OpsParser) is a practical utility library designed for OpenSeesPy users, providing a series of convenient functions and tools to help users build and analyze structural models more efficiently.

## Features

- Simplifies the creation and management of OpenSeesPy models

## Installation

```bash
pip install opsparser
```

## Quick Start

```python
import openseespy.opensees as ops
from opsparser import OpenSeesParser

# first hook all commands before your opensees code
parser = OpenSeesParser(ops)
parser.hook_all(debug = False) # Set debug = True to show parsing process

# your OpenSeesPy Code
# ...

# get your model's info
from opsparser import OpenSeesCommand as Command
# Node
Node = Command.NODE.instance
node_dict = Node.nodes  # node info

# Materials
Material = Command.MATERIAL.instance
material_dict = Material.materials  # material info

# Elements
Element = Command.ELEMENT.instance
Element_dict = Element.Elements  # Elements info

# and many convient tools
# like you can use newtag property for Node, Element, Material to get a unused tag
Node.newtag
Element.newtag
Material.newtag

# maybe 5 more continuous tags? Using `get_new_tags(start = 1)`
Node.get_new_tags(5)

```

## Examples

Check out the [examples documentation](https://opsparser.readthedocs.io/en/latest/examples.html) for more usage examples, including modeling and analysis of bridges, frames, and other structures.

## Documentation

Complete documentation is available at [OpsParser Documentation](https://opsparser.readthedocs.io/en/latest/index.html), including:

- [Installation Guide](https://opsparser.readthedocs.io/en/latest/installation.html)
- [Quick Start Guide](https://opsparser.readthedocs.io/en/latest/quick_start.html)
- [API Reference](https://opsparser.readthedocs.io/en/latest/api.html)
- [Known Issues](https://opsparser.readthedocs.io/en/latest/known_issues.html)

## Contributing

Contributions to the OpsParser project are welcome! Please participate through:

1. Submitting issues and feature requests
2. Contributing code improvements
3. Sharing your experiences and examples using OpsParser

## License

OpsParser is released under the MIT License.
