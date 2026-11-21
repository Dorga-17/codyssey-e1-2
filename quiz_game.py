"""퀴즈 게임의 전체 실행과 기능을 관리하는 QuizGame 클래스 모듈"""


import random
import json
from pathlib import Path
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
        self.state_file = Path(__file__).resolve().parent / "state.json"


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


    def save_state(self):
        """사용자 퀴즈와 플레이 기록을 JSON 파일에 저장한다."""
        state = {
            "user_quizzes": [
                quiz.to_dict()
                for quiz in self.quizzes
                if not quiz.is_default
            ],
            "high_score": self.high_score,
            "play_history": self.play_history,
            "next_user_quiz_id": self.next_user_quiz_id
        }

        try:
            json_text = json.dumps(state, ensure_ascii=False, indent=2)
            self.state_file.write_text(json_text, encoding="utf-8")
        except (OSError, TypeError, ValueError) as error:
            print(f"게임 저장 중 오류가 발생했습니다: {error}")
            return False

        print("게임 데이터가 state.json에 저장되었습니다.")
        return True


    def load_state(self):
        """state.json에서 사용자 퀴즈와 플레이 기록을 불러온다."""
        if not self.state_file.exists():
            print("저장된 게임 데이터가 없어 기본 상태로 시작합니다.")
            return False
        try:
            state = json.loads(
                self.state_file.read_text(encoding="utf-8")
            )
            user_quizzes_data = state["user_quizzes"]
            if not isinstance(user_quizzes_data, list):
                raise ValueError("사용자 퀴즈 데이터는 목록이어야 합니다.")
            loaded_quizzes = []
            seen_ids = set()
            for quiz_data in user_quizzes_data:
                if not isinstance(quiz_data, dict):
                    raise ValueError("퀴즈 데이터는 딕셔너리여야 합니다.")
                required_keys = {"id", "question", "choices", "answer", "hints", "is_default"}
                if not required_keys.issubset(quiz_data):
                    raise ValueError("사용자 퀴즈의 필수 항목이 누락되었습니다.")
                quiz_id = quiz_data["id"]
                if (
                    not isinstance(quiz_id, str)
                    or not quiz_id.startswith("user-")
                    or not quiz_id[5:].isdigit()
                    or int(quiz_id[5:]) < 1
                    or quiz_id != f"user-{int(quiz_id[5:])}"
                    or quiz_id in seen_ids
                ):
                    raise ValueError("사용자 문제 ID가 잘못되었거나 중복되었습니다.")

                if quiz_data["is_default"] is not False:
                    raise ValueError("사용자 문제의 유형이 올바르지 않습니다.")
                question = quiz_data["question"]
                if not isinstance(question, str) or not question.strip():
                    raise ValueError("문제 내용이 올바르지 않습니다.")
                choices = quiz_data["choices"]
                if (
                    not isinstance(choices, list)
                    or len(choices) != 4
                    or any(not isinstance(choice, str) or not choice.strip() for choice in choices)
                ):
                    raise ValueError("선택지는 내용이 있는 문자열 4개여야 합니다.")
                answer = quiz_data["answer"]
                if type(answer) is not int or not 1 <= answer <= 4:
                    raise ValueError("정답 번호는 1부터 4까지의 정수여야 합니다.")
                hints = quiz_data["hints"]
                if (
                    not isinstance(hints, list)
                    or len(hints) > 2
                    or any(not isinstance(hint, str) or not hint.strip() for hint in hints)
                ):
                    raise ValueError("힌트는 내용이 있는 문자열 최대 2개여야 합니다.")
                loaded_quiz = Quiz(
                    quiz_id=quiz_id,
                    question=question,
                    choices=choices,
                    answer=answer,
                    hints=hints,
                    is_default=False
                )
                loaded_quizzes.append(loaded_quiz)
                seen_ids.add(quiz_id)
            high_score = state["high_score"]
            if high_score is not None and (
                type(high_score) is not int or high_score < 0
            ):
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")
            play_history = state["play_history"]
            if not isinstance(play_history, list):
                raise ValueError("플레이 기록은 목록이어야 합니다.")
            required_record_keys = {
                "played_at", "question_count", "correct_count",
                "total_points", "question_results"
            }
            required_result_keys = {
                "quiz_id", "question", "selected_answer",
                "correct_answer", "is_correct", "hints_used", "points"
            }
            for record in play_history:
                if (
                    not isinstance(record, dict)
                    or not required_record_keys.issubset(record)
                ):
                    raise ValueError("플레이 기록의 구조가 올바르지 않습니다.")

                if (
                    not isinstance(record["played_at"], str)
                    or not record["played_at"].strip()
                ):
                    raise ValueError("플레이 날짜가 올바르지 않습니다.")
                question_count = record["question_count"]
                correct_count = record["correct_count"]
                total_points = record["total_points"]
                question_results = record["question_results"]
                if type(question_count) is not int or question_count < 1:
                    raise ValueError("플레이 문제 수가 올바르지 않습니다.")
                if (
                    type(correct_count) is not int
                    or not 0 <= correct_count <= question_count
                ):
                    raise ValueError("정답 개수가 올바르지 않습니다.")
                if type(total_points) is not int or total_points < 0:
                    raise ValueError("플레이 점수가 올바르지 않습니다.")
                if (
                    not isinstance(question_results, list)
                    or len(question_results) != question_count
                    or any(
                        not isinstance(result, dict)
                        or not required_result_keys.issubset(result)
                        for result in question_results
                    )
                ):
                    raise ValueError("문제별 플레이 기록이 올바르지 않습니다.")
                for item in question_results:
                    quiz_id = item["quiz_id"]
                    question = item["question"]
                    selected = item["selected_answer"]
                    answer = item["correct_answer"]
                    correct = item["is_correct"]
                    hints = item["hints_used"]
                    points = item["points"]
                    if (
                        not isinstance(quiz_id, str) or not quiz_id.strip()
                        or not isinstance(question, str) or not question.strip()
                    ):
                        raise ValueError("문제 ID 또는 내용이 올바르지 않습니다.")
                    if (
                        type(selected) is not int or not 1 <= selected <= 4
                        or type(answer) is not int or not 1 <= answer <= 4
                        or type(correct) is not bool
                        or correct != (selected == answer)
                        or type(hints) is not int or not 0 <= hints <= 2
                        or type(points) is not int
                        or points != (10 - 2 * hints if correct else 0)
                    ):
                        raise ValueError("문제별 플레이 기록의 값이 올바르지 않습니다.")
                if correct_count != sum(
                    item["is_correct"] for item in question_results
                ):
                    raise ValueError("전체 정답 개수가 일치하지 않습니다.")
                if total_points != sum(
                    item["points"] for item in question_results
                ):
                    raise ValueError("전체 점수가 일치하지 않습니다.")
            next_user_quiz_id = state["next_user_quiz_id"]
            if (
                type(next_user_quiz_id) is not int
                or next_user_quiz_id < 1
                or any(
                    next_user_quiz_id <= int(quiz.id[5:])
                    for quiz in loaded_quizzes
                )
            ):
                raise ValueError("다음 사용자 문제 번호가 올바르지 않습니다.")
        except (OSError, UnicodeError, json.JSONDecodeError,
                KeyError, TypeError, ValueError) as error:
            print(f"게임 데이터를 불러오지 못했습니다: {error}")
            return False
        self.quizzes = create_default_quizzes() + loaded_quizzes
        self.high_score = high_score
        self.play_history = play_history
        self.next_user_quiz_id = next_user_quiz_id
        print("저장된 게임 데이터를 불러왔습니다.")
        return True


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
