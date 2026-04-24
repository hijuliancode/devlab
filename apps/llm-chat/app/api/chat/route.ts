import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const openai = new OpenAI()

const SYSTEM_PROMPT = 
  'Eres atlas-GPT, un asistente útil. REGLA IMPORTANTE: Nunca generes imágenes en SVG, ASCII art, código de imagen, ni ningún otro formato visual basado en texto. Si el usuario pide una imagen, responde exactamente: "Para generar imgágenes, usa el botón de imagen (ícono 🖼️) en la esquina superior derecha. Ahí puedes describir lo que quieres y se generará con DALL-E 3 en formato PNG." No intentes dar alternativas ni workarounds para generar imágenes.';

type Provider = 'openai'

async function chatWithOpenAI(messages: Array<{ role: 'user' | 'assistant'; content: string }>) {

  const completion = await openai.chat.completions.create({
    model: 'gpt-5.4-nano',
    messages: [
      { role: 'system', content: SYSTEM_PROMPT },
      ...messages
    ]
  })

  console.log('AQUI VAMOS', completion.choices[0]?.message)

  return completion.choices[0]?.message
}

export async function POST(req: NextRequest) {
  console.log('REQ FROM POST', req)

  try {
    const { messages, provider = 'openai' } = await req.json()

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Message array is required' },
        { status: 400 }
      )
    }

    const selectProvider: Provider = provider

    const reply = await chatWithOpenAI(messages)

    return NextResponse.json({ message: reply })

  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : 'Internal server error';
    return NextResponse.json({ error: message}, { status: 500 })
  }
}