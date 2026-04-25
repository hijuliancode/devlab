import { NextRequest, NextResponse } from 'next/server'
import { MODELS } from '../../constants/models';

import { generateText } from 'ai'
import { openai } from '@ai-sdk/openai'
import { anthropic } from '@ai-sdk/anthropic'
import { google } from '@ai-sdk/google'

const SYSTEM_PROMPT = 
  'Eres atlas-GPT, un asistente útil. REGLA IMPORTANTE: Nunca generes imágenes en SVG, ASCII art, código de imagen, ni ningún otro formato visual basado en texto. Si el usuario pide una imagen, responde exactamente: "Para generar imgágenes, usa el botón de imagen (ícono 🖼️) en la esquina superior derecha. Ahí puedes describir lo que quieres y se generará con DALL-E 3 en formato PNG." No intentes dar alternativas ni workarounds para generar imágenes.';

type Provider = 'openai' | 'anthropic' | 'google'

const models = {
  openai: openai(MODELS.openai.chat),
  anthropic: anthropic('claude-haiku-4-5'),
  google: google('gemini-2.5-flash')
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

    // Vercel AI SDK's generateText function abstracts away provider-specific details, 
    // allowing you to use a consistent interface for generating text across different AI providers.
    
    const { text } = await generateText({
      model: models[selectProvider],
      system: SYSTEM_PROMPT,
      messages,
    })

    return NextResponse.json({
      message: {
        role: 'assistant',
        content: text
      }
    })

  } catch (error: unknown) {
    if (error instanceof Error && error.message === 'Conversation must start with a user message') {
      return NextResponse.json({ error: error.message }, { status: 400 })
    }

    const message = error instanceof Error ? error.message : 'Internal server error';
    return NextResponse.json({ error: message}, { status: 500 })
  }

}