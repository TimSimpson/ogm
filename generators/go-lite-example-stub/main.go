package golite_ex

import (
	"context"
	"fmt"
	djangoCrm "golite_ex/djangoCrm"
	petstore "golite_ex/petstore"
	"os"
)

func main() {
	core := NewHttpClient("https://localhost")
	psClient := petstore.NewDefaultAPI(core)
	ctx := context.Background()
	pet, err := psClient.FindPetById(ctx, 123)

	if err != nil {
		fmt.Errorf("Got error retrieving pet: %w", err)
		os.Exit(1)
	}
	fmt.Printf("Got pet: %s", pet)

	djangoCrmClient := djangoCrm.NewCasesAPI(core)
	fmt.Printf("just doing this to avoid the unused var error: %s", djangoCrmClient)
}
