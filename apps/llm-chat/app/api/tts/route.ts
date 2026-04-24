import { NextRequest, NextResponse } from 'next/server'
import { OpenAI } from 'openai'
import { MODELS, VOICES } from "../../constants/models"

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
})

export async function POST(req: NextRequest) {
  try {
    const { text } = await req.json()

    if (!text) {
      return NextResponse.json(
        { error: 'Text is required' },
        { status: 400 }
      )
    }

    const mp3 = await openai.audio.speech.create({
      model: MODELS.openai.tts,
      voice: VOICES.ballad,
      input: text,
      instructions: "Speak in a cheerful and positive tone.",
    })

    const buffer = Buffer.from(await mp3.arrayBuffer())

    return new NextResponse(buffer, {
      headers: {
        "Content-Type": 'audio/mpeg',
        'Content-Length': buffer.length.toString()
      }
    })


  } catch (error: unknown) {
    console.error('TTS error', error)
    const message = error instanceof Error ? error.message : 'Internal server error ???';
    return NextResponse.json({ error: message }, { status: 500 })
  }
}
