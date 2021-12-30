import pymysql
from time import sleep
from datas import Contact

# DB 연결자체는 main.py에서 설정
# 만들어진 연결정보를 받아서 사용해보자.

db_connect = pymysql.connect(
    host='finalproject.cbqjwimiu76h.ap-northeast-2.rds.amazonaws.com', 
    port=3306, 
    user='admin',
    passwd='Vmfhwprxm!123',
    db='test_phone_book',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)  # SELECT의 결과를, tuple이 아니라, dict 형태로 가져오도록.


# 쿼리를 날려주는 역할
cursor = db_connect.cursor()

# 로그인한 사용자가 몇번사용자인지 변수로 저장.
login_user_id = 0  # 임시로 0으로 초기화.


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
        print(login_user)  # 로그인 사용자 정보를 => 모든 항목들을 dict로 묶어서 들고있다.
        user_nickname = login_user['nickname']  # 사용자 정보 tuple => 닉네임을 추출.
        
        global login_user_id  # 최상단에서 만든 login_user_id 변수를 끌어와서 사용하겠다고 명시.
        login_user_id = login_user['id']  # 로그인한사용자 (내가)  몇번 id를 가지고 있는지 추출.
        
        print(f'{user_nickname}님, 환영합니다!')  # 로그인에 성공한 사람의 닉네임이 뭔지?
        sleep(2)
        
        return True
    
    
# 로그인 이후의 기능 메뉴
def print_phone_book_menu():
    print('===== 메인메뉴 =====')
    print('1. 전화번호 추가 등록')
    print('2. 전화목록 목록 조회')
    print('3. 내 전화번호부 검색')
    print('0. 로그아웃')
    print('===================')
    num = int( input('메뉴 선택 : ') )
    return num

# 추가 등록 함수
def add_phone_num():
    
    # 1. DB에 넣어야할 항목들을 입력받자.
    input_name = input('이름 : ')
    input_phone = input('전화번호 : ')
    input_memo = input('메모사항 : ')
    
    # 2. SQL 작성 -> INSERT INTO 로 데이터 추가. => user_id=12 처럼, DB의 본인 숫자를 찾아서 하드코딩으로 INSERT.
    sql = f"INSERT INTO contacts (contacts.name, contacts.phone_num, contacts.memo, contacts.user_id) VALUES ('{input_name}', '{input_phone}', '{input_memo}', {login_user_id})"
    
    # 3. cursor / db_connect 를 이용, 실제 DB에 쿼리 수행.
    cursor.execute(sql)
    db_connect.commit()
    
    # 4. 안내메세지 2초간 출력 ('연락처 등록이 완료되었습니다.')
    
    print('연락처 등록이 완료되었습니다.')
    sleep(2)


# 로그인한 사용자가 등록한 모든 폰번 출력
def show_all_contacts():
    # login_user_id만 갖고 있으면 => 내가 가진 연락처 목록 조회 가능.
    # 추가 input 필요 없다.
    
    # 1. SQL 작성 - 내 연락처 목록
    sql = f"SELECT * FROM contacts WHERE contacts.user_id = {login_user_id}"
    
    # 2. cursor => 쿼리 실행 / 실행 결과를 별도의 tuple에 담자.
    cursor.execute(sql)
    contact_list = cursor.fetchall()
    
    # 3. 목록을 돌면서, 이름/폰번/메모 =>  조경진(메모사항) : 010-5112-3237  양식으로 가공.
    for contact in contact_list:
        # print(contact)
        name = contact['name']
        phone_num = contact['phone_num']
        memo = contact['memo']
        
        contact_str = f'{name}({memo}) : {phone_num}'
        print(contact_str)
        
    sleep(2)
    
# 전화번호부에서, 이름 기준으로 검색.
def search_my_contact_list():
    input_keyword = input('검색할 이름의 일부를 입력 : ')  # 경진 => 조경진
    
    # 이름에 input_keyword를 포함하고 있는 (내가 가진) 모든 연락처 목록을 조회.
    sql = f"SELECT * FROM contacts WHERE contacts.user_id = {login_user_id} AND contacts.name LIKE '%{input_keyword}%'"
    
    # print('완성된 쿼리 : ', sql)
    
    # DB에서 쿼리 실행 -> 결과 출력
    cursor.execute(sql)
    
    result = cursor.fetchall()  # DB row들의 목록 : tuple
    
    # result : 검색 결과 목록 => 0개? 검색결과 없음.
    if len(result) == 0:
        print('검색 결과가 없습니다.')
        sleep(2)
    else:
        
        print('==== 검색 결과 ====')
        
        # 검색 결과 확인 => 1. 이름 (메모) ... 4. 이름4 (메모4)
        for index, row  in enumerate(result):  # 반복시 enumerate함수 => 몇번째 줄 + 어떤 데이터 동시 추출
            line = f"{index+1}. {row['name']} ({row['memo']})"
            print(line)
            
        # 몇번 연락처를 상세보기 할건지?
        contact_num = int( input('상세 보기 연락처 선택 : ') )
        
        # contact_num에 맞는 line을 가지고 => dict을 가지고, Contact 형태의 객체로 변환. (클래스 활용)
        contact = Contact()  # 임시로, 기본값만 가지고 있는 연락처 생성.
        
        # 위치에 맞는 dict 꺼내오자. => dict의 내용을 가지고 => contact객체의 내용물변수들을 채워주자. (클래스의 기능 추가)
        select_line = result[contact_num-1] # dict 꺼내오기.
        contact.set_data(select_line)  # dict -> 클래스 인스턴스 예제.
        
        # cf) 클래스 객체 -> dict로 변환해야하는 경우도 많다. (메쏘드로 만들고 활용. 향후 체험 예정)
        
        # 연락처의 상세 정보 표시. (메쏘드로 만들고 활용)
        detail_num = contact.show_detail_info()
        if detail_num == 1:
            new_name = input('변경할 이름 : ')
            update_contact(contact, new_name)
        elif detail_num == 2:
            delete_contact()
            
        
    
def update_contact(contact, value):
    # INSERT INTO를 실행시키는 파이썬 코드와 유사함.
    sql = f"UPDATE contacts SET contacts.name = '{value}' WHERE contacts.id = {contact.id}"
    
    cursor.execute(sql) # 어떤 변경사항이 있을지를 알려줌.
    db_connect.commit() # 변경사항들 실제 반영.

def delete_contact():
    pass
        
        