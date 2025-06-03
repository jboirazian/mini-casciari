from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os


CUENTO="""¿Diez años tenía yo? Sí, por ahí. Diez, once. Un verano en Buenos Aires, que para un chico de pueblo era como un viaje a la luna. Fuimos al Parque de la Costa, creo que fue la primera vez. Íbamos con mi tía Nélida, la que siempre me decía que yo tenía "cara de pillo". Y con mi primo Pepe. Pepe era de esos primos que estaban, ¿viste? Ni te molestaba, ni te divertía. Era como un mueble bajito, pero con rulos."""


load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

audio = elevenlabs.text_to_speech.convert(
    text=CUENTO,
    voice_id="2sPiogxCOM4lQ2KuKL6C",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    
)

# Save the generator to an MP3 file
with open("test2.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)