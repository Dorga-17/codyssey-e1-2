"""개별 퀴즈 데이터를 관리하는 Quiz 클래스 모듈."""


class Quiz:
    """객관식 퀴즈 한 문제의 데이터를 관리하는 클래스"""

    def __init__(self, quiz_id, question, choices, answer, hints=None, is_default=False):
        self.id = quiz_id
        self.question = question
        self.choices = list(choices)
        self.answer = answer
        self.hints = list(hints) if hints is not None else []
        self.is_default = is_default

    def display(self):
        """퀴즈의 질문과 선택지를 화면에 출력한다."""
        print(f"\n문제 : {self.question}")
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def check_answer(self, selected_answer):
        """사용자가 선택한 번호가 정답인지 확인한다."""
        return selected_answer == self.answer

    def get_hint(self, hint_number):
        """요청한 번호의 힌트를 반환한다."""
        if 1 <= hint_number <= len(self.hints):
            return self.hints[hint_number - 1]
        return None

    def to_dict(self):
        """퀴즈 데이터를 JSON 저장에 사용할 딕셔너리로 변환한다."""
        return {
            "id": self.id,
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
            "hints": list(self.hints),
            "is_default": self.is_default
        }
