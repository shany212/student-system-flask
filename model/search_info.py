from templates.config import conn
cur = conn.cursor()

def search_by_id(stuid):
    sql="SELECT * FROM stu WHERE id ='%s' " %(stuid)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    print("学号")
    print(result)
    return result

def search_by_kch(stukch):
    sql="SELECT * FROM stu WHERE kch ='%s' " %(stukch)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    print("课程号")
    print(result)
    return result