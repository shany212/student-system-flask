from templates.config import conn
cur = conn.cursor()

def insert_grade(student_id, course_id, grade):
    sql = "INSERT INTO stu(kch, id, point) VALUES (%s, %s, %s)"
    conn.ping(reconnect=True)
    cur.execute(sql, (course_id, student_id, grade))
    conn.commit()
    conn.close()
