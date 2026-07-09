-- name: add_user!
INSERT INTO users_maindata (tg_id, username, update_date, today_cal, daily_allow, realname) VALUES 
(:tg_id,:username,CURRENT_DATE,0,0, 'None');

-- name: delete_user!
DELETE FROM users_maindata WHERE tg_id = :tg_id;

-- name: set_realname!
UPDATE users_maindata 
SET realname = :new_name 
WHERE tg_id = :tg_id;

-- name: set_today_cal!
UPDATE users_maindata
SET today_cal = :today_cal
WHERE tg_id = :tg_id

-- name: get_user_date$
SELECT update_date 
FROM users_maindata
WHERE tg_id = :tg_id;

-- name: get_current_date$
SELECT CURRENT_DATE

-- name: plus_cal!
UPDATE users_maindata
SET today_cal = today_cal + :plus_cal
WHERE tg_id = :tg_id

-- name: set_date!
UPDATE users_maindata
SET update_date = CURRENT_DATE
WHERE tg_id = :tg_id

-- name: set_daily_allow!
UPDATE users_maindata
SET daily_allow = :daily_cal
WHERE tg_id = :tg_id

-- name: get_today_cal$
SELECT today_cal 
FROM users_maindata
WHERE tg_id = :tg_id

-- name: get_daily_allow$
SELECT daily_allow
FROM users_maindata
WHERE tg_id = :tg_id

-- name: get_realname$
SELECT realname
FROM users_maindata
WHERE tg_id = :tg_id

-- name: isregister$
SELECT EXISTS (
    SELECT 1
    FROM users_maindata
    WHERE tg_id = :tg_id
)