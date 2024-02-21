from app import formatter, llm, slack_client
from app.message import MultipartMessage, Message
from app.callbacks import AgenticCallbackHandler, ConversationalCallbackHandler
from app.config import PLACEHOLDERS
from app.types import ConversationID, ConversationHistory, MessageID
from random import choice
from time import time
from langchain.schema import OutputParserException

histories = ConversationHistory()


async def direct(_: str, __: str, channel: str, ts: str, thread_ts: str):
    content = "*Direct Mode* is not yet fully implemented..."
    slack_client.create(content, channel, thread_ts or ts)


async def conversational(
    prompt: str, initiated_by: str, channel: str, ts: str, thread_ts: str
):
    # setup query and response
    previous_msg = MessageID(channel, ts, thread_ts)
    conversation = ConversationID(previous_msg)
    placeholder = choice(PLACEHOLDERS)
    start_time = time()
    response = Message(placeholder, channel, thread_ts or ts)

    # run query and stream output
    handler = ConversationalCallbackHandler(response)

    query_result = await llm.conversation_chain.acall(
        {"question": prompt, "chat_history": histories.get(conversation)},
        callbacks=[handler],
    )

    # format response for slack
    answer = query_result["answer"]
    sources = formatter.sources(query_result["source_documents"])
    execution_time = formatter.time(time() - start_time)
    formatted_message = f"{answer}\n\n*Generated for <@{initiated_by}> in {execution_time} from sources {sources}*"

    # Update slack with final response
    response.update(formatted_message)

    # Update history
    histories.append(conversation, prompt, answer)


async def agentic(
    prompt: str, initiated_by: str, channel: str, ts: str, thread_ts: str
):
    # channel = event["channel"]
    # ts = thread_ts or ts
    # user = event["user"]

    try:
        response = MultipartMessage(channel, thread_ts or ts, initiated_by)
        handler = AgenticCallbackHandler(response)
        query_result = llm.plan_and_execute_agent.run(input=prompt, callbacks=[handler])
        response.finish()

    # BEGIN CRUDE HACK
    except OutputParserException as e:
        print("WARN: Using crude hack to parse LLM output\n", e)
        query_result = str(e)
        if not query_result.startswith("Could not parse LLM output: `"):
            raise e
        query_result = query_result.removeprefix(
            "Could not parse LLM output: `"
        ).removesuffix("`")
    # END CRUDE HACK
