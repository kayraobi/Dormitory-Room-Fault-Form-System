from dotenv import load_dotenv
load_dotenv()

from forms_service import FormsService
from ui import ResponsesTableUI


def main():
    forms = FormsService()

    # Google Forms'tan response'ları çek ve JSON'a yaz
    forms.get_responses()

    # UI'yi aç (JSON'dan okur)
    ResponsesTableUI(json_path="responses.json")


if __name__ == "__main__":
    main()
