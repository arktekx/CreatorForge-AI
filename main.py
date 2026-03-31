from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts
import hashlib
import os

app = FastAPI()

# Esto permite que tu página web (Frontend) hable con tu servidor (Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carpeta para guardar los audios temporales
CACHE_DIR = "static/audio_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "CreatorForge AI Corriendo", "message": "Listo para generar voz y overlays"}

@app.get("/tts")
async def text_to_speech(text: str = Query(..., min_length=1), voice: str = "es-MX-AlonsoNeural"):
    """
    Ruta para convertir texto a voz de Alonso.
    Ejemplo: /tts?text=Hola+Chat&voice=es-MX-AlonsoNeural
    """
    try:
        # Creamos un nombre único para el archivo basado en el texto y la voz
        file_name = hashlib.md5(f"{text}{voice}".encode()).hexdigest() + ".mp3"
        file_path = os.path.join(CACHE_DIR, file_name)

        # Si el audio no existe, lo generamos con edge-tts
        if not os.path.exists(file_path):
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file_path)

        # Devolvemos el archivo de audio para que el navegador lo reproduzca
        return FileResponse(file_path, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}

# Esta ruta servirá para la IA de Overlays más adelante
@app.get("/generate-overlay")
async def overlay_gen(prompt: str):
    return {"message": f"Próximamente: Generando overlay para '{prompt}' con IA"}