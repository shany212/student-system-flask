from templates.config import conn

cur = conn.cursor()

def add_user(username, password):
    sql = "INSERT INTO user(username, password, is_root) VALUES ('%s','%s',%d)" %(username, password, 0)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()
    conn.close()
