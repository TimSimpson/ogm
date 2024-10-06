package golite_ex

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

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
	if response.StatusCode < 200 || response.StatusCode >= 300 {
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
