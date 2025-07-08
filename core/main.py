# core/main.py
from fastapi import FastAPI, Request
from aiogram import types
from core.agent import bot, dp

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from afficon_bot!"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
    return {"status": "ok"}
