import json
import tkinter as tk
from tkinter import ttk


# 🔹 HARD-CODED QUESTION ID → TEXT MAP
QUESTION_TEXT_MAP = {
    "45c81dca": "den",
    "7bfd83fb": "Please provide a brief description of why you are taking this test:",
    "6f53ef54": "What is your current role/status?",
    "2d1e6d12": "Which topics are you most interested in?",
    "3325db2b": "On a scale of 1 to 5, how clear were the instructions for this form?",
    "5734ef20": "Rate the overall user experience:",
    "24e3f4f6": "Availability - Monday",
    "60b0b8a6": "Availability - Wednesday",
    "771c2f0b": "Availability - Friday",
    "0dd165ce": "Factor A: Speed",
    "73b36b93": "Factor B: Accuracy",
    "356cbd4d": "Factor C: Cost",
    "6c594c71": "Today's Date",
    "578407ae": "Current Time"
}


class ResponsesTableUI:
    def __init__(self, json_path):
        self.json_path = json_path
        self.root = tk.Tk()
        self.root.title("Google Forms Responses")
        self.root.geometry("800x500")

        self._build_table()
        self._load_data()

        self.root.mainloop()

    def _build_table(self):
        columns = ("question", "answer")

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        self.tree.heading("question", text="Question")
        self.tree.heading("answer", text="Answer")

        self.tree.column("question", width=350)
        self.tree.column("answer", width=420)

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_data(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        responses = data.get("last_fetched", [])

        for response in responses:
            answers = response.get("answers", {})

            for question_id, answer_block in answers.items():
                value = self._extract_answer(answer_block)
                question_text = QUESTION_TEXT_MAP.get(question_id, question_id)

                self.tree.insert(
                    "",
                    "end",
                    values=(question_text, value)
                )

    def _extract_answer(self, answer_block):
        if "textAnswers" in answer_block:
            answers = answer_block["textAnswers"].get("answers", [])
            return ", ".join(a.get("value", "") for a in answers)

        if "choiceAnswers" in answer_block:
            answers = answer_block["choiceAnswers"].get("answers", [])
            return ", ".join(a.get("value", "") for a in answers)

        return "—"
