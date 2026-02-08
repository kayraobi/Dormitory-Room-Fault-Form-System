import json
from googletrans import Translator


class Translation:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
        self.translator = Translator()

    def translate(self, dest="bs"):
        translated_answer = self.translator.translate(
            self.answer, dest=dest
        ).text
        return translated_answer


def get_text_answer(data):
    answers = data["last_fetched"][0]["answers"]
    results = []

    for question_id, answer_data in answers.items():
        for a in answer_data["textAnswers"]["answers"]:
            original_answer = a["value"]

            t = Translation(question_id, original_answer)
            translated = t.translate()

            results.append({
                "question_id": question_id,
                "original": original_answer,
                "translated": translated
            })

    return results


# ---- JSON OKU ----
with open("responses.json", "r", encoding="utf-8") as f:
    data = json.load(f)


print(get_text_answer(data))
