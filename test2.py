import json

# Assume a file named 'data.json' exists with the sample content
file_path = 'responses.json'
with open(file_path, 'r') as file:
    data = json.load(file)

answers = data["last_fetched"][0]["answers"]

for question_id, answer_data in answers.items():
    values = [
        a["value"]
        for a in answer_data["textAnswers"]["answers"]
    ]
    print(question_id, "->", values)

    def _save_to_json(self, result):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "w", encoding="utf-8") as f:
                   json.dump(python_data, json_file, indent=4)
            except json.JSONDecodeError:
                data = {}
