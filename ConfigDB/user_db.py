from sqlalchemy import insert, update, delete, select, column, func, label, values
from sqlalchemy.orm import Session
from ConfigDB.BaseModul import engine, users, user_members
import sqlite3

class SQL:
    session = Session(engine)

    def INSERT(self, user_id: int, user_name: str, logintg: str='', namedb: str='', fios: str='', nphone: int=0, numpd: int=0, numfl: int=0, numkv: int=0, numauto: int=0, regflag: bool = True,owner: bool = True, adm: bool = False):
        """
        Добавляем пользователя в БД

        """

        ins  = insert(users).values(
                User_id=user_id,
                User_name = user_name,
                LoginTG = logintg,
                NAMEDB = namedb,
                FIOS = fios,
                NPHONE = nphone,
                NUMPD = numpd,
                NUMFL = numfl,
                NUMKV = numkv,
                NUMAUTO = numauto,
                REGFLAG = regflag,
                OWNER = owner,
                Adm = adm
               )
        self.session.execute(ins)
        self.session.commit()


    def INSERT_MEMBERS(self, user_id: int, user_name: str):
        """
        Добавляем пользователя в БД
        """
        ins  = insert(user_members).values(
                User_id=user_id,
                User_name = user_name
               )
        self.session.execute(ins)
        self.session.commit()

    def USERADM(self, user_id: int):
        """
        Проверяем админ или нет
        """
        # Проверяем зарегистрированных - админ или пользователь
        query = select(func.count((users.c.User_id)).label("RowCount")).select_from(users).where(users.c.User_id == user_id, users.c.Adm == True)
        result = self.session.execute(query)
        for row in result:
            if int(row.RowCount) > 0:
                return True
            else:
                return False

    def EXISTUSER(self, user_id: int, reg: bool):
        """
        Проверяем наличие пользователя В базе
        """
        # Проверяем зарегистрированных - админ или пользователь
        if reg == True:
            query = select(func.count((users.c.User_id)).label("RowCount")).select_from(users).where(users.c.User_id == user_id, users.c.REGFLAG == True)
        else:
            #Проверяем жителей, кто отправил свои данные для регистрации на подтверждение администратору
            query = select(func.count((users.c.User_id)).label("RowCount")).select_from(users).where(users.c.User_id == user_id, users.c.REGFLAG == False)
        result = self.session.execute(query)
        for row in result:
            if int(row.RowCount) > 0:
                return True
            else:
                return False

    def LISTADMIN(self) -> list:
        """
        Получаем список User_ID админов
        """
        lst = list()
        query = select(users.c.User_id).select_from(users).where(users.c.Adm == True)
        result = self.session.execute(query)
        for row in result:
            lst.append(row.User_id)
        return lst


    def SELECT(self,pf: int, valuewhere: str | int):
        """
        Выборка для поиска
        """

        #c.namedb,users.c.namedb,users.c.logintg,users.c.nphone,users.c.numpd,users.c.numfl,users.c.numkv,users.c.numauto
        if pf == 1:
            #query = select(users).select_from(users).where(users.c.NAMEDB == valuewhere or users.c.User_name == valuewhere)
            #query = select(users).select_from(users).where(users.c.User_name.like('%' + valuewhere.lower() + '%') |  users.c.NAMEDB.like('%' + valuewhere.lower() + '%'))
            query = select(users).select_from(users).where(users.c.User_name.contains(valuewhere.lower()) |  users.c.NAMEDB.contains(valuewhere.lower()), users.c.REGFLAG == True)
        if pf == 2:
            query = select(users).select_from(users).where(users.c.NPHONE.contains(valuewhere), users.c.REGFLAG == True)
        if pf == 3:
            query = select(users).select_from(users).where(users.c.NUMKV == valuewhere, users.c.REGFLAG == True)
        if pf == 4:
            query = select(users).select_from(users).where(users.c.User_id == valuewhere, users.c.REGFLAG == True)
        if pf == 5:
            query = select(users).select_from(users).where(users.c.NUMAUTO.like('%' + valuewhere + '%'), users.c.REGFLAG == True)
        if pf == 6:
            query = select(users).select_from(users).where(users.c.User_id == valuewhere) #Для поиска любого юзера, не только зареганных
        if pf == 7:
            query = select(users).select_from(users).where(users.c.NUMAUTO != '', users.c.NUMAUTO != None)
        result = self.session.execute(query)
        return result
        #for row in result:
        #    print(row.User_name)

    def SELECT_REP(self,pf: int):
        """
        Выборка для отчетов
        """
        connection = sqlite3.connect('DOM.db')
        cursor = connection.cursor()
        if pf == 1: # незареганные
            sqlstr = f'SELECT count(*) kol FROM (select a.User_id AS USRID, A.User_name  from user_members a LEFT JOIN users b ON a.User_id = b.User_id WHERE  b.REGFLAG=False AND a.User_name NOT LIKE "%DomovoyFlowerBot%" ' \
                     f'UNION select a.User_id AS USRID, A.User_name from user_members a  LEFT JOIN users b ON a.User_id = b.User_id WHERE b.User_id IS NULL AND a.User_name NOT LIKE "%DomovoyFlowerBot%") a'
        if pf == 2: # незареганные , по которым есть данные в базе
            sqlstr = f'SELECT count(*) kol FROM (select a.User_id AS USRID, A.User_name  from user_members a LEFT JOIN users b ON a.User_id = b.User_id WHERE  b.REGFLAG=False  AND a.User_name NOT LIKE "%DomovoyFlowerBot%") a'
        if pf == 3: # незареганные, по которым нет данных в базе
            sqlstr = f'SELECT count(*) kol FROM (select a.User_id AS USRID, A.User_name from user_members a  LEFT JOIN users b ON a.User_id = b.User_id WHERE b.User_id IS NULL  AND a.User_name NOT LIKE "%DomovoyFlowerBot%") a'
        if pf == 4: # незареганные, по которым нет данных в базе
            sqlstr = f'SELECT ID_USER,NUMAUTO FROM users WHERE REGFLAG=True AND NUMAUTO IS NOT NULL AND NUMAUTO <>""'
        cursor.execute(sqlstr)
        users = cursor.fetchall()
        # Выводим результаты
        for user in users:
            result =  user[0]
        connection.close()
        return result

    def FINDSELECT(self,pf: int, valuewhere: str | int):
        """
        Выборка для поиска
        Тут подсчитываем количестов строк
        """
        #c.namedb,users.c.namedb,users.c.logintg,users.c.nphone,users.c.numpd,users.c.numfl,users.c.numkv,users.c.numauto
        if pf == 1:
            query = select(func.count).select_from(users).where(users.c.User_name.like('%' + valuewhere + '%') |  users.c.NAMEDB.like('%' + valuewhere + '%'))
        if pf == 2:
            query = select(func.count).select_from(users).where(users.c.NPHONE == valuewhere)
        if pf == 3:
            query = select(func.count).select_from(users).where(users.c.NUMKV == valuewhere)
        if pf == 4:
            query = select(func.count).select_from(users).where(users.c.NUMAUTO == valuewhere)
        result = self.session.execute(query)
        return result


    def DELETE(self,pf: int, iduser: int) -> bool:
        try:
            if pf == 1:
                query = delete(users).where(users.c.User_id == iduser)
            self.session.execute(query)
            self.session.commit()
            return True
        except:
            return False

    def DELETEMEMBERS(self) -> bool:
        try:
            query = delete(user_members)
            self.session.execute(query)
            self.session.commit()
            return True
        except:
            return False

    def UPDATE(self,pf:int, valuewhere: str | int,iduser: int) -> bool:
            """
            Обновление строки
            """
            try:
                if pf == 1:
                    query = update(users).values(NAMEDB=valuewhere).where(users.c.User_id == iduser)
                if pf == 2:
                    query = update(users).values(NPHONE=valuewhere).where(users.c.User_id == iduser)
                if pf == 3:
                    query = update(users).values(NUMKV=valuewhere).where(users.c.User_id == iduser)
                if pf == 4:
                    query = update(users).values(REGFLAG=valuewhere).where(users.c.User_id == iduser)
                if pf == 5:
                    query = update(users).values(NUMAUTO=valuewhere).where(users.c.User_id == iduser)
                if pf == 6:
                    query = update(users).values(NUMPD=valuewhere).where(users.c.User_id == iduser)
                if pf == 7:
                    query = update(users).values(NUMFL=valuewhere).where(users.c.User_id == iduser)
                self.session.execute(query)
                self.session.commit()
                return True
            except:
                return False



#if __name__== '__main__':
#    s = SQL()
#    for row in s.SELECT(pf=1,valuewhere='Рустам'):
#        print(row.User_name)

 #   print('--------------')
 #   for row in s.SELECT(2,valuewhere=11):
 #       print(row.User_name)

    #print('--------------')
    #for row in s.SELECT(3,valuewhere=13):
    #    print(row.User_name)
    #print(sql.EXISTUSER(userid="Рустам1"))
