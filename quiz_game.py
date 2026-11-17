"""퀴즈 게임의 전체 실행과 기능을 관리하는 QuizGame 클래스 모듈"""


class QuizGame:
    """퀴즈 게임 전체의 데이터와 기능을 관리하는 클래스"""

    def __init__(self):
        self.quizzes = []
        self.high_score = None
        self.play_history = []

    def show_menu(self):
        """메인 메뉴를 화면에 출력한다."""
        print("\n===== 철학 · 심리학 · 경제학 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록 보기 및 삭제")
        print("4. 점수 및 플레이 기록 확인")
        print("5. 저장 후 게임 종료")
        print("=============================================")

    def get_valid_input(self, prompt, min_value, max_value):
        """지정한 범위의 정수를 입력받고 검증한다."""
        while True:
            try:
                user_input = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None
            if not user_input:
                print("입력값이 비어 있습니다. 다시 입력해 주세요.")
                continue
            try:
                number = int(user_input)
            except ValueError:
                print("숫자를 입력해 주세요.")
                continue
            if not min_value <= number <= max_value:
                print(f"{min_value}에서 {max_value}까지의 숫자를 입력해 주세요.")
                continue
            return number

    def run(self):
        """메인 메뉴를 반복 실행하고 사용자 선택을 처리한다."""
        while True:
            self.show_menu()
            choice = self.get_valid_input("메뉴 번호(1-5) : ", 1, 5)
            if choice is None:
                print("입력이 중단되어 게임을 종료합니다.")
                print("현재 저장 기능은 아직 구현되지 않았습니다.")
                return
            if choice == 5:
                print("현재 저장 기능은 아직 구현되지 않았습니다.")
                print("게임을 종료합니다.")
                return
            print(f"\n{choice}번 메뉴의 기능은 아직 구현되지 않았습니다.")
