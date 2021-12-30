# 연락처를 표현. (DB - contacts 테이블에 대응.)
# 연락처에 관련된 메쏘드들을 내포할 예정.

class Contact:
    def __init__(self):
        # 객체 변수 생성 => 기본값들로 대입.
        self.id = 0  # 임시로 int인 0으로 대입. (나중에 int가 올거라고 암시.)
        self.user_id = 0
        self.name = ''  # 임시로 str 인 '' 대입. (나중에 str이 올거라고 암시.)
        self.phone_num = ''
        self.memo = ''
        