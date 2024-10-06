# OpenAPI Generator Templates

This repo contains some opionated Client templates for the Open API generator project.

## Clients

### Go Client "Lite"

Generates Go clients but without as much code as the official clients.
Only supports JSON and many features may be missing. However the result is simple and close to what a hand generated client may have looked like.

In particular, this generator works by creating functions for all operations. It then requires a "core client" type to be passed in. This is expected to have the following interface:

```go
type Client interface {
	SendRequest(ctx context.Context, method, relativeUrl string, hasBody bool, body interface{}, hasReturnValue bool, returnValue interface{}) error
}
```

You can then implement this yourself relatively simply, and the generated code will handle creating type rich pairings with the Open API functions.

Doing this allows you to insert all sorts of behavior into the client. For instance you could write a function to log the request URL, method, body etc. Or save the last response body to variable as a variable to check in integration tests. You can embed auth headers, or handle reauthentication. Etc. etc.

The existing API generator creates a lot of code to try do these things for you, but I often felt the generated code was in my way. By making the relatively simple interface above the responsibility of non-generated code, it's possible to do these things.

Second, this generator will create interfaces of the API which have methods for each operation, and finally a single implementation of this interface which accepts a "core client" so you don't have to pass the core client to global functions all the time. This also lets you use the interface and create mocks of it for situations where you don't want to test your API.

Finally, if you're generating multiple API specs but want to share the core client interface by defining that yourself, you can pass the following additional properties like so:

```
--additional-properties=coreClientTypeName=core.Client
--additional-properties=coreClientTypeNamePackage=github.com/TimSimpson/SomeThing/core
```

in the example above generated code would import `github.com/TimSimpson/SomeThing/core` and use the type `core.Client` instead of `Client` everywhere.

BTW, here is an rudimentary example of a "core" client:

```go

type HttpClient struct {
	baseUrl string
}

func NewHttpClient(baseUrl string) *HttpClient {
	return &HttpClient{
		baseUrl: baseUrl,
	}
}

func (self *HttpClient) SendRequest(ctx context.Context, method, relativeUrl string, hasBody bool, body interface{}, hasReturnValue bool, returnValue interface{}) error {
	var url string
	if strings.HasPrefix(relativeUrl, "/") {
		url = fmt.Sprintf("%s%s", self.baseUrl, relativeUrl)
	} else {
		url = fmt.Sprintf("%s/%s", self.baseUrl, relativeUrl)
	}
	bodyBytes, err := json.Marshal(body)
	if err != nil {
		return fmt.Errorf("error formating request body: %w", err)
	}
	var bodyReader io.Reader
	if hasBody {
		bodyReader = bytes.NewReader(bodyBytes)
	} else {
		bodyReader = nil
	}
	request, err := http.NewRequestWithContext(ctx, method, url, bodyReader)

	if err != nil {
		return fmt.Errorf("error constructing request: %w", err)
	}

	request.Header.Add("Authorization", "Bearer <JWT-go-here>")

	response, err := http.DefaultClient.Do(request)
	if err != nil {
		return fmt.Errorf("error executing request: %w", err)
	}
	if response.StatusCode< 200 || response.StatusCode >= 300 {
		// of course this code could parse the body for failure information
		return fmt.Errorf("bad status code! %d", response.StatusCode)
	}
    // TODO: handle authentication failures by re-authenticating and repeatng
    //       the request, if desired

	if hasReturnValue {
		responseBody, err := io.ReadAll(response.Body)
		if err != nil {
			return fmt.Errorf("error reading response body: %w", err)
		}

		err = json.Unmarshal(responseBody, returnValue)
		if err != nil {
			return fmt.Errorf("error unmarshalling response body: %w", err)
		}
	}

	return nil
}

```


## Building

This uses Python instead of shell scripts to build and test everything.

I recommend installing rye and doing this:

```bash
pushd scripts
rye sync
source .venv/bin/activate
popd # not strictly necessary
ogtt deps
ogtt build
ogtt gen go-lite
```

## Notes

Primary tutorial on customization
https://openapi-generator.tech/docs/customization/

Go codegen:
https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/java/org/openapitools/codegen/languages/GoClientCodegen.java

Go client templates:

https://github.com/OpenAPITools/openapi-generator/blob/master/modules/openapi-generator/src/main/resources/go/api.mustache