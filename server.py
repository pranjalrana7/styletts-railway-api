import torch
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import gdown

app = FastAPI()

# Lazy model load
model = None

MODEL_PATH = "styletts2.pt"
MODEL_URL = "https://drive.google.com/uc?id=1yqaC7uNqjaWg5B8yPXoD3bMBDZomjNCE"

def load_styletts2():
    global model
    if os.path.exists(MODEL_PATH) is False:
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
    
    if model is None:
        model = torch.jit.load(MODEL_PATH, map_location="cpu")
    return model


@app.get("/")
async def root():
    return {"status": "StyleTTS2 API running"}


@app.get("/tts")
async def tts(text: str = "Hello from StyleTTS2"):
    m = load_styletts2()

    with torch.no_grad():
        audio = m(text)

    out_path = "output.wav"
    torchaudio.save(out_path, audio.unsqueeze(0), 22050)

    return FileResponse(out_path, media_type="audio/wav")
