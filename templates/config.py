#数据库连接配置
import pymysql

conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='wuxian120',
        database='datadb'
    )
