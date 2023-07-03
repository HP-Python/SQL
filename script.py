import pyperclip

def get_clipboard():
    return pyperclip.paste()

def get_database(helper):
    sql = "SELECT PREFIX, ITEM_NAME FROM ITEM_COLLECT"
    return helper.fetch(sql)

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
    print(datas)
    text = reform_database(datas)
    print(text)
    pyperclip.copy(text)

def clipboard_database(helper):
    clip = get_clipboard()
    datas = reform_clipboard(clip)
    helper.connect()
    sql = "INSERT INTO ITEM_COLLECT (PREFIX, ITEM_NAME) VALUES (%s, %s)"
    for row in datas:
        print(row)
    helper.cur.executemany(sql, datas)
    helper.conn.commit()
    helper.close()

if __name__ == "__main__":
    from db import HELPER
    helper = HELPER()
    # clipboard_database(helper)
    database_clipboard(helper)
