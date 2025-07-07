from fastapi import FastAPI, Request
from aiogram import types

# Импортируем бота и диспетчер из основного файла с логикой бота
from core.agent import bot, dp

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from afficon_bot!"}

@app.post("/webhook")
async def telegram_webhook(req: Request):
    update = await req.json()
    TelegramRequest = types.Update.to_object(update)
    await dp.process_update(TelegramRequest)
    return {"status": "ok"}
