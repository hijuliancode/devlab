import { NextRequest, NextResponse } from "next/server";
import OpenAi from 'openai';
import { MODELS } from "../../constants/models";

const openai = new OpenAi({
  apiKey: process.env.OPENAI_API_KEY
})

export async function POST(req: NextRequest) {
  try {
    const { prompt, size = '1024x1024' } = await req.json()

    if (!prompt) {
      return NextResponse.json(
        { error: 'Prompt is required' },
        { status: 400 }
      )
    }

    const response = await openai.images.generate({
      model: MODELS.openai.images,
      prompt,
      n: 1,
      size: size as "1024x1024" | "1792x1024" | "1024x1792",
      response_format: 'b64_json'
    })

    const imageData = response.data?.[0]
    const b64 = imageData?.b64_json

    if( !b64 ) {
      return NextResponse.json(
        { error: 'No image data returned' },
        { status: 500 }
      )
    }

    return NextResponse.json({
      image: {
        b64,
        mimeType: 'image/png',
        revisedPrompt: imageData.revised_prompt ?? null
      },
    });

  } catch (err) {
    console.error('Image generation error:', err)  
    const message = err instanceof Error ? err.message : 'Internal Server Error'

    return NextResponse.json({ error: message }, { status: 500 });
  }
}