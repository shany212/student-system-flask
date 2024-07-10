from templates.config import conn
cur = conn.cursor()

def updata_by_id(stuid,grade):
    sql = "UPDATE stu SET point = %s WHERE id = %s" %(grade,stuid)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    print(result)
    return result

def updata_by_kch(stukch,grade):
    sql = "UPDATE stu SET point = %s WHERE kch = %s" % (grade, stukch)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    print(result)
    return result