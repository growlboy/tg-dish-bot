import aiosql
import datetime

class DataBaseManager:
    def __init__(self, pool):
        self.pool = pool
        self.queries = aiosql.from_path("queries.sql", "asyncpg", mandatory_parameters=False)

    async def __get_daily_allow(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                get_daily_allow = await self.queries.get_daily_allow(conn, tg_id=tg_id)
                return get_daily_allow
        except Exception as error:
            return "Error with getting"

    async def __get_today_cal(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                today_cal = await self.queries.get_today_cal(conn, tg_id=tg_id)
                return today_cal
        except Exception as error:
            return "Error with getting"

    async def __set_daily_allow(self, tg_id, daily_cal):
        try:
            async with self.pool.acquire() as conn:
                await self.queries.set_daily_allow(conn, tg_id=tg_id, daily_cal=daily_cal)
        except Exception as error:
            print("Error in __set_daily_allow", error)

    async def __plus_today_cal(self, tg_id, plus_cal):
        try:
            await self.__check_today_date(tg_id)

            async with self.pool.acquire() as conn:
                await self.queries.plus_cal(conn, tg_id=tg_id, plus_cal = plus_cal)
        except Exception as error:
            print("Error in __plus_today_cal", error)

    async def __set_today_cal(self, tg_id, new_cal):
        try:
            async with self.pool.acquire() as conn:
                await self.queries.set_today_cal(conn, tg_id=tg_id, today_cal = new_cal)
        except Exception as error:
            print("Error in __set_today_cal", error)
        
    async def AddUser(self, tg_id, username):
        try:
            async with self.pool.acquire() as conn:
                await self.queries.add_user(conn, tg_id=tg_id, username=username)
        except Exception as error:
            print("Error in AddUser", error)

    async def __delete_user(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                await self.queries.delete_user(conn, tg_id=tg_id)
        except Exception as error:
            print("Error in __delete_user", error)

    async def __set_realname(self, tg_id, name):
        try:
            async with self.pool.acquire() as conn:
                await self.queries.set_realname(conn, tg_id=tg_id, new_name=name)
        except Exception as error:
            print("Error in __set_realname", error)
     
    async def __get_realname(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                realname = await self.queries.get_realname(conn, tg_id=tg_id)
                return realname
        except Exception as error:
            print("Error in __get_realname", error)

    async def __check_today_date(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                last_date: datetime.date = await self.queries.get_user_date(conn, tg_id = tg_id)
                today_date: datetime.date = await self.queries.get_current_date(conn)

                if last_date != today_date:
                    await self.__set_today_cal(tg_id, 0)

                await self.queries.set_date(conn, tg_id=tg_id)
        except Exception as error:
            print("Error in __check_today_date", error)

    async def __is_register(self, tg_id):
        try:
            async with self.pool.acquire() as conn:
                return await self.queries.isregister(conn, tg_id=tg_id)
        except Exception as error:
             print("Error in __is_register", error)


    async def PlusTodayCal(self, tg_id, plus_cal):
        await self.__plus_today_cal(tg_id, plus_cal)
        return await self.__get_today_cal(tg_id)
    
    async def GetTodayCal(self, tg_id):
        return await self.__get_today_cal(tg_id)
    
    async def SetNewDailyAllow(self, tg_id, daily_allow):
        await self.__set_daily_allow(tg_id, daily_allow)
        return await self.__get_daily_allow(tg_id)
    
    async def GetDailyAllow(self, tg_id):
        return await self.__get_daily_allow(tg_id)

    async def SetRealname(self, tg_id, realname):
        await self.__set_realname(tg_id, realname)
        return await self.__get_realname(tg_id)
    
    async def GetRealname(self, tg_id):
        return await self.__get_realname(tg_id)
    
    async def CheckRegister(self, tg_id):
        return await self.__is_register(tg_id)
    
    async def IsHaveRealname(self, tg_id):
        if await self.GetRealname(tg_id) == 'None':
            return False
        else:
            return True