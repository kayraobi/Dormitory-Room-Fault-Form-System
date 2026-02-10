import json
import tkinter as tk
from tkinter import ttk

# 🔹 QUESTION ID → QUESTION TEXT MAP
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
        self.root.title("Translated Responses")
        self.root.geometry("900x550")

        self._build_table()
        self._load_data()

        self.root.mainloop()

    # ---------------- UI ----------------
    def _build_table(self):
        columns = ("question", "answer")

        self.tree = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        self.tree.heading("question", text="Question")
        self.tree.heading("answer", text="Answer")

        self.tree.column("question", width=420, anchor="w")
        self.tree.column("answer", width=460, anchor="w")

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------------- DATA ----------------
    def _load_data(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print("JSON okunamadı:", e)
            return

        # tabloyu temizle
        self.tree.delete(*self.tree.get_children())

        for response_key, answers in data.items():
            # 🔹 RESPONSE HEADER
            self.tree.insert(
                "",
                "end",
                values=(f"--- {response_key.upper()} ---", "")
            )

            for question_id, answer_list in answers.items():
                question_text = QUESTION_TEXT_MAP.get(question_id, question_id)
                answer_text = ", ".join(answer_list)

                self.tree.insert(
                    "",
                    "end",
                    values=(question_text, answer_text)
                )


# ---------------- RUN ----------------
if __name__ == "__main__":
    ResponsesTableUI("translated_answers.json")
