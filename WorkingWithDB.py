import sqlite3


db = sqlite3.connect('posts.db')
cur = db.cursor()


class DB():

    def get_channel_lists() -> str:
        res = cur.execute('select*from posts')
        data = res.fetchall()
        m = ''
        for el in data:
            m += f'{el[0]}) @{el[1]}\n'

        return m

    def add_channels(content: str):
        content = content.replace(' ', '')
        arr = content.split(',')

        for i in arr:
            cur.execute(
                f'insert into posts(id,tg_name) values (null, "{i}") ')
        db.commit()

    def delete_channels(content: str):
        content = content.replace(' ', '')
        arr = content.split(',')
        for i in arr:
            cur.execute(f'delete from posts where id = {i} ')
        db.commit()

    def get_chnls():
        res = cur.execute('select*from posts')
        data = res.fetchall()
        arr = []
        for i in range(len(data)):
            arr.append(data[i][1])
        return arr

    def get_admins_list():
        res = cur.execute('select*from admins')
        data = res.fetchall()
        arr = []
        for i in range(len(data)):
            arr.append(data[i][1])
        return arr

    def add_new_admin(id):
        res = cur.execute(f'select*from admins where external_id = "{id}" ')
        data = res.fetchone()
        if data is None:
            cur.execute(
                f'insert into admins(id,external_id) values (null, {id}) ')
            db.commit()
    # def add_new_chat(chat_id, chat_name):
    #     cur.execute(
    #                 f'insert into chats(id,chat_id,chat_name) values (null, "{chat_id}, {chat_name}")')
    #     db.commit()

    def get_all_chats():
        res = cur.execute('select*from chats')
        data = res.fetchall()
        m = ''
        for el in data:
            m += f'{el[0]}) {el[1]}\n'
        return m

    def get_external_id_by_id(id):
        res = cur.execute(f'select*from chats where id = {id}')
        data = res.fetchone()
        return data[0]

    def add_chat(link):
        res = cur.execute(f'select*from chats where chat_link = "{link}" ')
        data = res.fetchone()
        if data is None:
            cur.execute(
                f'insert into chats(id,chat_link) values (null, "{link}") ')
            db.commit()

    def get_all_keywords():
        res = cur.execute('select*from keywords')
        data = res.fetchall()
        m = ''
        for el in data:
            m += f'{el[0]}) {el[1]}\n'
        return m

    def add_new_keyword(content: str):
        arr = content.split(',')
        for word in arr:
            cur.execute(
                f'insert into keywords(id, word) values (null, "{word}") ')
            db.commit()

    def get_all_keywords():
        res = cur.execute('select*from keywords')
        data = res.fetchall()
        m = ''
        for el in data:
            m += f'{el[0]}) {el[1]}\n'
        return m

    def get_keywords_parse():
        res = cur.execute('select*from keywords')
        d = res.fetchall()
        a = []
        for el in d:
            a.append(el[1])
        return a

    def delete_keyword_by_id(content: str):
        content = content.replace(' ', '')
        arr = content.split(',')
        for id in arr:
            cur.execute(
                f'delete from keywords where id ="{id}" ')
            db.commit()
