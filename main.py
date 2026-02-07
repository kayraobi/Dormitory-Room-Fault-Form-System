from dotenv import load_dotenv
load_dotenv()  # <-- MUTLAKA İLK SATIRLARDA

from forms_service import FormsService

forms = FormsService()
responses = forms.get_responses()

print(responses)
