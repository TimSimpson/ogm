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


@cmd("go-lite", "builds a project with go-lite to test it")
def cmd_gen(args: t.List[str]) -> int:
    output = paths.OUTPUT / "go-lite"
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(paths.GENERATORS / "go-lite-example-stub", output)

    for (pkg_name, spec) in [
        ("petstore", "petstore-expanded.json"),
        ("djangoCrm", "django-crm.yml"),
    ]:
        subprocess.check_output(
            _exec_args(
                [
                    "generate",
                    "-g",
                    "go-lite",
                    # see https://github.com/OpenAPITools/openapi-generator/issues/535
                    "--additional-properties=enumClassPrefix=true",
                    "-o",
                    str(paths.OUTPUT / "go-lite" / pkg_name),
                    "--package-name",
                    pkg_name,
                    "--input-spec",
                    str(paths.SPECS / spec),
                ]
            )
        )

    subprocess.check_call(
        ["goimports", "-w", "."], cwd=output
    )
    subprocess.check_call(
        ["go", "mod", "tidy"], cwd=output
    )
    return subprocess.call(
        ["go", "build"],
        cwd=output,
    )
