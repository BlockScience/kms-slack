from app.types import MessageID
from slack_sdk import WebClient
from os import environ


client = WebClient(token=environ["SLACK_BOT_TOKEN"])


def create(content: str, channel: str, thread_ts: str, display_name: str = None) -> MessageID:
    response = client.chat_postMessage(
        channel=channel, thread_ts=thread_ts, text=content[:49000], username=display_name)
    return MessageID(channel, response.data["ts"], thread_ts=thread_ts)


def update(content: str, channel: str, message_ts: str, thread_ts: str) -> MessageID:
    response = client.chat_update(
        channel=channel, ts=message_ts, thread_ts=thread_ts, text=content[:30000])
    return MessageID(channel, response.data["ts"], thread_ts=thread_ts)
