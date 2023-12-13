from datetime import datetime
from zoneinfo import ZoneInfo


def get_local_timestamp():
    return datetime.now(tz=ZoneInfo("Asia/Seoul"))
