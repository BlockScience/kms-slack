class MessageID:
    def __init__(self, channel: str, message_ts: str, thread_ts: str = None):
        self.channel = channel
        self.message_ts = message_ts
        self.thread_ts = thread_ts
        self.is_thread_reply = bool(thread_ts)

    def __str__(self):
        if self.is_thread_reply:
            return f"{self.channel}/{self.thread_ts}/{self.message_ts}"
        return f"{self.channel}/{self.message_ts}"


class ConversationID:
    def __init__(self, message_id: MessageID):
        self.channel = message_id.channel
        self.ts = message_id.thread_ts if message_id.is_thread_reply else message_id.message_ts

    def __str__(self):
        return f"{self.channel}/{self.ts}"


class ConversationHistory:

    def __init__(self):
        self._histories = {}

    def append(self, id: ConversationID, prompt: str, response: str):
        key = self._conversation_key(id)
        self._check_and_create(id)
        self._histories[key].append((prompt, response))

    def get(self, id: ConversationID):
        key = self._conversation_key(id)
        self._check_and_create(id)
        return self._histories[key]

    def exists(self, id: ConversationID):
        key = self._conversation_key(id)
        return key in self._histories

    def _check_and_create(self, id: ConversationID):
        key = self._conversation_key(id)
        if key not in self._histories:
            self._histories[key] = []
            print(f"Creating new history for conversation {key}")

    def _conversation_key(self, id: ConversationID):
        return f"{id.channel}-{id.ts}"

    def __str__(self):
        return self._histories
