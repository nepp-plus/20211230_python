# DB 연결자체는 main.py에서 설정
# 만들어진 연결정보를 받아서 사용해보자.

db_connect = None

# 쿼리를 날려주는 역할
cursor = None

def set_db_info(connect):
    # db_connect라는 비어있는 변수에 연결정보 대입.
    db_connect = connect
    cursor = db_connect.cursor()