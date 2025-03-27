from pyrogram import Client
from ConfigData.config import Config, load_config

config: Config = load_config()

api_id = config.apiid.id
api_hash = config.apihash.hash
bot_token = config.tg_bot.token

async def get_chat_members(chat_id):
    app = Client("FlowerBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_member: dict[int, str] = {}
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_member[member.user.id] = member.user.username if member.user.username is not None else member.user.first_name
    await app.stop()
    return chat_member
