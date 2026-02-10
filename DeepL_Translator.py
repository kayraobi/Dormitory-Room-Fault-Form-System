import json
import deepl


class DeepL_Translator:
    def __init__(self, auth_key, input_path, output_path, target_lang="BS"):
        self.client = deepl.DeepLClient(auth_key)
        self.input_path = input_path
        self.output_path = output_path
        self.target_lang = target_lang

    def load_data(self):
        with open(self.input_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def translate(self):
        data = self.load_data()
        translated_responses = {}

        for idx, response in enumerate(data.get("last_fetched", []), start=1):
            response_key = f"response_{idx}"
            translated_responses[response_key] = {}

            answers = response.get("answers", {})

            for question_id, question in answers.items():
                text_answers = question.get("textAnswers", {}).get("answers", [])
                translated_values = []

                for answer in text_answers:
                    value = answer.get("value")
                    if value:
                        translated = self.client.translate_text(
                            value,
                            target_lang=self.target_lang
                        )
                        translated_values.append(translated.text)

                translated_responses[response_key][question_id] = translated_values

        self.save(translated_responses)

    def save(self, data):
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
