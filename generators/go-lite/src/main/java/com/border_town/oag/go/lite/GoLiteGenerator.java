package com.border_town.oag.go.lite;

import org.openapitools.codegen.*;
import org.openapitools.codegen.model.*;
import io.swagger.models.properties.*;

import java.util.*;
import java.io.File;

public class GoLiteGenerator extends org.openapitools.codegen.languages.GoClientCodegen {
  // public class GoLiteGenerator extends DefaultCodegen implements CodegenConfig
  // {

  // source folder where to write the files
  protected String sourceFolder = "src";
  protected String apiVersion = "1.0.0";

  /**
   * Configures the type of generator.
   *
   * @return the CodegenType for this generator
   * @see org.openapitools.codegen.CodegenType
   */
  public CodegenType getTag() {
    return CodegenType.CLIENT;
  }

  /**
   * Configures a friendly name for the generator. This will be used by the
   * generator
   * to select the library with the -g flag.
   *
   * @return the friendly name for the generator
   */
  public String getName() {
    return "go-lite";
  }

  /**
   * Provides an opportunity to inspect and modify operation data before the code
   * is generated.
   */
  @Override
  public OperationsMap postProcessOperationsWithModels(OperationsMap objs, List<ModelMap> allModels) {

    // to try debugging your code generator:
    // set a break point on the next line.
    // then debug the JUnit test called LaunchGeneratorInDebugger

    OperationsMap results = super.postProcessOperationsWithModels(objs, allModels);

    OperationMap ops = results.getOperations();
    List<CodegenOperation> opList = ops.getOperation();

    // iterate over the operation and perhaps modify something
    for (CodegenOperation co : opList) {
      // example:
      // co.httpMethod = co.httpMethod.toLowerCase();
    }

    return results;
  }

  /**
   * Returns human-friendly help for the generator. Provide the consumer with help
   * tips, parameters here
   *
   * @return A string value for the help message
   */
  public String getHelp() {
    return "Modifies the standard Go client generator to generate less code. May lack features you need and requires more hand-written code. YMMV";
  }

  public GoLiteGenerator() {
    super();

    this.apiDocTemplateFiles.clear();
    this.apiTestTemplateFiles.clear();
    this.modelDocTemplateFiles.clear();
    this.modelTestTemplateFiles.clear();

    // set the output folder here
    outputFolder = "generated-code/go-lite";

    /**
     * Models. You can write model files using the modelTemplateFiles map.
     * if you want to create one template for file, you can do so here.
     * for multiple files for model, just put another entry in the
     * `modelTemplateFiles` with
     * a different extension
     */
    modelTemplateFiles.put(
        "model.mustache", // the template to use
        ".go"); // the extension for each file to write

    /**
     * Api classes. You can write classes for each Api file with the
     * apiTemplateFiles map.
     * as with models, add multiple entries with different extensions for multiple
     * files per
     * class
     */
    apiTemplateFiles.put(
        "api.mustache", // the template to use
        ".go"); // the extension for each file to write

    /**
     * Template Location. This is the location which templates will be read from.
     * The generator
     * will use the resource stream to attempt to read the templates.
     */
    templateDir = "go-lite";

    /**
     * Api Package. Optional, if needed, this can be used in templates
     */
    apiPackage = "org.openapitools.api";

    /**
     * Model Package. Optional, if needed, this can be used in templates
     */
    modelPackage = "org.openapitools.model";

    /**
     * Reserved words. Override this with reserved words specific to your language
     */
    reservedWords = new HashSet<String>(
        Arrays.asList(
            "type", // replace with static values
            "struct",
            "go",
            "package"));

    /**
     * Additional Properties. These values can be passed to the templates and
     * are available in models, apis, and supporting files
     */
    additionalProperties.put("apiVersion", apiVersion);

    if (!additionalProperties.containsKey("coreClientTypeName")) {
      additionalProperties.put("coreClientTypeName", "Client");
    }

    // if (!additionalProperties.containsKey("coreClientTypeNamePackage")) {
    // additionalProperties.put("coreClientTypeNamePackage", "");
    // }

    // additionalProperties.put("coreClientPackage", "");
    // /**
    // * Language Specific Primitives. These types will not trigger imports by
    // * the client generator
    // */
    // languageSpecificPrimitives = new HashSet<String>(
    // Arrays.asList(
    // "string", // replace these with your types
    // "Type2"));
  }

  @Override
  public void processOpts() {
    super.processOpts();
    this.supportingFiles.clear();

    final Object value = this.additionalProperties.get("coreClientTypeNamePackage");
    if (value == null || ((value instanceof String) && ((String) value) == "")) {
      this.supportingFiles.add(new SupportingFile("client.mustache", "", "client.go"));
    }
  }

  /**
   * Escapes a reserved word as defined in the `reservedWords` array. Handle
   * escaping
   * those terms here. This logic is only called if a variable matches the
   * reserved words
   *
   * @return the escaped term
   */
  @Override
  public String escapeReservedWord(String name) {
    return "_" + name; // add an underscore to the name
  }

  /**
   * Location to write model files. You can use the modelPackage() as defined when
   * the class is
   * instantiated
   */
  public String modelFileFolder() {
    return outputFolder;
  }

  /**
   * Location to write api files. You can use the apiPackage() as defined when the
   * class is
   * instantiated
   */
  @Override
  public String apiFileFolder() {
    return outputFolder;
  }

  /**
   * override with any special text escaping logic to handle unsafe
   * characters so as to avoid code injection
   *
   * @param input String to be cleaned up
   * @return string with unsafe characters removed or escaped
   */
  @Override
  public String escapeUnsafeCharacters(String input) {
    // TODO: check that this logic is safe to escape unsafe characters to avoid code
    // injection
    return input;
  }

  /**
   * Escape single and/or double quote to avoid code injection
   *
   * @param input String to be cleaned up
   * @return string with quotation mark removed or escaped
   */
  public String escapeQuotationMark(String input) {
    // TODO: check that this logic is safe to escape quotation mark to avoid code
    // injection
    return input.replace("\"", "\\\"");
  }
}
