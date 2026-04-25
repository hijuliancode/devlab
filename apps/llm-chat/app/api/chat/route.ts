import { NextRequest, NextResponse } from 'next/server'
import { MODELS } from '../../constants/models';
import OpenAI from 'openai'
import Anthropic from '@anthropic-ai/sdk';
import { GoogleGenAI } from '@google/genai';

const openai = new OpenAI()
const anthropic = new Anthropic()
const google = new GoogleGenAI({})

const SYSTEM_PROMPT = 
  'Eres atlas-GPT, un asistente útil. REGLA IMPORTANTE: Nunca generes imágenes en SVG, ASCII art, código de imagen, ni ningún otro formato visual basado en texto. Si el usuario pide una imagen, responde exactamente: "Para generar imgágenes, usa el botón de imagen (ícono 🖼️) en la esquina superior derecha. Ahí puedes describir lo que quieres y se generará con DALL-E 3 en formato PNG." No intentes dar alternativas ni workarounds para generar imágenes.';

type Provider = 'openai' | 'anthropic' | 'google'

type MessageType = {
  role: 'user' | 'assistant';
  content: string
}

async function chatWithOpenAI(messages: Array<MessageType>) {

  const completion = await openai.chat.completions.create({
    model: MODELS.openai.chat,
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      ...messages
    ]
  })

  return completion.choices[0]?.message
}

async function chatWithAnthropic(messages: MessageType[]) {
  // Anthropic expects only user/assistant roles with only role+content fields
  const cleanMessages = messages
    .filter((m) => m.role === 'user' || m.role === 'assistant')
    .map((m) => ({ role: m.role as 'user' | 'assistant', content: m.content }))

  // Anthropic requires messages to start with "user" and alternate roles
  // Merge consecutive same-role messages
  const mergedMessages: MessageType[] = []

  for (const msg of cleanMessages) {
    const last = mergedMessages[mergedMessages.length - 1]

    if (last && last.role === msg.role) {
      last.content += '\n' + msg.content
    } else {
      mergedMessages.push({ ...msg })
    }
  }

  // Ensure it starts with a user message
  const firstMergedMessage = mergedMessages[0]
  
  if (!firstMergedMessage || firstMergedMessage.role !== 'user') {
    throw new Error("Conversation must start with a user message");
  }

  const response = await anthropic.messages.create({
    model: 'claude-haiku-4-5',
    max_tokens: 450,
    system: SYSTEM_PROMPT,
    messages: mergedMessages
  })

  const textBlock = response.content.find((block) => block.type === 'text')

  return {
    role: 'assistant' as const,
    content: textBlock?.type === 'text' ? textBlock.text : '',
  }

}

async function chatWithGoogle(messages: MessageType[]) {
  console.log(messages)

  // CLan simple
  const cleanMessages = messages
    .filter((m) => (m.role === 'user' || m.role === 'assistant') && m.content?.trim())
    .map((m) => ({ role: m.role, content: m.content.trim() }))

  if (cleanMessages.length === 0 || cleanMessages[0]?.role !== 'user') {
    throw new Error('Conversation must start with a user message')
  }

  // Map to gemini format
  const contents = cleanMessages.map((m) => ({
    role: m.role === 'assistant' ? 'model' : 'user',
    parts: [{ text: m.content }]
  }))

  // Gemini call
  const response = await google.models.generateContent({
    model: 'gemini-2.5-flash',
    contents,
    config: {
      systemInstruction: SYSTEM_PROMPT
    }
  })

  // Extract text robustrly
  const text = 
    response.text ??
    response.candidates?.[0]?.content?.parts
      ?.map((p: { text?: string }) => p.text)
      .filter(Boolean)
      .join('\n') ?? ''


  return {
    role: 'assistant' as const,
    content: text,
  }
}

export async function POST(req: NextRequest) {

  try {
    const { messages, provider = 'openai' } = await req.json()

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json(
        { error: 'A non-empty message array is required' },
        { status: 400 }
      )
    }

    const selectProvider: Provider = 
      provider === 'anthropic' ? 'anthropic' :
      provider === 'google' ? 'google' :
      'openai';

    let reply =
      selectProvider === 'anthropic' ? await chatWithAnthropic(messages) :
      selectProvider === 'google' ? await chatWithGoogle(messages) : 
      await chatWithOpenAI(messages);

    return NextResponse.json({ message: reply })

  } catch (error: unknown) {
    if (error instanceof Error && error.message === 'Conversation must start with a user message') {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }

    const message = error instanceof Error ? error.message : 'Internal server error';
    return NextResponse.json({ error: message}, { status: 500 })
  }
}