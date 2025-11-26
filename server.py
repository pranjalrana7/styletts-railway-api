from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
import torch
import uuid
import os
from TTS.api import TTS

app = FastAPI()

# Load a lightweight StyleTTS model (works on CPU)
model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name)

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
async def generate_tts(req: TTSRequest):
    try:
        output_path = f"{uuid.uuid4()}.wav"
        tts.tts_to_file(text=req.text, file_path=output_path)

        return FileResponse(output_path, media_type="audio/wav", filename="output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))