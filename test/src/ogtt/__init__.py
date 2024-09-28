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


@cmd("deps", "downloads latest dependencies")
def cmd_deps(args: t.List[str]) -> int:
    os.makedirs(SPECS_PATH, exist_ok=True)
    example_files = [
        "petstore.json",
        "petstore-expanded.json"
    ]
    for file_name in example_files:
        subprocess.check_call(
            [
                "wget",
                f"https://raw.githubusercontent.com/OAI/OpenAPI-Specification/refs/heads/main/examples/v3.0/{file_name}",
            ],
            cwd=SPECS_PATH,
        )

    open_api_jar = DEPS_PATH / "openapi-generator-cli.jar"

    subprocess.check_call(
        [
            "wget",
            "https://repo1.maven.org/maven2/org/openapitools/"
            "openapi-generator-cli/7.8.0/openapi-generator-cli-7.8.0.jar",
            "-O",
            str(open_api_jar),
        ],
        cwd=DEPS_PATH,
    )

    open_api_jar = DEPS_PATH / "openapi-generator-cli.jar"

    with open(DEPS_PATH / OPEN_API_CLI, "w") as file:
        file.write(
            textwrap.dedent(
                f"""
            #!/usr/bin/env bash
            java -ea \\
                ${{JAVA_OPTS}} \\
                -Xms512M \\
                -Xmx1024M \\
                -server \\
                -jar '{open_api_jar}' \\
                "${{@}}"
            """
            )
        )
    os.chmod(OPEN_API_CLI, 0o750)


@cmd("gen", "generate examples")
def cmd_gen(args: t.List[str]) -> int:
    if not DEPS_PATH.exists():
        raise RuntimeError("Run `deps` first.")

    os.makedirs(OUTPUT_PATH, exist_ok=True)

    #  ../deps/openapi-generator generate -g go  -o go --input-spec-root-directory ../deps/specs/  -t ../../templates/go
    subprocess.check_call(
        [
            OPEN_API_CLI,
            "generate"
        ],
        cwd=OUTPUT_PATH,
    )



def main() -> int:
    result = REGISTRY.dispatch(sys.argv[1:])
    sys.exit(result)
