import frontdoor
import subprocess
import typing as t

from . import paths

REGISTRY = frontdoor.CommandRegistry("build")
cmd = REGISTRY.decorate


@cmd("go-lite", "builds go lite generator")
def cmd_gen(args: t.List[str]) -> int:
    subprocess.check_call(
        [
            "mvn",
            "package",
        ],
        cwd=paths.GENERATORS / "go-lite",
    )
    return 0
