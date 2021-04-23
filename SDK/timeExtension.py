import time
from datetime import datetime

import pytz


class Timestamp(object):
    def __init__(self, timestamp, sync_tz = "Europe/Moscow"):
        self.sync_tz = sync_tz
        self.timestamp = timestamp
        zrh = pytz.timezone(self.sync_tz)
        tztime = zrh.localize(datetime.fromtimestamp(self.timestamp))
        tzfloat = (tztime - datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds()
        self.diff = timestamp - tzfloat

    def get_time(self):
        return self.timestamp + self.diff

    def __float__(self):
        return self.get_time()

    def passed(self):
        return time.time() >= self.get_time()

    @staticmethod
    def now():
        return Timestamp(time.time())
    
    def prettyprint(self):
        return datetime.fromtimestamp(self.get_time()).strftime("%Y/%m/%d %H:%M:%S")