import sys
sys.path.insert(0, "/root/pybot")

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import AsyncOpenAI
from typing import AsyncGenerator
import json, config

app = FastAPI()
client = AsyncOpenAI(base_url="https://polza.ai/api/v1", api_key=config.POLZA_KEY)
ALLOWED = set(config.MODELS.keys())

class ChatReq(BaseModel):
    messages: list[dict]
    model: str = "x-ai/grok-4.1-fast"

async def stream(messages, model) -> AsyncGenerator[str, None]:
    try:
        async with client.chat.completions.stream(
            model=model, messages=messages, max_tokens=1500
        ) as s:
            async for chunk in s:
                text = chunk.choices[0].delta.content if chunk.choices else None
                if text:
                    yield f"data: {json.dumps({"text": text})}\n\n"
        yield "data: [DONE]\n\n"
    except Exception as e:
        yield f"data: {json.dumps({"error": str(e)})}\n\n"

@app.post("/api/chat")
async def chat(req: ChatReq):
    model = req.model if req.model in ALLOWED else "x-ai/grok-4.1-fast"
    return StreamingResponse(
        stream(req.messages, model),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )

app.mount("/", StaticFiles(directory="/root/pybot/public", html=True), name="static")
