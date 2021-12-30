import pymysql
# DB 연결자체는 main.py에서 설정
# 만들어진 연결정보를 받아서 사용해보자.

db_connect = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin',
    passwd='Vmfhwprxm!123',
    db='test_phone_book',
    charset='utf8')


# 쿼리를 날려주는 역할
cursor = db_connect.cursor()


def print_main_menu():
    print('====== 전화번호부 ======')
    print('1. 로그인')
    print('2. 회원가입')
    print('0. 프로그램 종료')
    print('=======================')
    menu_num =  int( input('메뉴 선택 : ') )
    return menu_num

# 회원가입 실행 함수 - DB에 쿼리를 날려주자.
# 회원가입 => users 테이블에, 회원정보가 담긴 row를 추가하자.  INSERT INTO 활용.

def sign_up():
    input_email =  input('가입 이메일 : ')
    input_password = input('사용할 비밀번호 : ')
    input_nickname = input('닉네임 : ')
    
    # INSERT INTO 쿼리의 VALUES에 들어가도록 처리.
    
    # f string으로 실제 입력된 내용을 쿼리에 반영.
    # SQL (쿼리)를 짤때는 'string' 형태로 처리를 해야하는일이 빈번함.
    # f"문장"  형태로, 큰 string은 " " 로 감싸자.
    sql = f"INSERT INTO users (users.email, users.password, users.nickname) VALUES ( '{input_email}', '{input_password}', '{input_nickname}' )"
    
    cursor.execute(sql)
    db_connect.commit()