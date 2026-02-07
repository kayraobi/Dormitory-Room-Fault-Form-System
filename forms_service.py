from googleapiclient.discovery import build
from auth_manager import AuthManager
import os
import json


class FormsService:
    def __init__(self):
        self.service = build(
            "forms",
            "v1",
            credentials=AuthManager.get_credentials()
        )
        self.file_path = "responses.json"

    def get_responses(self):
        form_id = os.getenv("FORM_API")

        if not form_id:
            raise RuntimeError("FORM_API env variable not set")

        result = self.service.forms().responses().list(
            formId=form_id
        ).execute()

        self._save_to_json(result)
        return result

    def _save_to_json(self, result):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        data["last_fetched"] = result.get("responses", [])
        data["total_responses"] = len(data["last_fetched"])

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
