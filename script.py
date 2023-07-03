import pyperclip

# 从剪贴板导入数据库
# 从数据库导入剪贴板
def get_clipboard():
    return pyperclip.paste()

def get_database(helper):
    sql = "SELECT PREFIX, ITEM_NAME FROM ITEM_COLLECT"
    return helper.fetch(sql)

def get_item_collect(helper):
    sql = "SELECT ITEM_NAME FROM ITEM_COLLECT"
    return [row[0] for row in helper.fetch(sql)]

def reform_clipboard(clip):
    result = []
    prefix = None
    for row in clip.split("\r\n"):
        if row.startswith("+ "):
            prefix = row
            continue
        if row.startswith("- "):
            result.append((prefix, row[2:]))
    return result

def reform_database(datas):
    result = []
    prefix = None
    for row in datas:
        if row[0] != prefix:
            prefix = row[0]
            result.append(row[0])
            result.append("- " + row[1])
        else:
            result.append("- " + row[1])
    return "\n".join(result)

def database_clipboard(helper):
    datas = get_database(helper)
    text = reform_database(datas)
    pyperclip.copy(text)

def database_clipboard_noForm(helper):
    ret = get_item_collect(helper)
    pyperclip.copy("\n".join(ret))

def clipboard_database(helper):
    clip = get_clipboard()
    datas = reform_clipboard(clip)
    helper.connect()
    sql = "DROP TABLE IF EXISTS ITEM_COLLECT"
    helper.cur.execute(sql)
    sql = """
        CREATE TABLE ITEM_COLLECT (
        ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        PREFIX VARCHAR(50) NOT NULL,
        ITEM_NAME VARCHAR(20) NOT NULL);
        """
    helper.cur.execute(sql)
    sql = "INSERT INTO ITEM_COLLECT (PREFIX, ITEM_NAME) VALUES (%s, %s)"
    helper.cur.executemany(sql, datas)
    helper.conn.commit()
    helper.close()

if __name__ == "__main__":
    from db import HELPER
    helper = HELPER()
    database_clipboard_noForm(helper)
