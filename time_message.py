from aiogram import Bot
from Lexicon.lexicon_ru import LEXICON_TIME
from ConfigData.config import Config,load_config
from ConfigDB.user_db import SQL
from Function.GetMember import get_chat_members

config: Config = load_config()

async def send_message_1day(bot:Bot):
    await bot.send_message(load_config().groupid.GroupIDStr,LEXICON_TIME['1day'],message_thread_id=35443)

async def send_message_2day(bot:Bot):
    await bot.send_message(load_config().groupid.GroupIDStr,LEXICON_TIME['2day'],message_thread_id=35443)

async def send_message_overuser(bot:Bot):
    chat_members = await get_chat_members(int(config.groupid.GroupIDStr))
    s = SQL()
    s.DELETEMEMBERS()
    for memberid, membername in chat_members.items():
        s.INSERT_MEMBERS(
            user_id=memberid,
            user_name=membername
        )
    await bot.send_message(load_config().groupid.GroupIDStr,text=f'Всего незарегистрированных в чате: {s.SELECT_REP(pf=1)} \n'
                              f'Данные не подтвердили: {s.SELECT_REP(pf=2)} \n'
                              f'Данных нет, нужна регистрация: {s.SELECT_REP(pf=3)}')
