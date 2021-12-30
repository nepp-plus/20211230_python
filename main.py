# PyMySQL - 디비 서버 연동 체험.
# 단순 동작 위주의 코드 작성
# DB 연결 => 기타기능 : phone_book.py 모듈 이용.

from time import sleep
from phone_book import add_phone_num, print_main_menu, sign_up, sign_in, print_phone_book_menu, show_all_contacts, search_my_contact_list


# 프로그램이 종료될 사유가 생길때까지 무한반복.

while True:
    menu_num = print_main_menu()

    if menu_num == 2:
        sign_up()
    elif menu_num == 1:
        login_result = sign_in()
        
        # 로그인에 성공했다면? 개인별 연락처 메뉴로 이동.
        if login_result:
            while True:
                num = print_phone_book_menu()
                if num == 0:
                    print('로그아웃 후 메인으로 돌아갑니다.')
                    sleep(2)
                    break
                elif num == 1:
                    add_phone_num()
                elif num == 2:
                    show_all_contacts()
                elif num == 3:
                    search_my_contact_list()
                
    elif menu_num == 0:
        print('프로그램을 종료합니다.')
        break