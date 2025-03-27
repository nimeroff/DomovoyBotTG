from sqlalchemy import create_engine, MetaData, Table, String, INTEGER, Column, Text, DATETIME, Boolean, ForeignKey
from datetime import datetime

#from ConfigData.config import Config, load_config
#config: Config = load_config()

engine = create_engine('sqlite:///DOM.db')
engine.connect()
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('ID', INTEGER(), unique=True, primary_key=True),
    Column('User_id', INTEGER(), unique=True,  nullable=False),
    Column('User_name', Text(), nullable=False),
    Column('LoginTG', Text(), nullable=True),
    Column('NAMEDB', Text(), nullable=True),
    Column('FIOS', Text(), nullable=True),

    Column('NPHONE', String(10), nullable=True),
    Column('NUMPD', INTEGER(), nullable=True),
    Column('NUMFL', INTEGER(), nullable=True),
    Column('NUMKV', INTEGER(), nullable=True),
    Column('NUMAUTO', String(9), nullable=True),
    Column('REGFLAG', Boolean(), default=True),
    Column('OWNER', Boolean(), default=True),
    Column('Create_user', DATETIME(), default=datetime.now()),
    Column('Adm', Boolean(), default=False)
);

user_members = Table(
    'user_members',
    metadata,
    Column('ID', INTEGER(), unique=True, primary_key=True),
    Column('User_id', INTEGER(), unique=True,  nullable=False),
    Column('User_name', Text(), nullable=True)
);


metadata.create_all(engine)
