from pymysql import connect
import sys
sys.path.append("C:\dev")
from HP_config import HP
import time

class HELPER:
    def __init__(self) -> None:
        self.conn = None
        self.cur = None

    def connect(self):
        while True:
            try:
                self.conn = connect(host=HP.host,
                                    user=HP.user,
                                    password=HP.pwd,
                                    db=HP.db)
                self.cur = self.conn.cursor()
                print('DB connected')
                break
            except Exception as e:
                time.sleep(0.5)
                print(e)

    def close(self):
        self.cur.close()
        self.conn.close()

    def execute(self, sql):
        self.connect()
        self.cur.execute(sql)
        self.conn.commit()
        self.close()

    def fetch(self, sql):
        self.connect()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.close()
        return result

    def fetch_one(self, sql):
        self.connect()
        self.cur.execute(sql)
        result = self.cur.fetchone()
        self.close()
        return result
