import json
import tkinter as tk
from tkinter import ttk

QUESTION_TEXT_MAP = {
    "45c81dca": "Room / Location",
    "7bfd83fb": "Additional comments",
    "6f53ef54": "Current role / status",
    "2d1e6d12": "Interested topic(s)",
    "3325db2b": "Instruction clarity (1–5)",
    "5734ef20": "Overall experience",
    "24e3f4f6": "Availability - Morning",
    "60b0b8a6": "Availability - Afternoon",
    "771c2f0b": "Availability - Friday",
    "0dd165ce": "Factor A: Speed",
    "73b36b93": "Factor B: Accuracy",
    "356cbd4d": "Factor C: Cost",
    "6c594c71": "Date",
    "578407ae": "Time"
}


class TodoResponsesUI:
    def __init__(self, json_path):
        self.json_path = json_path
        self.completed = []
        self.history_window = None

        self.root = tk.Tk()
        self.root.title("Responses – Todo")
        self.root.geometry("1100x650")

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable = tk.Frame(self.canvas)

        self.scrollable.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._bind_mousewheel(self.canvas)

        self._load_data()
        self._build_bottom()

        self.root.mainloop()

    def _bind_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", self._on_mousewheel)      # macOS / Windows
        widget.bind_all("<Button-4>", self._on_mousewheel_linux)  # Linux up
        widget.bind_all("<Button-5>", self._on_mousewheel_linux)  # Linux down

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        if event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    # -------- DATA --------
    def _load_data(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for response_key, answers in data.items():
            self._add_response_task(response_key, answers)

    def _add_response_task(self, response_key, answers):
        box = tk.LabelFrame(
            self.scrollable,
            text=response_key.upper(),
            padx=15,
            pady=12
        )
        box.pack(fill="x", expand=True, padx=25, pady=12)

        for qid, values in answers.items():
            question = QUESTION_TEXT_MAP.get(qid, qid)
            lbl = tk.Label(
                box,
                text=f"{question}: {', '.join(values)}",
                anchor="w",
                justify="left",
                wraplength=1000
            )
            lbl.pack(anchor="w", pady=2)

        ttk.Checkbutton(
            box,
            text="✔ Mark response as done",
            command=lambda: self._complete_response(box, response_key, answers)
        ).pack(anchor="e", pady=6)

    # -------- ACTIONS --------
    def _complete_response(self, frame, response_key, answers):
        self.completed.append((response_key, answers))
        frame.destroy()

    # -------- BOTTOM / HISTORY --------
    def _build_bottom(self):
        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=25, pady=10)

        ttk.Button(bottom, text="History", command=self._open_history).pack(anchor="e")

    def _open_history(self):
        if self.history_window and self.history_window.winfo_exists():
            self.history_window.lift()
            return

        self.history_window = tk.Toplevel(self.root)
        self.history_window.title("History")
        self.history_window.geometry("1000x550")

        self.history_window.protocol("WM_DELETE_WINDOW", self._close_history)

        canvas = tk.Canvas(self.history_window)
        scrollbar = ttk.Scrollbar(self.history_window, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas)

        frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for item in list(self.completed):
            response_key, answers = item

            box = tk.LabelFrame(frame, text=f"✔ {response_key.upper()}", padx=15, pady=10)
            box.pack(fill="x", expand=True, padx=25, pady=10)

            for qid, values in answers.items():
                question = QUESTION_TEXT_MAP.get(qid, qid)
                tk.Label(
                    box,
                    text=f"{question}: {', '.join(values)}",
                    anchor="w",
                    justify="left",
                    wraplength=900
                ).pack(anchor="w", pady=2)

            ttk.Button(
                box,
                text="↩ Restore",
                command=lambda i=item, b=box: self._restore_response(i, b)
            ).pack(anchor="e", pady=6)

    def _restore_response(self, item, history_box):
        response_key, answers = item
        self.completed.remove(item)
        history_box.destroy()
        self._add_response_task(response_key, answers)

    def _close_history(self):
        if self.history_window:
            self.history_window.destroy()
            self.history_window = None
