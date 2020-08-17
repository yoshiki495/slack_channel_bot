class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "@here Welcome to Slack! :wave: We're so glad you're here."
            ),
        },
    }

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel

    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.WELCOME_BLOCK,
            ],
        }

    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]