from base64 import b64decode


def time(seconds) -> str:
    minutes, remainder = divmod(int(seconds), 60)
    return f"{minutes}m {remainder}s" if minutes > 0 else f"{remainder}s"


def sources(source_documents: list[str]) -> str:
    if not source_documents:
        return "*No Sources*"
    sources = [source.metadata["url"] for source in source_documents]

    links = ", ".join([f"<{source}|{index+1}>" for index, source in enumerate(sources)])
    return f"{links}"


def error(error) -> str:
    return f":robot_face: Sorry, I can't answer that...\n\n*{type(error).__name__}*\n{error}"
