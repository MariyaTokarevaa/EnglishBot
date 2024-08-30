
import psycopg2 as psycopg2
import random

from config import bot, db_connection
from telebot.types import Message


def hello(message: Message, cid):
    with psycopg2.connect(db_connection) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT telegram_id FROM users;""")
            users_list = cur.fetchall()
            if any(cid in user for user in users_list):
                bot.send_message(cid, f"С возвращением, {message.from_user.first_name}."
                                      f" Давай продолжим!")
            else:
                bot.send_message(cid, f"Привет {message.from_user.first_name}, я вижу, ты у нас впервые!"
                                      f"Сейчас я тебя зарегистрирую и начнем учить слова!")
                cur.execute("""INSERT INTO users (telegram_id) 
                            VALUES(%s) returning id""", [cid])

                insert_id = cur.fetchone()[0]
                cur.executemany("""INSERT INTO userword(telegram_id, word_id) 
                                VALUES (%s, %s)""", [
                    (insert_id, 1), (insert_id, 2), (insert_id, 3),
                    (insert_id, 4), (insert_id, 5), (insert_id, 6),
                    (insert_id, 7), (insert_id, 8), (insert_id, 9),
                    (insert_id, 10)

                ])
                conn.commit()


def add_new_word(message: Message):
    cid = message.chat.id
    if ' ' not in message.text:
        bot.send_message(chat_id=cid, text=f'Что-то я тебя не понимаю, повтори еще раз')
        return
    if message.text.split()[0].isalpha() and message.text.split()[1].isalpha():
        english = message.text.split()[0].capitalize()
        russian = message.text.split()[1].capitalize()
        with psycopg2.connect(db_connection) as conn:
            with conn.cursor() as cur:
                cur.execute("""SELECT id FROM users WHERE telegram_id = %s;""", [cid])
                u_id = cur.fetchone()
                cur.execute("""SELECT english FROM words;""")
                words = cur.fetchall()
                dict_res = []
                for word in words:
                    dict_res.append(word[0])
                if english not in dict_res:
                    cur.execute("""INSERT INTO words (english, russian) 
                                VALUES (%s, %s) returning id;""",
                                (english, russian))
                    insert_id = cur.fetchone()[0]
                    cur.execute("""INSERT INTO userword (word_id, telegram_id) 
                                VALUES(%s, %s);""", (insert_id, u_id[0]))
                    cur.execute("""SELECT COUNT(*) 
                                FROM userword u 
                                JOIN users u2 on u.telegram_id = u2.id
                                WHERE u2.telegram_id = %s;""", [cid])
                    num_of_word = cur.fetchone()[0]
                    log_message = (f'Пара {english} - {russian} добавлена в словарь. Теперь в вашем словаре '
                                   f'{num_of_word} слов')
                else:
                    cur.execute("""SELECT english, russian 
                                FROM userword u 
                                JOIN users u2 on u.telegram_id = u2.id
                                JOIN words w on u.word_id = w.id
                                WHERE u2.telegram_id = '%s'""", [cid])
                    userwords_list = cur.fetchall()
                    dict_res = []
                    for word in userwords_list:
                        dict_res.append(word[0])
                    if english not in dict_res:
                        cur.execute("""SELECT id 
                                    FROM words 
                                    WHERE english = %s;""", [english])
                        dict_id = cur.fetchone()[0]
                        cur.execute("""INSERT INTO  userword (word_id, telegram_id) 
                                    VALUES (%s, %s);""", (dict_id, u_id[0]))
                        cur.execute("""SELECT COUNT(*) 
                                    FROM userword u 
                                    JOIN users u2 on u.telegram_id = u2.id
                                    WHERE u2.telegram_id = %s;""", [cid])
                        num_of_word = cur.fetchone()[0]
                        log_message = (f'Пара {english} - {russian} добавлена в словарь. Теперь в вашем словаре'
                                       f'{num_of_word} слов')
                    else:
                        log_message = f' Пара {english} - {russian} уже присутствует в вашем словаре'
                conn.commit()
            bot.send_message(chat_id=cid, text=log_message)
    else:
        bot.send_message(chat_id=cid, text=f'Что-то я тебя не понимаю, повтори еще раз')


def delete_from_userword(cid, targetword):
    with psycopg2.connect(db_connection) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT u.id, english, russian 
                        FROM userword u 
                        JOIN users u2 on u.telegram_id = u2.id
                        JOIN words d on u.word_id = d.id
                        WHERE u2.telegram_id = %s AND english = %s;""", (cid, targetword))
            userwords_list = cur.fetchall()
            cur.execute("""DELETE FROM userword WHERE id = %s; """, [userwords_list[0][0]])
            log_message = f'Пара {userwords_list[0][1]} - {userwords_list[0][2]} успешно удалена из вашего словаря'
            bot.send_message(chat_id=cid, text=log_message)
        conn.commit()


def get_user_words(cid):
    with psycopg2.connect(db_connection) as conn:
        with conn.cursor() as cur:
            cur.execute("""SELECT english, russian 
                        FROM userword u
                        JOIN users u2 on u.telegram_id = u2.id
                        JOIN words w on u.word_id = w.id
                        WHERE u2.telegram_id = '%s'
                        ORDER BY RANDOM() LIMIT 4;""", [cid])
            all_words = cur.fetchall()
            target_list = all_words[0]
            owner_list = all_words[1:]
            owner_word_list = [owner_list[0][0], owner_list[1][0], owner_list[2][0]]
    conn.commit()
    return target_list, owner_word_list
