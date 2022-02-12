import sqlite3
from datetime import datetime


class Database(object):

    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.sqlite_create_db()
        self.initial_setup()

    def commit(self):
        self.con.commit()

    def sqlite_create_db(self):
        # Для значений, который пользователь может выбирать из списка, но не создавать сам
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS maps(
                map TEXT NOT NULL PRIMARY KEY
            ) 
            """)

    def initial_setup(self):
        self.fill_default()

        self.commit()

    def fill_default(self):
        # self.cur.execute(
        #     """
        #     INSERT OR IGNORE INTO
        #         limited_values
        #     VALUES
        #         ("lang", "ru"),
        #         ("lang", "en")
        #     """)
        pass

    # def get_common_setting(self, key):
    #     """Возвращает настройку по ключу.
    #     Если настройка не найдена, возвращает None.
    #     """
    #
    #     self.cur.execute(
    #         f"""
    #         SELECT
    #             value
    #         FROM
    #             common_settings
    #         WHERE
    #             key = "{key}"
    #         """)
    #
    #     try:
    #         return self.cur.fetchone()["value"]
    #     except TypeError:
    #         return None

    def get_maps(self):
        request = f"""
                SELECT
                    maps.map
                FROM
                    maps
                """

        self.cur.execute(request)

        return [row[0] for row in self.cur.fetchall()]

    def add_map(self, map_name):
        self.cur.execute(
            f"""
            INSERT OR IGNORE INTO
                maps
            VALUES
                ("{map_name}")
            """)
        self.commit()


db = Database()
