import { ElevenLabsClient, play } from "@elevenlabs/elevenlabs-js";
import { Readable } from "stream";
import dotenv from 'dotenv'

dotenv.config({ path: '../../../.env.local', quiet: true })

const elevenlabs = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY
})

const audio = await elevenlabs.textToSpeech.convert('JBFqnCBsd6RMkjVDRZzb', {
  text: 'Hola, bienvenida a Softwaredeportivo, soy Elev, tu asistente de entrenamiento personal. Estoy aquí para ayudarte a alcanzar los objetivos de tu club o escuela deportiva y llevarla al siguiente nivel. ¿En qué puedo ayudarte hoy?',
  modelId: 'eleven_v3',
  outputFormat: 'mp3_44100_128',
})

const reader = audio.getReader()
const stream = new Readable({
  async read() {
    const { done, value } = await reader.read()
    if (done) {
      this.push(null)
    } else {
      this.push(value)
    }
  }
})

await play(stream)