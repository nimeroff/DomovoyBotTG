from aiogram import  Router, Bot, F, types, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Text, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from Keyboards.keyboards import create_key,create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU_REG, LEXICON_MENU, LEXICON_INLINE_FINDA, LEXICON_EDITPROFILE, LEXICON_MENU_ADMIN, LEXICON_EDIT
from ConfigDB.user_db import SQL
from ConfigData.config import podjezd
from ConfigData.config import Config, load_config
from Filters.filters import IsAdmin,IsGroupMess, IsNameButton, IsKv
from Function.functions import existkv, lowertext
from Function.GetMember import get_chat_members

router: Router = Router()
router.message.filter(IsAdmin(),IsGroupMess())
keyboard_start = create_key(2,**LEXICON_MENU_ADMIN)
keyboard_inline_find = create_inline_key(1, **LEXICON_INLINE_FINDA)
keyboard_inline_edit = create_inline_key(2,**LEXICON_EDIT)

id_dict: dict[str,str | int | bool] = {}
pod_dict: dict[str, str] = {}
fl_dict: dict[str, str] = {}
kv_dict: dict[str, str] = {}

config: Config=load_config()

class FSMFormAgree(StatesGroup):
    fyes = State()
    fno = State()

class FSMFormSe(StatesGroup):
    ffind_name = State()
    ffind_phone = State()
    ffind_kv = State()
    ffind_auto = State()

class FSMFormD(StatesGroup):
    fdict_pod = State()
    fdict_fl = State()
    fdict_kv = State()

class FSMFormEd(StatesGroup):
    feditname = State()
    feditkv = State()
    feditavto = State()
    feditphone = State()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Вы администратор', reply_markup=keyboard_start)

@router.callback_query(F.data.in_(['yesagree']))
async def agreebutton(callback: CallbackQuery, bot: Bot):
    s = SQL()
    idnum = int(callback.message.text)
    if s.UPDATE(pf = 4, valuewhere = True, iduser = idnum):
        await callback.message.answer(f'Заявка принята! {callback.message.text}')
        await bot.send_message(idnum,'Ваша заявка принята, нажмите ->>> /start')


@router.callback_query(F.data.in_(['noagree']))
async def agreebutton(callback: CallbackQuery, bot: Bot):
    s = SQL()
    idnum = int(callback.message.text)
    if s.DELETE(pf=1, iduser=idnum):
        await callback.message.answer(f'Заявка отклонена! {callback.message.text}')
        await bot.send_message(idnum, 'Ваша заявка отклонена /start')


@router.message(Text(text='убери меню'))
async def deletemenu(message:Message,bot:Bot):
    # config: Config = load_config()
    # await bot.send_message(chat_id= config.groupid,text='Удалил меню, исправь этот баг, больше удалять не буду',reply_markup=types.ReplyKeyboardRemove)
    await message.answer(text='Удалил меню, исправь этот баг, больше удалять не буду',reply_markup=types.ReplyKeyboardRemove)

# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
@router.message(Text(text='Поиск'))
async def anceta_find(message: Message):
    await message.answer('Как будем искать?', reply_markup=keyboard_inline_find)

@router.callback_query(F.data.in_(['afindname']))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите имя для поиска:')
    await state.set_state(FSMFormSe.ffind_name)

@router.message(StateFilter(FSMFormSe.ffind_name),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введенное значение для поиска
    #await state.update_data(ffindname=message.text)
    #user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    s = SQL()
    # print(user_dict[message.from_user.id]['ffindname'])
    #for row in s.SELECT(pf=1, valuewhere=user_dict[message.from_user.id]['ffindname']):
    sqls = s.SELECT(pf=1, valuewhere=message.text)
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=1, valuewhere=message.text):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n'
                                 )
            await message.answer(text=row.User_id,reply_markup=keyboard_inline_edit)
    else:
        await message.answer('С таким именем человека в базе нет')


@router.callback_query(Text(text='afindphone'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер телефона через 8:')
    await state.set_state(FSMFormSe.ffind_phone)

@router.message(StateFilter(FSMFormSe.ffind_phone),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введеннОе значение для поискв
    # await state.update_data(ffindphone=message.text)
    # user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    s = SQL()
    # for row in s.SELECT(pf=2, valuewhere=user_dict[message.from_user.id]['ffindphone']):
    sqls = s.SELECT(pf=2, valuewhere=message.text)
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=2, valuewhere=message.text):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n'
                                 )
            await message.answer(text=row.User_id,reply_markup=keyboard_inline_edit)
    else:
        await message.answer('С таким номером человека в базе нет')


@router.callback_query(Text(text='afindkv'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер квартиры')
    await state.set_state(FSMFormSe.ffind_kv)


@router.message(StateFilter(FSMFormSe.ffind_kv),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введеннОе значение для поиска
    # await state.update_data(ffindkv=message.text)
    # user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    s = SQL()
    # for row in s.SELECT(pf=3, valuewhere=user_dict[message.from_user.id]['ffindkv']):
    sqls = s.SELECT(pf=3, valuewhere=message.text)
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=3, valuewhere=message.text):
           await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                     f'Телефон: {row.NPHONE} \n'                                  
                                     f'Подъезд: {row.NUMPD} \n'
                                     f'Этаж: {row.NUMFL} \n'
                                     f'Квартира: {row.NUMKV} \n'
                                     f'Номер авто: {row.NUMAUTO} \n'
                                     f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n'
                                 )
           await message.answer(text=row.User_id,reply_markup=keyboard_inline_edit)
    else:
        await message.answer('В этой квартире никто не зарегистрирован')

@router.callback_query(Text(text='afindauto'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите часть номера авто')
    await state.set_state(FSMFormSe.ffind_auto)


@router.message(StateFilter(FSMFormSe.ffind_auto),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введеннОе значение для поискв
    await state.clear()
    s = SQL()
    sqls = s.SELECT(pf=5, valuewhere=message.text.lower() if message.text is not None else "")
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=5, valuewhere=message.text.lower() if message.text is not None else ""):
           await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                     f'Телефон: {row.NPHONE} \n'                                  
                                     f'Подъезд: {row.NUMPD} \n'
                                     f'Этаж: {row.NUMFL} \n'
                                     f'Квартира: {row.NUMKV} \n'
                                     f'Номер авто: {row.NUMAUTO} \n'
                                     f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n'
                                 )
           await message.answer(text=row.User_id,reply_markup=keyboard_inline_edit)
    else:
        await message.answer('Нет данных по этому авто')

# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник
# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник
# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник

@router.message(Text(text='Справочник'))
async def dictionary_start(message: Message, state: FSMContext):
    pod_dict.clear()
    await state.clear()
    for i in range(1, len(podjezd) + 1):
        pod_dict.update({'p' + str(i) + 'podac': str(i) + ' подъезд'})
    keyboard_inline_dict = create_inline_key(1, **pod_dict)
    await message.answer('Подъезды', reply_markup=keyboard_inline_dict)
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFormD.fdict_pod)


def createdictfloor(pd: str):
    fl_dict.clear()
    i = int(pd[1])
    if i == 8:
        jj = 2
    else:
        jj = 1
    fl_dict.update({'p' + str(i) + 'ff' + 'backflac': '<<Назад'})
    for j in range(jj, len(podjezd[i]) + jj):
        fl_dict.update({'p' + str(i) + 'f' + str(j) + 'flac': str(j) + ' этаж'})


@router.callback_query(FSMFormD.fdict_pod)
async def dictionary_start(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'p1podac':
        createdictfloor('p1podac')
    if callback.data == 'p2podac':
        createdictfloor('p2podac')
    if callback.data == 'p3podac':
        createdictfloor('p3podac')
    if callback.data == 'p4podac':
        createdictfloor('p4podac')
    if callback.data == 'p5podac':
        createdictfloor('p5podac')
    if callback.data == 'p6podac':
        createdictfloor('p6podac')
    if callback.data == 'p7podac':
        createdictfloor('p7podac')
    if callback.data == 'p8podac':
        createdictfloor('p8podac')
    else:
        pass
    keyboard_inline_dict = create_inline_key(1, **fl_dict)
    await callback.message.edit_text('Этажи:', reply_markup=keyboard_inline_dict)
    await state.set_state(FSMFormD.fdict_fl)

def fl_backshow(pflk: str):
    if pflk[4:8] == 'back':
        return True
    elif pflk[4:8] == 'flac':
        return False

def createdictkv(pfl: str):
    kv_dict.clear()
    p = int(pfl[1])
    f = int(pfl[3])
    kv_dict.update({'p' + str(p) + 'f' + str(f) + 'backkv': '<<'})
    s = SQL()
    for j in range(podjezd[p][f][0], podjezd[p][f][1] + 1):
        for row in s.SELECT(pf=3, valuewhere=j):
            kv_dict.update({'p' + str(p) + 'f' + str(f) + 'kvkv' + str(j): str(j)})


@router.callback_query(FSMFormD.fdict_fl)
async def dictionary_start(Callback: CallbackQuery, state: FSMContext):
    if fl_backshow(str(Callback.data)) == False:
        createdictkv(str(Callback.data))
        keyboard_inline_dict = create_inline_key(7, **kv_dict)
        await Callback.message.edit_text('Квартиры:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormD.fdict_kv)
    elif fl_backshow(str(Callback.data)) == True:
        keyboard_inline_dict = create_inline_key(1, **pod_dict)
        await Callback.message.edit_text('Подъезды:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormD.fdict_pod)



def kv_backshow(pflk: str):
    if pflk[4:8] == 'back':
        return True
    elif pflk[4:8] == 'kvkv':
        return False


@router.callback_query(FSMFormD.fdict_kv)
async def dictionary_start(Callback: CallbackQuery, state: FSMContext):
    if kv_backshow(str(Callback.data)) == False:
        keyboard_inline_dict = create_inline_key(7, **kv_dict)
        st = str(Callback.data)
        kv = st[8:len(st)]
        s = SQL()
        for row in s.SELECT(pf=3, valuewhere=kv):
            await Callback.message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                               f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n'
                                               f'Подъезд: {row.NUMPD} \n'
                                               f'Этаж: {row.NUMFL} \n'
                                               f'Квартира: {row.NUMKV} \n'
                                               f'Машина: {row.NUMAUTO} \n'
                                               f'Телефон: {row.NPHONE} \n')
        await state.set_state(FSMFormD.fdict_kv)
    elif kv_backshow(str(Callback.data)) == True:
        keyboard_inline_dict = create_inline_key(1, **fl_dict)
        await Callback.message.edit_text('Этажи:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormD.fdict_fl)



#Редактирование профиля юзера Редактирование профиля юзера Редактирование профиля юзера Редактирование профиля юзера
#Редактирование Редактирование Редактирование Редактирование Редактирование Редактирование Редактирование Редактирование Редактирование Редактирование
@router.callback_query(Text(text='editname'))
async def anceta_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(userid=callback.message.text)
    await callback.message.answer('Введите новое имя:')
    await state.set_state(FSMFormEd.feditname)

@router.message(StateFilter(FSMFormEd.feditname),IsNameButton())
async def anceta_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    id_dict = await state.get_data()
    s = SQL()
    if s.UPDATE(pf=1, valuewhere=id_dict["name"], iduser=int(id_dict["userid"])):
        await message.answer('Имя изменено:' + message.text)
        await state.clear()
    sqls = s.SELECT(pf=4, valuewhere=int(id_dict["userid"]))
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=4, valuewhere=int(id_dict["userid"])):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n',
                                 reply_markup=keyboard_start
                                 )
        id_dict.clear()
    else:
        await message.answer('С таким номером человека в базе нет')

@router.callback_query(Text(text='editkv'))
async def anceta_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(userid=callback.message.text)
    await callback.message.answer('Введите квартиру:')
    await state.set_state(FSMFormEd.feditkv)

@router.message(StateFilter(FSMFormEd.feditkv),IsNameButton(), IsKv())
async def anceta_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    id_dict = await state.get_data()
    numpod = existkv(vnkv=int(message.text),param=True)[1]
    numfl = existkv(vnkv=int(message.text), param=True)[2]
    s = SQL()
    if s.UPDATE(pf=6, valuewhere=numpod, iduser=int(id_dict["userid"])):
        await message.answer('Номер подъезда изменен:' + str(numpod))
    if s.UPDATE(pf=7, valuewhere=numfl, iduser=int(id_dict["userid"])):
        await message.answer('Номер этажа изменен:' + str(numfl))
    if s.UPDATE(pf=3, valuewhere=id_dict["name"], iduser=int(id_dict["userid"])):
        await message.answer('Номер квартиры изменен:' + message.text)
    await state.clear()
    sqls = s.SELECT(pf=4, valuewhere=int(id_dict["userid"]))
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=4, valuewhere=int(id_dict["userid"])):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n',
                                  reply_markup=keyboard_start
                                 )
        id_dict.clear()
    else:
        await message.answer('С таким номером человека в базе нет')

@router.message(StateFilter(FSMFormEd.feditkv))
async def anceta_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Некорректный номер квартиры, введите заново:')
    await state.set_state(FSMFormEd.feditkv)

@router.callback_query(Text(text='editavto'))
async def anceta_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(userid=callback.message.text)
    await callback.message.answer('Введите номер авто:')
    await state.set_state(FSMFormEd.feditavto)

@router.message(StateFilter(FSMFormEd.feditavto),IsNameButton())
async def anceta_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    id_dict = await state.get_data()
    s = SQL()
    if s.UPDATE(pf=5, valuewhere=id_dict["name"], iduser=int(id_dict["userid"])):
        await message.answer('Номер авто изменен:' + message.text)
        await state.clear()
    sqls = s.SELECT(pf=4, valuewhere=int(id_dict["userid"]))
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=4, valuewhere=int(id_dict["userid"])):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n',
                                  reply_markup=keyboard_start
                                 )
        id_dict.clear()
    else:
        await message.answer('С таким номером человека в базе нет')


@router.callback_query(Text(text='editphone'))
async def anceta_edit(callback: CallbackQuery, state: FSMContext):
    await state.update_data(userid=callback.message.text)
    await callback.message.answer('Введите номер телефона:')
    await state.set_state(FSMFormEd.feditphone)

@router.message(StateFilter(FSMFormEd.feditphone),IsNameButton())
async def anceta_edit(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    id_dict = await state.get_data()
    s = SQL()
    if s.UPDATE(pf=2, valuewhere=id_dict["name"], iduser=int(id_dict["userid"])):
        await message.answer('Номер телефона изменен:' + message.text)
        await state.clear()
    sqls = s.SELECT(pf=4, valuewhere=int(id_dict["userid"]))
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf=4, valuewhere=int(id_dict["userid"])):
            await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                                      f'Телефон: {row.NPHONE} \n'                                  
                                      f'Подъезд: {row.NUMPD} \n'
                                      f'Этаж: {row.NUMFL} \n'
                                      f'Квартира: {row.NUMKV} \n'
                                      f'Номер авто: {row.NUMAUTO} \n'
                                      f'Логин в ТГ: @{row.LoginTG if row.LoginTG is not None else ""} \n',
                                  reply_markup=keyboard_start
                                 )
        id_dict.clear()
    else:
        await message.answer('С таким номером человека в базе нет')

""""
Вывод списка незарегистрированных
"""

@router.message(Text(text='Незарегистрированные'))
async def get_member(message: Message):
    chat_members = await get_chat_members(int(config.groupid.GroupIDStr))
    s = SQL()
    s.DELETEMEMBERS()
    for memberid, membername in chat_members.items():
        s.INSERT_MEMBERS(
            user_id=memberid,
            user_name=membername
        )
    await message.answer(text=f'Всего незарегистрированных в чате: {s.SELECT_REP(pf=1)} \n'
                              f'Данные не подтвердили: {s.SELECT_REP(pf=2)} \n'
                              f'Данных нет, нужна регистрация: {s.SELECT_REP(pf=3)}')
    #for memberid, membername in chat_members.items():
    #    if s.SELECT_REP(pf = 1,valuewhere=memberid):
    #        await message.answer(text=f"<a href='tg://user?id={memberid}'>{membername}</a>",parse_mode="html")


@router.message(Text(text='Исправить номера авто'))
async def edit_numberauto(message: Message):
    s = SQL()
    sqls = s.SELECT(pf = 7, valuewhere="")
    rw = sqls.fetchone()
    if rw is not None:
        for row in s.SELECT(pf = 7, valuewhere=""):
            autonumber = lowertext(row.NUMAUTO)
            s.UPDATE(pf = 5, valuewhere=autonumber,iduser=row.User_id)
    await message.answer("Всё ок")