import requests
from CaseInsensitiveDict import CaseInsensitiveDict


class SlackClient:
    def __init__(self, slack_token: str) -> None:
        self.slack_token = slack_token

        self.session = requests.sessions.Session()
        self.session.headers = CaseInsensitiveDict(dictionary={"Authorization": f"Bearer {slack_token}"})

    def send_message(self, channel: str, message: str) -> None:
        self.session.post(
            "https://slack.com/api/chat.postMessage",
            json={
                "channel": f"#{channel}",
                "unfurl_links": False,
                "unfurl_media": False,
                "username": "Canary hitman",
                "mrkdwn": True,
                "icon_emoji": ":bird:",
                "text": message,
            },
        )

    def get_user(self, email: str) -> str:
        response = self.session.post("https://slack.com/api/users.lookupByEmail", data={"email": email})

        return response.json()["user"]["name"]
