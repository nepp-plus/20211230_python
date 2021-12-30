import pymysql
from time import sleep
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
    
    print('회원가입이 완료되었습니다. 메인화면으로 돌아갑니다.')
    sleep(2)
    
# 로그인 (sign in) 기능
# 아이디 / 비번을 입력받아서 => DB에 정보가 맞는 회원이 있는지 검색.
# True / False로 결과도 리턴.
def sign_in():
    input_email = input('이메일 : ')
    input_pw = input('비밀번호 : ')
    
    # 아이디와 / 비밀번호가 맞는 회원이 있는가? 조회 SELECT 쿼리.
    sql = f"SELECT * FROM users WHERE users.email = '{input_email}' AND users.password = '{input_pw}'"
    
    # 조회 쿼리 실행
    cursor.execute(sql)
    
    # cursor에는 실행 결과가 표로 담겨있다. => tuple로 변환.
    user_list = cursor.fetchall()
    
    # 로그인 성공? 실패? 판별 기준 => user_list의 갯수가 0개 : 실패.
    if len(user_list) == 0:
        print('잘못된 회원 정보입니다. 다시 로그인 해주세요.')
        sleep(2)
        return False
    else:
        # 아이디/비번 일치 회원 발견. => 성공
        # user_list => 0번쨰 아이템 : 로그인에 성공한 사람 정보.
        
        login_user = user_list[0] # 최소한, 0번째는 있을것이다.
        # print(login_user)  # 로그인 사용자 정보를 => 모든 항목들을 tuple로 묶어서 들고있다.
        user_nickname = login_user[3]  # 사용자 정보 tuple => 닉네임을 추출.
        
        print(f'{user_nickname}님, 환영합니다!')  # 로그인에 성공한 사람의 닉네임이 뭔지?
        sleep(2)
        
        return True
    
    
# 로그인 이후의 기능 메뉴
def print_phone_book_menu():
    print('===== 메인메뉴 =====')
    print('1. 전화번호 추가 등록')
    print('2. 전화목록 목록 조회')
    print('0. 로그아웃')
    print('===================')
    num = int( input('메뉴 선택 : ') )
    return num