from templates.config import conn
cur = conn.cursor()
def is_null(username,password):
	if(username==''or password==''):
		return True
	else:
		return False
def is_existed(username,password):
	sql="SELECT * FROM user WHERE username ='%s' and password ='%s'" %(username,password)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def exist_user(username):
	sql = "SELECT * FROM user WHERE username ='%s'" % (username)
	conn.ping(reconnect=True)
	cur.execute(sql)
	conn.commit()
	result = cur.fetchall()
	if (len(result) == 0):
		return False
	else:
		return True

def is_admin(username):
    try:
        sql = "SELECT is_root FROM user WHERE username ='%s'" % (username)
        conn.ping(reconnect=True)
        cur.execute(sql)
        conn.commit()
        result = cur.fetchall()
        if len(result) == 0:
            print("User does not exist.")
            return False
        else:
            is_root = result[0][0]
            print("is_root:", is_root)
            return is_root == 1
    except Exception as e:
        print("Error:", e)
        return False

