from app import slack_client
from time import time


class Message:
    def __init__(self, content: str, channel: str, thread_ts: str | None, display_name: str | None = None):
        self.message_ts = slack_client.create(
            content, channel, thread_ts, display_name).message_ts
        self.content = content
        self.channel = channel
        self.thread_ts = thread_ts
        self.in_thread = bool(thread_ts)

    def update(self, content: str, append: bool = False, update_content: bool = True):
        if not update_content:
            slack_client.update(content, self.channel,
                                self.message_ts, self.thread_ts)
            return self
        if append:
            self.content += content
        else:
            self.content = content
        slack_client.update(self.content, self.channel,
                            self.message_ts, self.thread_ts)
        return self


class MultipartMessage:
    def __init__(self, channel: str, thread_ts: str, initiated_by: str):
        self.channel = channel
        self.thread_ts = thread_ts
        self.initiated_by = initiated_by
        self.streaming_buffer: str = ""
        self.streaming_target: Message | None = None
        self.finished: bool = False
        self._messages: list[Message] = []
        self.start_time = time()

    def add(self, content: str) -> Message:
        resp = Message(content, self.channel, self.thread_ts)
        self._messages.append(resp)
        return resp

    def get(self, index: int) -> Message | None:
        return None if index >= len(self._messages) else self._messages[index]

    def finish(self) -> None:
        self.finished = True

    def latest(self) -> Message | None:
        return self.get(self._len() - 1)

    def _len(self) -> int:
        return len(self._messages)

    def __repr__(self):
        return '<Thread %r>' % self.thread_ts
