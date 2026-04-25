
import { generateText } from 'ai'

import { openai } from '@ai-sdk/openai'
import { anthropic} from '@ai-sdk/anthropic'
import { google } from '@ai-sdk/google'
import dotenv from "dotenv";

dotenv.config({ path: "../../../.env.local", quiet: true });

const { text } = await generateText({
  model: openai('gpt-5.4-nano'),
  // model: anthropic('claude-haiku-4-5'),
  // model: google('gemini-2.5-flash'),
  prompt: 'Hi, who are you?'
})

console.log('>>>', text)