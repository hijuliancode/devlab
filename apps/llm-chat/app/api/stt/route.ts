import { NextRequest, NextResponse } from 'next/server'
 import { OpenAI } from 'openai'
import { MODELS } from '../../constants/models'

 const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
 })

 export async function POST(req: NextRequest) {
  try {

    const formData = await req.formData()
    const audioFile = formData.get('audio') as File

    if (!audioFile) {
      return NextResponse.json(
        { error: 'Audio file is required' },
        { status: 400 }
      )
    }

    const transcription = await openai.audio.transcriptions.create({
      model: MODELS.openai.audio,
      file: audioFile
    })

    return NextResponse.json({ text: transcription.text })

  } catch (error: unknown) {
    console.error('SST error', error)

    const message = error instanceof Error ? error.message : 'Internal server error'

    return NextResponse.json({ error: message }, { status: 500 })

  }
 }