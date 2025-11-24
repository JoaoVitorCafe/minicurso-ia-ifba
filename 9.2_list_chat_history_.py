from langgraph.checkpoint.postgres import PostgresSaver
from urllib.parse import quote
import json

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5433"
POSTGRES_DATABASE = "DB_IFBA"

conn_string = (
    f"postgresql://{POSTGRES_USER}:{quote(POSTGRES_PASSWORD)}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
)

with PostgresSaver.from_conn_string(conn_string) as memory:
    memory.setup()

    config = {"configurable": {"thread_id": "3"}}

    checkpoints = list(memory.list(config))

    all_messages = []

    for checkpoint_tuple in checkpoints:
        checkpoint_state = checkpoint_tuple.checkpoint

        channel_values = checkpoint_state.get("channel_values", {})
        messages = channel_values.get("messages", [])

        for msg in messages:
            msg_type = getattr(msg, "type", None)
            msg_content = getattr(msg, "content", None)

            all_messages.append({
                "type": msg_type,
                "content": msg_content
            })

    print(json.dumps(all_messages, indent=2, ensure_ascii=False))

