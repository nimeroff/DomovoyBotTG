from aiogram import Router, F, Bot, types
from aiogram.types import ChatMemberRestricted, ChatMemberMember, ChatMemberAdministrator
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from Keyboards.keyboards import create_key, create_inline_key
from Lexicon.lexicon_ru import LEXICON_MENU, LEXICON_INLINE_FIND, LEXICON_EDITPROFILE
from ConfigDB.user_db import SQL
from ConfigData.config import podjezd, Config, load_config
from Filters.filters import IsRegistration, IsNameButton,IsGroupMess,IsChatMember, LenNumPhone

router: Router = Router()
router.message.filter(IsRegistration(),IsGroupMess(),IsChatMember())

keyboard_work = create_key(2, **LEXICON_MENU)
keyboard_inline_find = create_inline_key(1, **LEXICON_INLINE_FIND)
keyboard_edit = create_key(1, **LEXICON_EDITPROFILE)

#Создаем базу данных пользователей
user_dict: dict[int, dict[str, str | int | bool]] = {}

pod_dict: dict[str, str] = {}
fl_dict: dict[str, str] = {}
kv_dict: dict[str, str] = {}

class FSMFormEdit(StatesGroup):
    fedit_name = State()
    fedit_phone = State()
    fedit_kv = State()
    fedit_auto = State()

class FSMFormSearch(StatesGroup):
    ffind_name = State()
    ffind_phone = State()
    ffind_kv = State()
    ffind_auto = State()

class FSMFormDict(StatesGroup):
    fdict_pod = State()
    fdict_fl = State()
    fdict_kv = State()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Вы зарегистрированы, с чего начнём?', reply_markup=keyboard_work)

# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
# ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК ПОИСК
@router.message(Text(text='Поиск'))
async def anceta_find(message: Message):
    await message.answer('Как будем искать?', reply_markup=keyboard_inline_find)

@router.callback_query(F.data.in_(['findname']))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Укажите имя для поиска:')
    await state.set_state(FSMFormSearch.ffind_name)

@router.message(StateFilter(FSMFormSearch.ffind_name),IsNameButton())
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

    else:
        await message.answer('С таким именем человека в базе нет')


@router.callback_query(Text(text='findphone'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер телефона полностью через +7, либо часть:')
    await state.set_state(FSMFormSearch.ffind_phone)

@router.message(StateFilter(FSMFormSearch.ffind_phone),IsNameButton())
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
    else:
        await message.answer('С таким номером человека в базе нет')


@router.callback_query(Text(text='findkv'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите номер квартиры')
    await state.set_state(FSMFormSearch.ffind_kv)


@router.message(StateFilter(FSMFormSearch.ffind_kv),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введеннОе значение для поискв
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
    else:
        await message.answer('В этой квартире никто не зарегистрирован')

@router.callback_query(Text(text='findauto'))
async def anceta_find(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите полностью или часть номера авто')
    await state.set_state(FSMFormSearch.ffind_auto)

@router.message(StateFilter(FSMFormSearch.ffind_auto),IsNameButton())
async def anceta_find(message: Message, state: FSMContext):
    # Сохраняем введенное значение для поискв
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
    else:
        await message.answer('Нет данных по этому авто')

# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник
# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник
# Справочник * Справочник *  Справочник *  Справочник * Справочник *  Справочник * Справочник
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
    await state.set_state(FSMFormDict.fdict_pod)


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


@router.callback_query(FSMFormDict.fdict_pod)
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
    await state.set_state(FSMFormDict.fdict_fl)

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


@router.callback_query(FSMFormDict.fdict_fl)
async def dictionary_start(Callback: CallbackQuery, state: FSMContext):
    if fl_backshow(str(Callback.data)) == False:
        createdictkv(str(Callback.data))
        keyboard_inline_dict = create_inline_key(7, **kv_dict)
        await Callback.message.edit_text('Квартиры:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormDict.fdict_kv)
    elif fl_backshow(str(Callback.data)) == True:
        keyboard_inline_dict = create_inline_key(1, **pod_dict)
        await Callback.message.edit_text('Подъезды:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormDict.fdict_pod)



def kv_backshow(pflk: str):
    if pflk[4:8] == 'back':
        return True
    elif pflk[4:8] == 'kvkv':
        return False


@router.callback_query(FSMFormDict.fdict_kv)
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
        await state.set_state(FSMFormDict.fdict_kv)
    elif kv_backshow(str(Callback.data)) == True:
        keyboard_inline_dict = create_inline_key(1, **fl_dict)
        await Callback.message.edit_text('Этажи:', reply_markup=keyboard_inline_dict)
        await state.set_state(FSMFormDict.fdict_fl)


# Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование
# Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование
# Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование
# Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование #Редактирование Редактирование

@router.message(Text(text='Редактировать профиль'))
async def anceta_edit(message: Message):
    await message.answer('Что меняем?', reply_markup=keyboard_edit)

@router.message(Text(text='Назад в главное меню'))
async def anceta_edit(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Возврат в главное меню', reply_markup=keyboard_work)

@router.message(Text(text='Изменить имя'))
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    for row in s.SELECT(pf=4, valuewhere=message.from_user.id):
        nameuser = row.NAMEDB
    await message.answer(f'Ваше текущее имя: {nameuser}.\n Новое имя:')
    await state.set_state(FSMFormEdit.fedit_name)

@router.message(StateFilter(FSMFormEdit.fedit_name), IsNameButton())
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    if s.UPDATE(pf=1, valuewhere=message.text, iduser=message.from_user.id):
        await message.answer('Имя изменено:' + message.text)
        await state.clear()
    else:
        await message.answer('Что-то пошло не так:' + message.text)


@router.message(Text(text='Изменить телефон'))
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    for row in s.SELECT(pf=4, valuewhere=message.from_user.id):
        nameuser = row.NPHONE
    await message.answer(f'Текущий номер: {nameuser}.\n Введите новый, в формате XXX***XX**, всего 10 цифр:')
    await state.set_state(FSMFormEdit.fedit_phone)


@router.message(StateFilter(FSMFormEdit.fedit_phone), F.text.isdigit(), LenNumPhone())
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    if s.UPDATE(pf=2, valuewhere='+7' + message.text, iduser=message.from_user.id):
        await message.answer('Номер телефона изменен: +7' + message.text)
        await state.clear()
    else:
        await message.answer('Что-то пошло не так:' + message.text)

@router.message(StateFilter(FSMFormEdit.fedit_phone))
async def anceta_edit(message: Message, state: FSMContext):
    await message.answer('Введите цифрами в формате XXX***XX**, всего 10 цифр:')
    await state.set_state(FSMFormEdit.fedit_phone)


@router.message(Text(text='Изменить номер квартиры'))
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    for row in s.SELECT(pf=4, valuewhere=message.from_user.id):
        nameuser = row.NUMKV
    await message.answer(f'Ваш текущий номер квартиры: {nameuser}.\n Новый номер квартиры:')
    await state.set_state(FSMFormEdit.fedit_kv)



@router.message(StateFilter(FSMFormEdit.fedit_kv), F.text.isdigit())
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    if s.UPDATE(pf=3, valuewhere=message.text, iduser=message.from_user.id):
        await message.answer('Номер квартиры изменен:' + message.text)
        await state.clear()
    else:
        await message.answer('Что-то пошло не так:' + message.text)

@router.message(Text(text='Изменить номер авто'))
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    for row in s.SELECT(pf=4, valuewhere=message.from_user.id):
        nameuser = row.NUMAUTO
    await message.answer(f'Ваш текущий номер авто: {nameuser}.\n Новый номер авто:')
    await state.set_state(FSMFormEdit.fedit_auto)

@router.message(StateFilter(FSMFormEdit.fedit_auto), IsNameButton())
async def anceta_edit(message: Message, state: FSMContext):
    s = SQL()
    if s.UPDATE(pf=5, valuewhere=message.text, iduser=message.from_user.id):
        await message.answer('Номер авто изменен:' + message.text)
        await state.clear()
    else:
        await message.answer('Что-то пошло не так:' + message.text)

@router.message(Text(text='Профиль'))
async def anceta_edit(message: Message):
    s = SQL()
    for row in s.SELECT(pf=4, valuewhere=message.from_user.id):
        await message.answer(text=f'Имя в базе: {row.NAMEDB} \n'
                            f'Телефон: {row.NPHONE} \n'
                            f'Подъезд: {row.NUMPD} \n'
                            f'Этаж: {row.NUMFL} \n'
                            f'Квартира: {row.NUMKV} \n'
                            f'Номер авто: {row.NUMAUTO} \n'
                       )