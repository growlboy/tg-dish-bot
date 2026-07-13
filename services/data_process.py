import logging

logger = logging.getLogger(__name__)

async def PlusCallories(prompt, tg_id, db, ai):
    answer = await ai.count_callories_request(prompt)

    if answer[0] != None:
        if answer[0].isdigit():
            new_cal = int(answer[0])
            today_cal = await db.PlusTodayCal(tg_id, new_cal)

            if today_cal:
                return str(new_cal), str(today_cal)
            else:
                logger.info(f"Database error.")
        else:
            logger.info(f"AI give not digit. Trying again.")
            return PlusCallories(prompt, tg_id, db, ai)
    else:
        logger.info(f"Error: {answer[1]}.")


async def IsRegister(tg_id, db):
    try:
        if await db.CheckRegister(tg_id) and await db.IsHaveRealname(tg_id):
            return True
        else:
            return False
    except:
        logger.info(f"Database error.")


async def GetDayAllow(prompt, tg_id, db, ai):
    try:
        answer = await ai.day_allow_request(prompt)

        if answer[0] != None:
            if answer[0].isdigit():
                new_allow = int(answer[0])
                allow = await db.SetNewDailyAllow(tg_id, new_allow)

                if allow:
                    return str(allow)
                else:
                    logger.info(f"Database error.")
            else:
                logger.info(f"AI give not digit. Trying again.")
        else:
            logger.info(f"Error: {answer[1]}.")

    except Exception as error:
        print(error)
