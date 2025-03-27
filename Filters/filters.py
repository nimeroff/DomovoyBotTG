from aiogram.filters import BaseFilter
from ConfigData.config import Config, load_config
from aiogram.types import Message, ChatMemberMember, ChatMemberRestricted, ChatMemberAdministrator
from ConfigDB.user_db import SQL
from aiogram import Bot

config: Config = load_config()

class IsAdmin(BaseFilter):
    #admin_id =config.adminc.Adminstr
    async def __call__(self, message:Message) -> bool:
        #return str(message.from_user.id) == self.admin_id
        s = SQL()
        return s.USERADM(user_id=message.from_user.id)

class IsRegistration(BaseFilter):
    async def __call__(self, message:Message) -> bool:
        s = SQL()
        return s.EXISTUSER(user_id=message.from_user.id, reg=True)

class IsNotRegistration(BaseFilter):
    async def __call__(self, message:Message) -> bool:
        s = SQL()
        return not s.EXISTUSER(user_id=message.from_user.id, reg=True)

class LenNumPhone(BaseFilter):
    async def __call__(self,message:Message) -> bool:
        st = message.text
        if len(st)!=10:
            return False
        else:
            return True

class IsKv(BaseFilter):
    async def __call__(self,message:Message) -> bool:
        kv = int(message.text)
        if kv<1 or kv>426:
            return False
        else:
            return True

class IsNameButton(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.text in ('Назад в главное меню','Изменить имя','Изменить телефон','Изменить номер квартиры','Изменить номер авто',
                            'Нет авто','Регистрация','Поиск','Справочник','Редактировать профиль','Профиль','/getid','Незарегистрированные'):
            return False
        else:
            return True

class IsGroupMess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.id == int(config.groupid.GroupIDStr):
            return False
        else:
            return True

class IsFromGroupMess(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.chat.id == int(config.groupid.GroupIDStr):
            return True
        else:
            return False

class IsChatMember(BaseFilter):
    async def __call__(self, message: Message, bot:Bot) -> bool:
        user_status = await bot.get_chat_member(config.groupid.GroupIDStr, message.from_user.id)
        if isinstance(user_status, ChatMemberMember) or isinstance(user_status, ChatMemberRestricted) or isinstance(user_status, ChatMemberAdministrator):
            return True
        else:
            return False

class IsEN(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        alf: list[str] = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S','T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        findtext = message.text if message.text is not None else ''
        bl = False
        for smb in findtext:
            if smb.upper() in alf:
                bl = True
        if bl == True:
            return False
        else:
            return True



