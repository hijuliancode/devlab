import { Anthropic } from '@anthropic-ai/sdk/client.js';
import dotenv from 'dotenv'
dotenv.config({ path: "../../../.env.local", quiet: true });

const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })

async function main() {
  const msg = await anthropic.messages.create({
    model: 'claude-haiku-4-5',
    max_tokens: 200,
    messages: [
      {
        "role": "user",
        "content": "Cual es la capital de Colombia?",
      }
    ]
  })

  const block = msg.content[0].text

  console.log(block)
}

main().catch(console.error)