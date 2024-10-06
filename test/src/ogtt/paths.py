import os
import pathlib
import typing as t

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
ROOT_PATH = pathlib.Path(ROOT)
DEPS_PATH = ROOT_PATH / "deps"
GENERATORS_PATH = ROOT_PATH / "../generators"
SPECS_PATH = DEPS_PATH / "specs"
OPEN_API_CLI = DEPS_PATH / "openapi-generator"
OUTPUT_PATH = ROOT_PATH / "output"
