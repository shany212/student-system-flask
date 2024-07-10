from templates.config import conn
cur = conn.cursor()

def delete_by_id(stuid):
    sql = "DELETE FROM stu WHERE id = %s"%(stuid)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    result = cur.fetchall()
    return result
