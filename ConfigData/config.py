from __future__ import annotations
from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str

@dataclass
class Admin:
    Adminstr: str

@dataclass
class GroupID:
    GroupIDStr: str

@dataclass
class ApiI:
    id: str

@dataclass
class ApiH:
    hash: str

@dataclass
class Config:
    tg_bot: TgBot
    adminc: Admin
    groupid: GroupID
    apiid: ApiI
    apihash: ApiH

def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN')),
                  adminc=Admin(Adminstr=env('ADMIN')),
                  groupid=GroupID(GroupIDStr=env('ChatIdProd')),
                  apiid=ApiI(id=env('APIID')),
                  apihash=ApiH(hash=env('APIHASH'))
                  )


podjezd= {1:
    {
        1:[1,3],
        2:[4,11],
        3:[12,20],
        4:[21,29],
        5:[30,38],
        6:[39,47],
    },
    2:
    {
        1:[48,50],
        2:[51,61],
        3:[62,72],
        4:[73,83],
        5:[84,94],
        6:[95,105],
        7:[106,116]
    },
    3:
    {
        1:[117,122],
        2:[123,131],
        3:[132,140],
        4:[141,149],
        5:[150,158],
        6:[159,167],
        7:[168,176],
        8:[177,185]
    },
    4:
    {
        1:[186,187],
        2:[188,192],
        3:[193,197],
        4:[198,202],
        5:[203,207],
        6:[208,212],
        7:[213,217],
        8:[218,222]
    },
    5:
    {
        1:[223,224],
        2:[225,229],
        3:[230,234],
        4:[235,239],
        5:[240,244],
        6:[245,249],
        7:[250,254],
        8:[255,259]
    },
    6:
    {
        1:[260,267],
        2:[268,278],
        3:[279,289],
        4:[290,300],
        5:[301,311],
        6:[312,322],
        7:[323,333]
    },
    7:
    {
        1:[334,341],
        2:[342,352],
        3:[353,363],
        4:[364,374],
        5:[375,385],
        6:[386,396]
    },
    8:
    {
        2:[397,402],
        3:[403,408],
        4:[409,414],
        5:[415,420],
        6:[421,426]
    }
}