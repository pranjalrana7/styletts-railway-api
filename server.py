import os
import uuid
import shutil
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from TTS.api import TTS
from pydub import AudioSegment

app = FastAPI()

# Model name to load at runtime. Change to Parler-Medium model ID if available.
MODEL_NAME = os.environ.get("MODEL_NAME", "tts_models/en/ljspeech/tacotron2-DDC")
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

# Lazy-loaded TTS object
_tts = None

def get_tts():
    global _tts
    if _tts is None:
        # If Hugging Face token is provided, set the env variable for the TTS loader
        if HUGGINGFACE_TOKEN:
            os.environ["HUGGING_FACE_HUB_TOKEN"] = HUGGINGFACE_TOKEN
        _tts = TTS(MODEL_NAME)
    return _tts

@app.get("/")
async def root():
    return {"status": "ok", "model": MODEL_NAME}

@app.get("/tts")
async def tts(text: str = Query(..., min_length=1), fmt: str = Query("mp3", regex="^(mp3|wav)$")):
    try:
        tts = get_tts()
        tmp_id = str(uuid.uuid4())
        wav_path = f"/tmp/{tmp_id}.wav"
        out_path = f"/tmp/{tmp_id}.{fmt}"

        # Generate wav via TTS
        tts.tts_to_file(text=text, file_path=wav_path)

        if fmt == "wav":
            shutil.move(wav_path, out_path)
        else:
            # convert wav -> mp3 using pydub (ffmpeg)
            audio = AudioSegment.from_wav(wav_path)
            audio.export(out_path, format="mp3")
            os.remove(wav_path)

        return FileResponse(out_path, media_type="audio/mpeg" if fmt=="mp3" else "audio/wav", filename=f"tts.{fmt}")

    except Exception as e:
        raise HTTPException(status_code=500, 
