from aiogram import  Router, Bot, F, types, Dispatcher
from aiogram.types import Message, CallbackQuery,ChatMemberUpdated
from aiogram.filters import CommandStart, Text, StateFilter, Command, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, MEMBER, RESTRICTED
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from Keyboards.keyboards import create_key,create_inline_key_with_url
from Lexicon.lexicon_ru import LEXICON_MENU_REG,LEXICON_INLINE_URL, LEXICON_INLINE_URLR, LEXICON_OTHER
from ConfigDB.user_db import SQL
from ConfigData.config import Config, load_config
from Filters.filters import IsFromGroupMess


router: Router = Router()
keyboard_start = create_key(2,**LEXICON_MENU_REG)
keyboard_url = create_inline_key_with_url(1,**LEXICON_INLINE_URL)
keyboard_urlr = create_inline_key_with_url(1,**LEXICON_INLINE_URLR)
keyboard_other = create_key(3,**LEXICON_OTHER)

text1=f'ООО Управляющая компания "Новая УФА"\n' \
                         f'Телефон: 212-00-19\n' \
                         f'Диспетчерская служба:+73472120058\n' \
                         f'Гарантийная служба: +73472009201'

text2=f'ООО Управляющая компания "Новая УФА"\n' \
                         f'\t Содержание, тариф 27,3 руб/кв.м.\n' \
                         f'\t Охрана 290 руб\n' \
                         f'\t Видеонаблюдение 105,08 руб\n' \
                         f'\t Домофон 40 руб\n' \
                         f'\t Потребление коммунальных ресурсов в целях содержания общего имущества'

text3=f'ООО ИС "ТВК"\n' \
                         f'\t Холодная вода 79,67 руб/м3\n' \
                         f'\t Горячая вода:\n' \
                         f'\t\t Холодная вода 79,67 руб/м3\n' \
                         f'\t\t Подогрев холодной воды 2724,91/Гкал\n' \
                         f'\t Водоотведение (потреблённые ХВС+ГВС) 89,86 руб/м3\n' \
                         f'Телефон: +73472922322, WhatsApp +79872540466'

text4=f'ООО "Энергетическая сбытовая компания Башкортостана"\n' \
                         f'\tЭлектроэнергия однотарифный 2,81 руб. кВт*ч"\n' \
                         f'\tС другими тарифами вы можете ознакомиться\n' \
                         f'\tна их сайте\n' \
                         f'Телефон: +73472222200, +73472222255'

text5=f'ЧОП «Медведь - Уфа"\n' \
                         f'Номера охраны:\n' \
                         f'\t\t+79273399048\n' \
                         f'\t\t+79273206836\n' \
                         f'\t\t+79371564536'

@router.message(CommandStart())
async def other_start_command(message: Message):
    await message.answer(f'Вы не состоите в чате 3 квартала ЖК ЦБ,\n'
                         f'но вы можете ознакомиться с информацией в меню',reply_markup=keyboard_other)

@router.message(Text(text='УК Новая УФА'))
async def dict_spr(message: Message):
    await message.answer(text1)

@router.message(Text(text='Квартплата'))
async def dict_spr(message: Message):
    await message.answer(text2)
    await message.answer(text3)
    await message.answer(text4)

@router.message(Text(text='Охрана'))
async def dict_spr(message: Message):
    await message.answer(text5)

@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
async def new_member(event: ChatMemberUpdated, bot:Bot):
    s = SQL()
    config: Config = load_config()
    nameuser = event.new_chat_member.user.username if event.new_chat_member.user.username is not None else event.new_chat_member.user.first_name
    if s.EXISTUSER(user_id=event.new_chat_member.user.id,reg=True) | s.EXISTUSER(user_id=event.new_chat_member.user.id,reg=False):
        await bot.send_message(config.groupid.GroupIDStr,
                               text=f"Добро пожаловать, <a href='tg://user?id={event.new_chat_member.user.id}'><b>{nameuser}</b></a>, в чат 3 квартала!",
                               parse_mode="html",
                               reply_markup=keyboard_urlr)
    else:
        await bot.send_message(config.groupid.GroupIDStr,f"Привет, <a href='tg://user?id={event.new_chat_member.user.id}'><b>{nameuser}</b></a>, я бот 'Домовой'. \n"
                                              f"Добро пожаловать в чат 3 квартала! \n"
                                              f"Просьба пройти регистрацию в боте.\n"
                                              f"В противном случае вы будете исключены из чата \n"
                                              f"Спасибо!\n",
                               reply_markup=keyboard_url)


@router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER >> IS_NOT_MEMBER))
async def new_member(event: ChatMemberUpdated, bot:Bot):
    s = SQL()
    if s.EXISTUSER(user_id=event.new_chat_member.user.id,reg=True) or s.EXISTUSER(user_id=event.new_chat_member.user.id,reg=False):
        s.UPDATE(pf=4,valuewhere=0,iduser=event.new_chat_member.user.id)


@router.message(Command(commands=["getid"]))
async def getid(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,f"ID: {message.from_user.id}")


@router.message(Command(commands=["getuk"]))
async def getid(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,text1)


@router.message(Command(commands=["getkv"]))
async def getid(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,text2)
    await bot.send_message(message.from_user.id, text3)
    await bot.send_message(message.from_user.id, text4)


@router.message(Command(commands=["getsc"]))
async def getid(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id, text5)

#@router.message()
#async def mess_topic(message: types.Message,bot:Bot):
    text = message.text.lower()
    config: Config = load_config()

#    if 'бот' in text:
#        await bot.send_message(config.groupid.GroupIDStr,"Что? Напиши мне в личку",reply_to_message_id=message.message_thread_id,reply_markup=keyboard_urlr)
#    if 'тема3' in text:
#        await bot.send_message(config.groupid.GroupIDStr,"Тест тема3",message_thread_id=2)
#        await bot.send_message(config.groupid.GroupIDStr, "Тест тема3General")


@router.message(IsFromGroupMess())
async def stg2(message: types.Message):
    text = message.text.lower() if message.text is not None else ""
    if 'поделит' in text or 'отправ' in text or 'подска' in text or 'скин' in text or 'какой' in text or 'кому' in text or 'скажит' in text or 'написат' in text or 'кто' in text or 'куда' in text:
        if 'номер' in text or 'телефон' in text or 'звонить' in text:
            if 'ук' in text or 'управляющ' in text or 'диспетчер' in text or ('гарантийн' in text and 'отдел' in text):
                await message.answer(text1)  # выводим номер УК
            elif 'охран' in text:
                await message.answer(text5)  # выводим номер охраны
            elif 'твк' in text or 'отопление' in text or 'воду' in text:
                await message.answer(text3)  # выводим номер охраны
            elif 'электроэнерг' in text or 'эскб' in text or 'свет' in text:
                await message.answer(text4)  # выводим номер охраны
            elif 'нет' in text or 'пропал' in text or 'отсутствует' in text or 'исчез' in text:
                if 'свет' in text or 'отоплен' in text or 'электричеств' in text or 'вод' in text:
                    await message.answer(text1)  # выводим номер УК
        elif 'твк' in text or 'отопление' in text or 'воду' in text:
            await message.answer(text3)  # выводим номер охраны
        elif 'электроэнерг' in text or 'эскб' in text or 'свет' in text:
            await message.answer(text4)  # выводим номер охраны
