from dotenv import load_dotenv
import os

from forms_service import FormsService
from ui import ResponsesTableUI
from DeepL_Translator import DeepL_Translator

load_dotenv()


def main():
    forms = FormsService()
    forms.get_responses()

    translator = DeepL_Translator(
        auth_key=os.getenv("DEEPL_API"),
        input_path="responses.json",
        output_path="translated_answers.json",
        target_lang="BS"
    )

    translator.translate()

    ResponsesTableUI(json_path="translated_answers.json")


if __name__ == "__main__":
    main()
