from email.iterators import typed_subpart_iterator

from aiogram import  Router, Bot, F, types, Dispatcher
from aiogram.types import Message, CallbackQuery,ChatMemberUpdated
from aiogram.filters import CommandStart, Text, StateFilter, Command, IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, MEMBER, RESTRICTED
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from Keyboards.keyboards import create_key,create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU_REG,LEXICON_INLINE_REG, LEXICON_MENU,LEXICON_INLINE_YESNO, LEXICON_INLINE_AGREE, LEXICON_MENU_AUTO
from ConfigDB.user_db import SQL
from ConfigData.config import podjezd
from Filters.filters import IsNotRegistration,IsGroupMess, IsChatMember, IsEN
from Handlers import work_handlers
from Filters.filters import LenNumPhone, IsKv
from ConfigDB.user_db import SQL
from Function.functions import existkv, lowertext

router: Router = Router()
router.message.filter(IsNotRegistration(),IsGroupMess(),IsChatMember())
keyboard_work = create_key(2,**LEXICON_MENU)
keyboard_start = create_key(2,**LEXICON_MENU_REG)
keyboard_inline_start = create_inline_key(2,**LEXICON_INLINE_REG)
keyboard_auto = create_key(1, **LEXICON_MENU_AUTO)
keyboard_inline_agree = create_inline_key(2,**LEXICON_INLINE_AGREE)
keyboard_inline_yesno = create_inline_key(2,**LEXICON_INLINE_YESNO)

#Создаем базу данных пользователей
user_dict: dict[int,
                dict[str,
                     str | int | bool
                    ]
                ]={}

pod_dict: dict[str,str]={}
fl_dict: dict[str,str]={}
kv_dict: dict[str,str]={}

class FSMFillForm(StatesGroup):
    fill_name = State()
    fill_phone = State()
    fill_kv = State()
    fill_photo = State()
    fill_auto = State()

class FSMFormEdit(StatesGroup):
    fedit_name = State()
    fedit_phone = State()
    fedit_kv = State()

class FSMFormSearch(StatesGroup):
    ffind_name = State()
    ffind_phone = State()
    ffind_kv = State()

class FSMFormDict(StatesGroup):
    fdict_pod = State()
    fdict_fl = State()
    fdict_kv = State()



@router.message(CommandStart())
async def process_start_command(message: Message):
    s = SQL()
    if s.EXISTUSER(user_id=message.from_user.id, reg=False) == True:
        for row in s.SELECT(pf = 6, valuewhere = message.from_user.id):
            await message.answer(f'Здравствуйте! У вас имеются не подтверждённые данные в базе: \n'
                                    f'Имя в базе: {row.NAMEDB} \n'
                                    f'Телефон: {row.NPHONE} \n'
                                    f'Подъезд: {row.NUMPD} \n'
                                    f'Этаж: {row.NUMFL} \n'
                                    f'Квартира: {row.NUMKV} \n'
                                    f'Номер авто: {row.NUMAUTO} \n',
                               reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Отправить их на подтверждение Администратору чата?', reply_markup=keyboard_inline_yesno)
    else:
        await message.answer('Добро пожаловать!', reply_markup=types.ReplyKeyboardRemove())
        await message.answer('Прошу пройти регистрацию',reply_markup=keyboard_inline_start)

@router.callback_query(F.data.in_(["yes"]))
async def yesreg(callback:CallbackQuery, bot: Bot):
    await callback.message.answer('Данные отправлены, ожидайте ответа!')
    s = SQL()
    for ls in s.LISTADMIN():
        for row in s.SELECT(pf = 6, valuewhere = callback.from_user.id):
            await bot.send_message(ls,
                               text=f'Прошу подтвердить регистрацию нового жителя: \n'
                                    f'Имя в базе: {row.NAMEDB} \n'
                                    f'Телефон: {row.NPHONE} \n'
                                    f'Подъезд: {row.NUMPD} \n'
                                    f'Этаж: {row.NUMFL} \n'
                                    f'Квартира: {row.NUMKV} \n'
                                    f'Номер авто: {row.NUMAUTO} \n'
                               )
            await bot.send_message(ls,
                               text=f'{callback.from_user.id} \n',
                               reply_markup=keyboard_inline_agree)


"""
    Регистрация Регистрация Регистрация Регистрация 
"""
@router.callback_query(F.data.in_(['registr']) | F.data.in_(["no"]))
async def anceta_start(message: Message,bot: Bot, state: FSMContext):
    s = SQL()
    s.DELETE(pf=1,iduser=message.from_user.id)
    await bot.send_message(message.from_user.id, f'Заранее подготовьте фото квитанции/прописки/выписка из ЕГРН\n Чтобы администратор мог убедиться в представленных вами данных')
    await bot.send_message(message.from_user.id, 'Укажите ваше имя:')
    #Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)

@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def anceta_name(message: Message, state: FSMContext):
    #Сохраняем введенное имя в хранилище
    await state.update_data(name=message.text)
    await message.answer('Ваш номер телефона без "+7" и без "8" в формате XXX***XX**:')
    #Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_phone)

@router.message(StateFilter(FSMFillForm.fill_name))
async def anceta_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Некорректный ввод имени, прошу снова внести имя буквами')
    await state.set_state(FSMFillForm.fill_name)

@router.message(StateFilter(FSMFillForm.fill_phone),LenNumPhone(),F.text.isdigit())
async def anceta_name(message: Message, state: FSMContext):
    #Сохраняем введенный номер телефона в хранилище
    await state.update_data(phone=message.text)
    await message.answer('Ваш номер квартиры:')
    #Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_kv)

@router.message(StateFilter(FSMFillForm.fill_phone))
async def anceta_name(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('Прошу внести номер телефона цифрами в формате XXX***XX**, всего 10 цифр, прошу внести снова:')
    await state.set_state(FSMFillForm.fill_phone)

@router.message(StateFilter(FSMFillForm.fill_kv),F.text.isdigit(), IsKv())
async def anceta_name(message: Message, state: FSMContext):
    #Сохраняем введенный номер квартиры в хранилище
    await state.update_data(numkv=message.text)
    await message.answer('Номер авто, в формате А111АА102 (русские буквы):', reply_markup=keyboard_auto)
    await state.set_state(FSMFillForm.fill_auto)

@router.message(StateFilter(FSMFillForm.fill_kv))
async def anceta_name(message: Message, state: FSMContext):
    await state.update_data(numkv=message.text)
    await message.answer('Некорректный ввод номера квартиры, всего 426 квартир, прошу внести цифрами:')
    await state.set_state(FSMFillForm.fill_kv)

@router.message(StateFilter(FSMFillForm.fill_auto),IsEN())
async def anceta_name(message: Message, state: FSMContext):
    #Сохраняем введенный номер авто в хранилище
    autonumber = message.text.lower() if message.text is not None else ""
    await state.update_data(numauto=lowertext(autonumber))
    await message.answer('Приложите фото, подтверждающее регистрацию:',reply_markup=types.ReplyKeyboardRemove)
    await state.set_state(FSMFillForm.fill_photo)

@router.message(StateFilter(FSMFillForm.fill_auto))
async def anceta_name(message: Message, state: FSMContext):
    #Обрабатывает ошибку ввода номера авто
    autonumber = message.text.lower() if message.text is not None else ""
    await state.update_data(numauto=lowertext(autonumber))
    await message.answer('Некорректный номер авто, используйте русские буквы:',reply_markup=types.ReplyKeyboardRemove)
    await state.set_state(FSMFillForm.fill_auto)


@router.message(StateFilter(FSMFillForm.fill_photo),F.photo)
async def anceta_name(message: Message, state: FSMContext, bot: Bot):
    #Устанавливаем состояние ожидания ввода имени
    user_dict[message.from_user.id] = await state.get_data()
    photo_data = message.photo[-1]
    namedb = user_dict[message.from_user.id]["name"]
    s = SQL()
    s.INSERT(
        user_id=message.from_user.id,
        user_name=message.from_user.first_name,
        logintg=message.from_user.username,
        namedb=namedb.lower(),
        fios=message.from_user.full_name,
        nphone="+7" + user_dict[message.from_user.id]["phone"],
        numpd=existkv(vnkv=int(user_dict[message.from_user.id]["numkv"]),param=True)[1],
        numfl=existkv(vnkv=int(user_dict[message.from_user.id]["numkv"]),param=True)[2],
        numkv=user_dict[message.from_user.id]["numkv"],
        numauto=user_dict[message.from_user.id]["numauto"],
        regflag=False
    )
    await state.clear()
    await message.answer(f'Спасибо за регистрацию! \n Я отправлю данные для подтверждения администратору')
    vnumpd = existkv(vnkv=int(user_dict[message.from_user.id]["numkv"]),param=True)[1]
    vnumfl = existkv(vnkv=int(user_dict[message.from_user.id]["numkv"]),param=True)[2]
    # Отправляем сохранённые данные пользователю
    if message.from_user.id in user_dict:
        await message.answer(text=f'Имя в базе: {user_dict[message.from_user.id]["name"]} \n'
                                  f'Телефон: {user_dict[message.from_user.id]["phone"]} \n'
                                  f'Подъезд: {vnumpd} \n'
                                  f'Этаж: {vnumfl} \n'
                                  f'Квартира: {user_dict[message.from_user.id]["numkv"]} \n'
                                  f'Номер авто: {user_dict[message.from_user.id]["numauto"]} \n',
                                  reply_markup=types.ReplyKeyboardRemove()
                             )
        # Отправляем данные нового юзера админам
        for ls in s.LISTADMIN():
            await bot.send_message(ls,
                                  text=f'Прошу подтвердить регистрацию нового жителя: \n'
                                  f'Имя в базе: {user_dict[message.from_user.id]["name"]} \n'
                                  f'Телефон: {user_dict[message.from_user.id]["phone"]} \n'
                                  f'Подъезд: {vnumpd} \n'
                                  f'Этаж: {vnumfl} \n'
                                  f'Квартира: {user_dict[message.from_user.id]["numkv"]} \n'
                                  f'Номер авто: {user_dict[message.from_user.id]["numauto"]} \n'
                                  )
            await bot.send_photo(ls,photo=photo_data.file_id)
            await bot.send_message(ls,
                                   text=f'{message.from_user.id} \n',
                                   reply_markup=keyboard_inline_agree
                                   )
    else:
        await message.answer('Вы не прошли регистрацию', reply_markup=keyboard_start)
    #router.include_router(work_handlers.router)


@router.message(StateFilter(FSMFillForm.fill_photo))
async def anceta_name(message: Message, state: FSMContext):
    #Сохраняем фото квартиры в хранилище
    await state.update_data(photo=message.photo[-1])
    await message.answer('Пришлите фото!')
    await state.set_state(FSMFillForm.fill_photo)
