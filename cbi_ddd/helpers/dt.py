from datetime import datetime

from pytz import timezone


class DateTimeHelper:
    @classmethod
    def utcnow(cls):
        return datetime.now(timezone('UTC'))
