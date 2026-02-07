import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

class AuthManager:
    _creds = None

    SCOPES = [
        "https://www.googleapis.com/auth/forms.body.readonly",
        "https://www.googleapis.com/auth/forms.responses.readonly"
    ]

    @classmethod
    def get_credentials(cls):
        if cls._creds and cls._creds.valid:
            return cls._creds

        if os.path.exists("token.json"):
            cls._creds = Credentials.from_authorized_user_file(
                "token.json", cls.SCOPES
            )

        if not cls._creds or not cls._creds.valid:
            if cls._creds and cls._creds.expired and cls._creds.refresh_token:
                cls._creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", cls.SCOPES
                )
                cls._creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(cls._creds.to_json())

        return cls._creds
