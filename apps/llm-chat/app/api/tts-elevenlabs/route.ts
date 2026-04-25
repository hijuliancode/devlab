import { NextRequest, NextResponse } from 'next/server'
import { ElevenLabsClient } from '@elevenlabs/elevenlabs-js'

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY
})

const VOICE_ID = 'JBFqnCBsd6RMkjVDRZzb'

export async function POST(req: NextRequest) {
  try {
    const { text } = await req.json()
    console.log('POST req text', text)
    
    if (!text) {
      return NextResponse.json(
        { error: 'Text is required' },
        { status: 400 }
      )
    }

    const mp3 = await elevenlabs.textToSpeech.convert(VOICE_ID, {
      text,
      modelId: 'eleven_v3',
      outputFormat: 'mp3_44100_128'
    })

    return new NextResponse(mp3, {
      headers: {
        "Content-Type": 'audio/mpeg',
      }
    })

  } catch (error: unknown) {
    console.error('TTS error', error)
    const message = error instanceof Error ? error.message : 'Internal server error ???';
    return NextResponse.json({ error: message }, { status: 500 })
  }
}