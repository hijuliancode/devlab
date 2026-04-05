import OpenAI from "openai"

export const openAiClient = (apiKey: string): OpenAI => {
  return new OpenAI({ apiKey });
}
