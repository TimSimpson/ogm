import frontdoor
import os
import pathlib
import subprocess
import sys
import textwrap
import typing as t

REGISTRY = frontdoor.CommandRegistry("snet")
cmd = REGISTRY.decorate

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
ROOT_PATH = pathlib.Path(ROOT)
DEPS_PATH = ROOT_PATH / "deps"
SPECS_PATH = DEPS_PATH / "specs"
OPEN_API_CLI = DEPS_PATH / "openapi-generator"
OUTPUT_PATH = ROOT_PATH / "output"


def main() -> int:
    from . import root

    result = root.REGISTRY.dispatch(sys.argv[1:])
    sys.exit(result)
