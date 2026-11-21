"""퀴즈 게임의 전체 실행과 기능을 관리하는 QuizGame 클래스 모듈"""


import random
from datetime import datetime
from default_quizzes import create_default_quizzes
from quiz import Quiz


class QuizGame:
    """퀴즈 게임 전체의 데이터와 기능을 관리하는 클래스"""

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.high_score = None
        self.play_history = []
        self.next_user_quiz_id = 1


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


    def get_required_text(self, prompt):
        """공백이 아닌 문자열을 안전하게 입력받는다."""
        while True:
            try:
                text = input(prompt).strip()
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다.")
                return None
            if not text:
                print("내용을 입력해 주세요.")
                continue
            return text


    def add_quiz(self):
        """사용자가 입력한 문제를 새로운 퀴즈로 등록한다."""
        print("\n===== 퀴즈 추가 =====")
        question = self.get_required_text("문제 내용 : ")
        if question is None:
            print("퀴즈 추가를 취소했습니다.")
            return None
        choices = []
        for number in range(1, 5):
            choice = self.get_required_text(f"{number}번 선택지 : ")
            if choice is None:
                print("퀴즈 추가를 취소했습니다.")
                return None
            choices.append(choice)
        answer = self.get_valid_input("정답 번호(1-4) : ", 1, 4)
        if answer is None:
            print("퀴즈 추가를 취소했습니다.")
            return None
        hints = []
        print("힌트는 최대 2개까지 입력할 수 있습니다.")
        print("힌트를 생략하려면 Enter를 누르세요.")
        for number in range(1, 3):
            try:
                hint = input(f"{number}번 힌트 : ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되어 퀴즈 추가를 취소했습니다.")
                return None
            if not hint:
                break
            hints.append(hint)
        while any(
            quiz.id == f"user-{self.next_user_quiz_id}"
            for quiz in self.quizzes
        ):
            self.next_user_quiz_id += 1
        quiz_id = f"user-{self.next_user_quiz_id}"
        new_quiz = Quiz(
            quiz_id,
            question,
            choices,
            answer,
            hints=hints,
            is_default=False
        )
        self.quizzes.append(new_quiz)
        self.next_user_quiz_id += 1
        print(f"퀴즈가 추가되었습니다. (ID : {quiz_id})")
        return new_quiz


    def show_quiz_list(self):
        """기본 제공 문제와 사용자 추가 문제를 모두 출력한다."""
        print("\n===== 전체 퀴즈 목록 =====")
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        default_count = sum(quiz.is_default for quiz in self.quizzes)
        user_count = len(self.quizzes) - default_count

        print(f"전체 문제 수 : {len(self.quizzes)}개")
        print(f"기본 제공 문제 : {default_count}개")
        print(f"사용자 추가 문제 : {user_count}개")
        for number, quiz in enumerate(self.quizzes, start=1):
            if quiz.is_default:
                quiz_type = "기본 제공 / 삭제 불가"
            else:
                quiz_type = "사용자 추가 / 삭제 가능"
            print(f"\n[{number}] ID : {quiz.id}")
            print(f"문제 유형 : {quiz_type}")
            quiz.display()
            print(f"정답 : {quiz.answer}번")
            if quiz.hints:
                for hint_number, hint in enumerate(quiz.hints, start=1):
                    print(f"힌트 {hint_number} : {hint}")
            else:
                print("힌트 : 없음")


    def delete_quiz(self):
        """사용자가 추가한 퀴즈만 삭제한다."""
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return False
        self.show_quiz_list()
        number = self.get_valid_input(
            f"삭제할 문제 번호(1-{len(self.quizzes)}, 0 : 취소) : ",
            0,
            len(self.quizzes)
        )
        if number is None or number == 0:
            print("퀴즈 삭제를 취소했습니다.")
            return False
        selected_quiz = self.quizzes[number - 1]
        if selected_quiz.is_default:
            print("기본 제공 문제는 삭제할 수 없습니다.")
            return False
        deleted_quiz = self.quizzes.pop(number - 1)
        print(f"퀴즈가 삭제되었습니다. (ID : {deleted_quiz.id})")
        return True


    def select_question_count(self):
        """사용자가 풀 문제 수를 선택하고 검증한다."""
        total = len(self.quizzes)
        if total == 0:
            print("풀 수 있는 퀴즈가 없습니다.")
            return None
        print(f"\n현재 풀 수 있는 퀴즈는 {total}개입니다.")
        return self.get_valid_input(
            f"풀 문제 수를 선택해 주세요(1-{total}) : ", 1, total
        )


    def select_random_quizzes(self, count):
        """지정한 개수의 퀴즈를 중복 없이 무작위로 선택한다."""
        return random.sample(self.quizzes, count)


    def ask_question(self, quiz):
        """퀴즈 한 문제를 출제하고 힌트, 정답, 점수를 처리한다."""
        quiz.display()
        hints_used = 0
        while hints_used < 2 and hints_used < len(quiz.hints):
            action = self.get_valid_input(
                "힌트 사용(1 : 힌트 보기, 2 : 정답 입력) : ", 1, 2
            )
            if action is None:
                return None
            if action == 2:
                break
            hints_used += 1
            print(f"힌트 {hints_used} : {quiz.get_hint(hints_used)}")
        selected_answer = self.get_valid_input(
            f"정답 번호(1-{len(quiz.choices)}) : ", 1, len(quiz.choices)
        )
        if selected_answer is None:
            return None
        is_correct = quiz.check_answer(selected_answer)
        if is_correct:
            points = 10 - (2 * hints_used)
            print(f"정답입니다! {points}점을 획득했습니다.")
        else:
            points = 0
            correct_choice = quiz.choices[quiz.answer - 1]
            print(f"오답입니다. 정답은 {quiz.answer}번, '{correct_choice}'입니다.")
            print(f"획득 점수 : 0점")
        return {
            "quiz_id": quiz.id,
            "question": quiz.question,
            "selected_answer": selected_answer,
            "correct_answer": quiz.answer,
            "is_correct": is_correct,
            "hints_used": hints_used,
            "points": points
        }


    def play_quiz(self):
        """선택한 문제를 순서대로 출제하고 전체 결과를 집계한다."""
        count = self.select_question_count()
        if count is None:
            return None
        selected_quizzes = self.select_random_quizzes(count)
        total_points = 0
        correct_count = 0
        question_results = []
        for index, quiz in enumerate(selected_quizzes, start=1):
            print(f"\n===== {index}/{count}번 문제 =====")
            result = self.ask_question(quiz)
            if result is None:
                print("퀴즈 진행이 중단되었습니다. 이번 플레이 결과는 기록하지 않습니다.")
                return None
            question_results.append(result)
            total_points += result["points"]
            if result["is_correct"]:
                correct_count += 1
        print("\n===== 퀴즈 결과 =====")
        print(f"푼 문제 수 : {count}개")
        print(f"맞힌 문제 수 : {correct_count}개")
        print(f"총점 : {total_points}점 / {count * 10}점")
        result = {
            "question_count": count,
            "correct_count": correct_count,
            "total_points": total_points,
            "question_results": question_results
        }
        self.record_play_result(result)
        return result


    def record_play_result(self, result):
        """완료한 플레이를 기록하고 최고 점수를 갱신한다."""
        play_record = {
            "played_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "question_count": result["question_count"],
            "correct_count": result["correct_count"],
            "total_points":result["total_points"],
            "question_results": result["question_results"]
        }
        self.play_history.append(play_record)
        if self.high_score is None or play_record["total_points"] > self.high_score:
            self.high_score = play_record["total_points"]
        return play_record


    def show_score_history(self):
        """최고 점수와 전체 플레이 기록을 출력한다."""
        print("\n===== 최고 점수 및 플레이 기록 =====")
        if self.high_score is None:
            print("최고 점수 : 아직 기록이 없습니다.")
        else:
            print(f"최고 점수 : {self.high_score}점")
        if not self.play_history:
            print("플레이 기록이 없습니다.")
            return
        print(f"전체 플레이 횟수 : {len(self.play_history)}회")
        for index, record in enumerate(self.play_history, start=1):
            print(f"\n[{index}회차] {record['played_at']}")
            print(f"푼 문제 수 : {record['question_count']}개")
            print(f"맞힌 문제 수 : {record['correct_count']}개")
            print(f"총점 : {record['total_points']}점")
            for number, item in enumerate(record["question_results"], start=1):
                result_text = "정답" if item["is_correct"] else "오답"
                print(f"  {number}번 문제 [{result_text}] : {item['question']}")
                print(f"    선택한 답 : {item['selected_answer']}번")
                print(f"    실제 정답 : {item['correct_answer']}번")
                print(f"    힌트 사용 : {item['hints_used']}개")
                print(f"    획득 점수 : {item['points']}점")


    def run(self):
        """메인 메뉴를 반복 실행하고 사용자 선택을 처리한다."""
        while True:
            self.show_menu()
            choice = self.get_valid_input("메뉴 번호(1-5) : ", 1, 5)
            if choice is None:
                print("입력이 중단되어 게임을 종료합니다.")
                print("현재 저장 기능은 아직 구현되지 않았습니다.")
                return
            if choice == 1:
                self.play_quiz()
                continue
            if choice == 2:
                self.add_quiz()
                continue
            if choice == 3:
                self.delete_quiz()
                continue
            if choice == 4:
                self.show_score_history()
                continue
            if choice == 5:
                print("현재 저장 기능은 아직 구현되지 않았습니다.")
                print("게임을 종료합니다.")
                return
            print(f"\n{choice}번 메뉴의 기능은 아직 구현되지 않았습니다.")
