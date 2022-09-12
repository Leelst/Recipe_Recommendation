


def load_db(li):
    conn = pymysql.connect(host='localhost', user='root', password='Lja15410!',db='cp1', charset='utf8')
    cur = conn.cursor()