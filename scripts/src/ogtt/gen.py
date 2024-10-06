import frontdoor
import shutil
import subprocess
import typing as t

from . import paths

REGISTRY = frontdoor.CommandRegistry("build")
cmd = REGISTRY.decorate


def _exec_args(args: t.List[str]) -> t.List[str]:
    go_lite_jar = (
        paths.GENERATORS / "go-lite/target/go-lite-openapi-generator-1.0.0.jar"
    )
    cli_jar = paths.DEPS / "openapi-generator-cli.jar"
    return [
        "java",
        "-cp",
        f"{go_lite_jar}:{cli_jar}",
        "org.openapitools.codegen.OpenAPIGenerator",
    ] + args


@cmd("petstore", "builds the petstore example")
def cmd_gen(args: t.List[str]) -> int:
    output = paths.OUTPUT / "go/petstore"
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(paths.GENERATORS / "go-lite-example-stub", output)

    subprocess.check_output(
        _exec_args(
            [
                "generate",
                "-g",
                "go-lite",
                "-o",
                str(paths.OUTPUT / "go/petstore/generated"),
                "--package-name",
                "petstore",
                "--input-spec",
                str(paths.SPECS / "petstore-expanded.json"),
            ]
        )
    )

    return subprocess.call(
        ["go", "build"],
        cwd=output,
    )
