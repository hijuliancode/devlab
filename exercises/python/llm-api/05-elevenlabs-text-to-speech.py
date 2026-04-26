from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key = os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
  # text = "Hello, this is a test of the ElevenLabs text-to-speech API.",
  text = "Hola, bienvenido a ElevationSport, soy Elev, tu asistente de entrenamiento personal. Estoy aquí para ayudarte a alcanzar los objetivos de tu club o escuela deportiva y llevarla al siguiente nivel. ¿En qué puedo ayudarte hoy?",
  voice_id = "JBFqnCBsd6RMkjVDRZzb",  # browse voices at elevenlabs.io/app/voice-library
  model_id = "eleven_v3",
  output_format="mp3_44100_128",
)

play(audio)