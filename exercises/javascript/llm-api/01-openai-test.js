import dotenv from "dotenv";
dotenv.config({ path: "../../../.env.local", quiet: true });

import { createClient } from "@devlab/ai-client";

const client = createClient("openai", {
  apiKey: process.env.OPENAI_API_KEY,
});

// client.responses is the main entry point for generating responses from the model. It provides a create method that accepts an object with the following properties:
// - model: The name of the model to use for generating the response. In this case, we are using "gpt-5.4-nano".
// - input: The input text that you want the model to generate a response for. In this case, we are asking the model to write a haiku about the ocean in a maximum of 60 characters.
// - max_output_tokens: The maximum number of tokens that the model should generate in the response. In this case, we are setting it to 60.
// The create method returns a promise that resolves to an object containing the generated response. The generated text can be accessed through the output_text property of the response object.

// const response = await client.responses.create({
//   model: "gpt-5.4-nano",
//   input: "Escribe un haiku sobre el océano en maximo 60 caracteres",
//   max_output_tokens: 60,
// })

// console.log(response.output_text);

/* 
  Streaming responses is also supported.
  Instead of waiting for the entire response to be generated,
  you can receive the response in chunks as it is being generated.
  This can be done by using the createStream method instead of create.
  The createStream method returns an async iterable that you can iterate over to receive the response chunks as they are generated.
*/

const stream = await client.responses.create({
  model: "gpt-5.4-nano",
  input: "Escribe un cuento sobre la luna en maximo 260 caracteres",
  stream: true,
})

for await (const event of stream) {
  if (event.type === "response.output_text.delta") {
    process.stdout.write(event.delta)
  }
}

console.log();