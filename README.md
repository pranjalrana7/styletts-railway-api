# Parler-TTS-Medium (template)

This repo runs a small TTS API using Coqui `TTS` and exposes `/tts?text=...&fmt=mp3`.

## Usage
1. Set `MODEL_NAME` environment variable to the model you want to use (default uses a small demo model).
2. If the model requires a Hugging Face token to download, set `HUGGINGFACE_TOKEN` env var.
3. Deploy on Railway/Render. The first request will download the model (lazy load) and may take time.

## Endpoints
- `GET /` → health
- `GET /tts?text=Your+text&fmt=mp3` → returns 
