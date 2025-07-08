from fastapi import FastAPI, Request
from aiogram import types
from core.agent import dp  # <-- импортируешь диспетчер из agent.py

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from afficon_bot!"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()
    telegram_update = types.Update.to_object(update)
    await dp.process_update(telegram_update)
    return {"status": "ok"}