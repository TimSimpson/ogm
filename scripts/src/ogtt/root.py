import frontdoor
import os
import pathlib
import subprocess
import sys
import textwrap
import typing as t

REGISTRY = frontdoor.CommandRegistry("ogtt")
cmd = REGISTRY.decorate

ROOT = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")
ROOT_PATH = pathlib.Path(ROOT)
DEPS_PATH = ROOT_PATH / "deps"
SPECS_PATH = DEPS_PATH / "specs"
OPEN_API_CLI = DEPS_PATH / "openapi-generator"
OUTPUT_PATH = ROOT_PATH / "output"


@cmd("build", "builds generators")
def cmd_build(args: t.List[str]) -> int:
    from . import build

    return build.REGISTRY.dispatch(args)


@cmd("deps", "downloads latest dependencies")
def cmd_deps(args: t.List[str]) -> int:
    from . import deps

    return deps.REGISTRY.dispatch(args)


@cmd("gen", "generate examples")
def cmd_gen(args: t.List[str]) -> int:
    from . import gen

    return gen.REGISTRY.dispatch(args)
