import { Anthropic } from '@anthropic-ai/sdk'
import dotenv from 'dotenv'

dotenv.config({ path: '../../../.env.local', quiet: true })

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
})

async function main() {
  console.log('Iniciando stream...\n')

  const stream = await anthropic.messages.stream({
    model: 'claude-haiku-4-5',
    max_tokens: 1000,
    messages: [
      {
        role: 'user',
        content: 'Cual es la capital de Colombia'
      },
      {
        role: 'user',
        content: '¿Y cual es el color de su bandera?'
      }
    ]
  })

  let tokensAproximados = 0

  for await (const event of stream) {
    if (event.type === 'message_start') {
      console.log('[evento] message_start')
    }

    if (
      event.type === 'content_block_delta' &&
      event.delta.type === 'text_delta'
    ) {
      process.stdout.write(event.delta.text)
      tokensAproximados += 1
    }

    if (event.type === 'message_stop') {
      console.log('\n\n[evento] message_stop')
    }
  }

  console.log('Stream finalizado.')
  console.log(`Fragmentos de texto recibidos: ${tokensAproximados}`)
}

main().catch((err) => {
  console.error('Error en stream:', err)
})