import frontdoor
import os
import pathlib
import subprocess
import sys
import textwrap
import typing as t

REGISTRY = frontdoor.CommandRegistry("deps")
cmd = REGISTRY.decorate

from . import paths


@cmd("examples", "downloads existing open api specs")
def cmd_deps(args: t.List[str]) -> int:
    os.makedirs(paths.SPECS_PATH, exist_ok=True)
    print("Downloading example specs...")
    example_files = [
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/refs/heads/main/examples/v3.0/petstore.json",
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/refs/heads/main/examples/v3.0/petstore-expanded.json",
        "https://raw.githubusercontent.com/api-extraction-examples/existing-openapi-specs/refs/heads/main/django/django-4/intel-owl.yml",
    ]
    for url in example_files:
        subprocess.check_call(
            [
                "wget",
                url,
            ],
            cwd=paths.SPECS_PATH,
        )
    return 0


@cmd("openapi-generator", "Downloads the openapi-generator jar")
def cmd_openapi_generator(args: t.List[str]) -> int:
    print("Downloading openapi-generator-cli...")
    open_api_jar = paths.DEPS_PATH / "openapi-generator-cli.jar"

    subprocess.check_call(
        [
            "wget",
            "https://repo1.maven.org/maven2/org/openapitools/"
            "openapi-generator-cli/7.8.0/openapi-generator-cli-7.8.0.jar",
            "-O",
            str(open_api_jar),
        ],
        cwd=paths.DEPS_PATH,
    )

    print("creating openapi-generator-cli script...")
    open_api_jar = paths.DEPS_PATH / "openapi-generator-cli.jar"

    with open(paths.DEPS_PATH / paths.OPEN_API_CLI, "w") as file:
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
    os.chmod(paths.OPEN_API_CLI, 0o750)
    return 0
