import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from ConfigData.config import Config, load_config
from Handlers import other_handlers, admin_handlers, reg_handlers, work_handlers
from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
import aioschedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from time_message import send_message_1day, send_message_2day, send_message_overuser
from datetime import datetime
#set MY_ENV_VAR = valuepip

#Инициализируем логер

logger = logging.getLogger(__name__)

#Функция конфигурирования и запуска бота

async def main() -> None:
    #Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
        '[%(asctime)s] - %(name)s - %(message)s '
    )
    #Выводим консоль информации в начале запуска

    logger.info('DomovoyFlowerBot')

    #Загружаем Конфиг в переменную config

    config: Config = load_config()
    #config: Config = load_config("C:/Users/URAZGULOV/PycharmProjects/Domovoy/.env")

    #Инициализируем бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    #Сообщения по расписанию
    scheduler = AsyncIOScheduler(timezone="Asia/Yekaterinburg")
    scheduler.add_job(send_message_1day, trigger='cron', day=20, hour=12, minute=1, start_date=datetime.now(), kwargs={'bot':bot})
    scheduler.add_job(send_message_1day, trigger='cron', day=21, hour=12, minute=1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(send_message_1day, trigger='cron', day=22, hour=12, minute=1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(send_message_1day, trigger='cron', day=23, hour=12, minute=1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(send_message_2day, trigger='cron', day=24, hour=12, minute=1, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.add_job(send_message_overuser, "interval", days=60, start_date=datetime.now(), kwargs={'bot': bot})
    scheduler.start()

    #Регистрируем роутеры
    dp.include_router(admin_handlers.router)
    dp.include_router(reg_handlers.router)
    dp.include_router(work_handlers.router)
    dp.include_router(other_handlers.router)


    #Пропускать накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=["message", "inline_query", "chat_member", "callback_query"])


if __name__ == '__main__':
    asyncio.run(main())