_default:
    @just --list

hi:
    echo hi

build:
    cd generators/go-lite && mvn package
    # java -cp generators/go-lite/generators/my-codegen/target/my-codegen-openapi-generator-1.0.0.jar:modules/openapi-generator-cli/target/openapi-generator-cli.jar org.openapitools.codegen.OpenAPIGenerator

exec args:
    java -cp generators/go-lite/target/go-lite-openapi-generator-1.0.0.jar:test/deps/openapi-generator-cli.jar org.openapitools.codegen.OpenAPIGenerator {{args}}

gen:
    java -cp generators/go-lite/target/go-lite-openapi-generator-1.0.0.jar:test/deps/openapi-generator-cli.jar org.openapitools.codegen.OpenAPIGenerator generate -g go-lite -o test/output/go/petstore --input-spec test/deps/specs/petstore-expanded.json --package-name petstore

_meta:
    cd test/output && ../deps/openapi-generator meta -o ../../generators/go-lite -n go-lite -p com.border-town.oag.go.lite

_old_temp1:
    cd test/output && ../deps/openapi-generator meta -o ../../generators/go-lite -n go-lite -p com.border-town.oag.go.lite

_old_temp2:
    ../deps/openapi-generator generate -g go  -o go --input-spec-root-directory ../deps/specs/  -c ../../generators/go-client-lite/config.yaml -t ../../generators/go-client-lite/templates