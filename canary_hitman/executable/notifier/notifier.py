from datetime import datetime

from canary_hitman.clients.slack import SlackClient


class Notifier:
    def __init__(self, channel_to_notify: str, slack_token: str) -> None:
        self.channel_to_notify = channel_to_notify
        self.slack_token = slack_token

        self.slack_client = SlackClient(slack_token=self.slack_token)

    def notify_failure(self) -> None:
        pass

    def notify_new_release(self, canary_releaser_email: str, new_canary_commit_link: str, project_name: str) -> None:
        canary_releaser: str = self.slack_client.get_user(email=canary_releaser_email)

        message = (
            f":clock1: *RELEASE TIME*: {datetime.now().strftime('%d %b, %a - %H:%M')}\n\n"
            f":bust_in_silhouette: *RELEASER*: <@{canary_releaser}>\n\n"
            f":gitlab: *COMMIT (last in MR)*: <{new_canary_commit_link}|link>\n\n"
            f":hammer_and_wrench: *PROJECT NAME*: {project_name}\n"
        )

        self.slack_client.send_message(self.channel_to_notify, message)

    def notify_override(
        self,
        canary_releaser_email: str,
        previous_canary_releaser_email: str,
        new_canary_commit_link: str,
        project_name: str,
    ) -> None:
        canary_releaser: str = self.slack_client.get_user(email=canary_releaser_email)
        previous_canary_releaser: str = self.slack_client.get_user(email=previous_canary_releaser_email)

        message = (
            f":clock1: *RELEASE TIME*: {datetime.now().strftime('%d %b, %a - %H:%M')}\n\n"
            f":bust_in_silhouette: *RELEASER*: <@{canary_releaser}>\n\n"
            f":gitlab: *COMMIT (last in MR)*: <{new_canary_commit_link}|link>\n\n"
            f":hammer_and_wrench: *PROJECT NAME*: {project_name}\n\n\n"
            f":speaking_head_in_silhouette: cc <@{previous_canary_releaser}>; _Your canary deployment will be overriden by this release._\n"
        )

        self.slack_client.send_message(self.channel_to_notify, message)
