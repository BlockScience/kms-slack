from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, LLMResult, AgentFinish
from app.message import MultipartMessage, Message
from app.config import STREAM_IF_STARTS_WITH
from time import time


class ConversationalCallbackHandler(BaseCallbackHandler):
    def __init__(self, response: Message):
        super().__init__()
        self.response = response
        self.streaming_buffer = ""
        self.last_update = time()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.streaming_buffer += token
        if self.streaming_buffer.strip() and time() - self.last_update > 1:
            self.last_update = time()
            self.response.update(self.streaming_buffer)


class AgenticCallbackHandler(BaseCallbackHandler):
    def __init__(self, multi_response: MultipartMessage):
        super().__init__()
        self.response = multi_response

    def on_llm_start(
        self, serialized: dict[str, any], prompts: list[str], **kwargs: any
    ) -> any:
        self.check_for_finished()
        """Run when LLM starts running."""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.response.streaming_target is None:
            self.response.streaming_buffer += token
            if self.response.streaming_buffer.startswith(STREAM_IF_STARTS_WITH):
                self.response.streaming_target = self.response.add(
                    self.response.streaming_buffer
                )
                self.response.streaming_buffer = ""
            return
        else:
            self.response.streaming_target.update(token, append=True)

    def finish_streaming(self):
        self.response.streaming_target = None
        self.response.streaming_buffer = ""

    def on_llm_end(self, response: LLMResult, **kwargs: any) -> any:
        """Run when LLM ends running."""
        self.streaming_target = None

    def on_agent_action(self, action: AgentAction, **kwargs: any) -> any:
        """Run on agent action."""
        tool = action.tool
        action_input = action.tool_input
        self.response.add(f"Using *{tool}* with input:\n`{action_input}`")

    def on_tool_end(self, output: str, **kwargs: any) -> any:
        """Run when tool ends running."""
        self.finish_streaming()

    def on_agent_finish(self, finish: AgentFinish, **kwargs: any) -> any:
        """Run on agent end."""
        finish = finish.log
        self.response.add(finish)

    def on_chain_start(
        self, serialized: dict[str, any], inputs: dict[str, any], **kwargs: any
    ) -> any:
        """Run when chain starts running."""
        self.check_for_finished()

    def on_chain_end(self, outputs: dict[str, any], **kwargs: any) -> any:
        """Run when chain ends running."""
        self.finish_streaming()
        self.check_for_finished()

    def on_text(self, text: str, **kwargs: any) -> any:
        """Run on arbitrary text."""
        print("on_text:")
        print(text, kwargs)

    def check_for_finished(self):
        first = self.response.get(0)
        if first and not self.response.finished:
            first.update(
                f"[Processing... {round(time()-self.response.start_time)}s]\n\n{first.content}",
                update_content=False,
            )
