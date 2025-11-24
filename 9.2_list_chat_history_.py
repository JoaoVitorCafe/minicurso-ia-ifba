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

    last_checkpoint = checkpoints[0]
    last_checkpoint_state = last_checkpoint.checkpoint
    last_checkpoint_channel_values = last_checkpoint_state.get("channel_values", {})
    last_checkpoint_messages = last_checkpoint_channel_values.get("messages", [])
    for msg in last_checkpoint_messages:
        all_messages.append({
            "type": msg.type,
            "content": msg.content
        })

    print(json.dumps(all_messages, indent=2, ensure_ascii=False))

