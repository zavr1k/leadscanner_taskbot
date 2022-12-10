import uvicorn
from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI

from bot_api.taskbot import router
from bot_telegram.taskbot import bot, dp
from config import settings
from database import async_session, init_models

WEBHOOK_PATH = f'/{settings.API_TOKEN}/'
WEBHOOK_URL = f'https://{settings.WEBHOOK_HOST}{WEBHOOK_PATH}'

app = FastAPI()
app.include_router(router=router)


@app.on_event('startup')
async def on_startup() -> None:
    bot['db'] = async_session
    await dp.skip_updates()
    await bot.delete_webhook()
    await bot.set_webhook(
        url=WEBHOOK_URL,
    )
    await init_models()


@app.on_event('shutdown')
async def on_shutdown() -> None:
    await bot.delete_webhook()


@app.post(WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict) -> None:
    telegraam_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegraam_update)


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
