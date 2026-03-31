import io
import edge_tts
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Permisos para que tu web de Vercel pueda hablar con Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {
        "status": "CreatorForge AI Corriendo",
        "message": "Listo para generar voz y overlays",
        "region": "Oregon, USA"
    }

@app.get("/tts")
async def text_to_speech(text: str = Query(..., min_length=1), voice: str = "es-MX-AlonsoNeural"):
    communicate = edge_tts.Communicate(text, voice)
    audio_data = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.write(chunk["data"])
    
    audio_data.seek(0)
    return StreamingResponse(audio_data, media_type="audio/mpeg")
