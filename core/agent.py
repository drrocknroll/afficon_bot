import os
import json
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# === Настройки Telegram ===
BOT_TOKEN = os.getenv("BOT_TOKEN") or "твой_токен"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class AlexBSalesAgent:
    def __init__(self, profile="partners"):
        self.profile = profile
        self.load_personal_traits()
        self.db = self.init_db()
        
    def load_personal_traits(self):
        """Загрузка персональных характеристик"""
        base_path = "C:/Users/user/Projects/backend/ai_agents/AlexB-Sales/personal"
        self.psych_profile = self.load_text_file(f"{base_path}/psych_report.txt")
        self.nlp_profile = self.load_text_file(f"{base_path}/nl_profile.txt")
        self.chat_styles = self.load_messenger_styles(f"{base_path}/messenger_chats")
        
    def load_text_file(self, path):
        """Загрузка текстового файла"""
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def load_messenger_styles(self, dir_path):
        """Загрузка стилей общения из мессенджеров"""
        styles = {}
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith('.txt'):
                    platform = filename.split('.')[0]
                    styles[platform] = self.load_text_file(f"{dir_path}/{filename}")
        return styles
        
    def init_db(self):
        """Инициализация базы данных"""
        db_path = "C:/Users/user/Projects/backend/ai_agents/AlexB-Sales/data"
        os.makedirs(db_path, exist_ok=True)
        return sqlite3.connect(f"{db_path}/{self.profile}.db")
    
    def switch_profile(self, new_profile):
        """Переключение между профилями (партнёры/клиенты/поставщики)"""
        self.profile = new_profile
        self.db.close()
        self.db = self.init_db()
        print(f"Переключено на профиль: {new_profile}")

# === Telegram хендлеры ===

@dp.message_handler(commands=["start"])
async def handle_start(message: Message):
    await message.answer("👋 Привет! Я AlexB-Sales — бот-агент по работе с партнёрами. Готов помочь!")

# Пример использования
if __name__ == "__main__":
    agent = AlexBSalesAgent()
    print("Агент AlexB-Sales инициализирован!")
    print(f"Загружено стилей общения: {len(agent.chat_styles)}")

    # Возможность запустить бота в polling-режиме (локально)
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
