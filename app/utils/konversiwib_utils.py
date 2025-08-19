
from datetime import datetime, timezone
import pytz

def konversi_wib(dt_utc):
    if not isinstance(dt_utc, datetime):
        return dt_utc
    if dt_utc.tzinfo is None:
        dt_utc = dt_utc.replace(tzinfo=timezone.utc)
    wib = pytz.timezone("Asia/Jakarta")
    return dt_utc.astimezone(wib).strftime('%Y-%m-%d %H:%M:%S')