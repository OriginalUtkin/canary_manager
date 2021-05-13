from canary_hitman.clients.base import BaseClient

from .exceptions import ErrorCodeException, LookupByEmailException


class SlackClient(BaseClient):
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

        r_json = response.json()

        if not r_json["ok"]:
            raise ErrorCodeException

        if not r_json["user"].get("name"):
            raise LookupByEmailException

        return response.json()["user"]["name"]
