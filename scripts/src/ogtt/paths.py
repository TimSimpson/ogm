import os
import pathlib
import typing as t

_ROOT_STR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
ROOT = pathlib.Path(_ROOT_STR)
DEPS = ROOT / "../deps"
GENERATORS = ROOT / "../generators"
SPECS = DEPS / "../specs"
OPEN_API_CLI = DEPS / "openapi-generator"
OUTPUT = ROOT / "../output"
