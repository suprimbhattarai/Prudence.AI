class ConversationTitleService:
    MAX_TITLE_LENGTH = 60

    @classmethod
    def generate_initial_title(cls, content: str) -> str:
        normalized = " ".join(content.split())

        if len(normalized) <= cls.MAX_TITLE_LENGTH:
            return normalized

        return normalized[: cls.MAX_TITLE_LENGTH - 3].rstrip() + "..."
