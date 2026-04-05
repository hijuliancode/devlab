import { openAiClient } from "./clients/index.js";

type LLMName = "openai";

type ClientOptions = {
  apiKey: string;
};

export function createClient(provider: LLMName, options: ClientOptions) {
  if (!options.apiKey) {
    throw new Error("API key is required");
  }

  switch (provider) {
    case "openai":
      return openAiClient(options.apiKey);

    default:
      throw new Error(`Unsupported LLM: ${provider}`);
  }
}
