from datetime import datetime, timezone

def snowflake_time(id: int, /) -> datetime:
    timestamp = ((id >> 22) + 1420070400000) / 1000
    return datetime.fromtimestamp(timestamp)