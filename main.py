from dotenv import load_dotenv
import os

from forms_service import FormsService
from DeepL_Translator import DeepL_Translator
from ui import TodoResponsesUI

load_dotenv()


def main():
    # 1️⃣ Form cevaplarını çek
    forms = FormsService()
    forms.get_responses()  # responses.json

    # 2️⃣ Çevir
    translator = DeepL_Translator(
        auth_key=os.getenv("DEEPL_API"),
        input_path="responses.json",
        output_path="translated_answers.json",
        target_lang="BS"
    )
    translator.translate()

    # 3️⃣ UI (her response = task)
    TodoResponsesUI("translated_answers.json")


if __name__ == "__main__":
    main()
