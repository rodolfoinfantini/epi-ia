import pymongo
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os

load_dotenv()

client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = client["epi_ia"]
collection = db["alerts"]


def save_alert(alert_class, timestamp, filename):
    timestamp = datetime.strptime(
        timestamp.replace('.webm', ''), "%Y%m%d_%H%M%S")
    br_tz = timezone(timedelta(hours=-3))
    br_timestamp = timestamp.replace(tzinfo=br_tz)
    alert = {
        "class": alert_class,
        "timestamp": br_timestamp,
        "record": filename,
        "thumb": filename.replace(".webm", ".png"),
    }

    collection.insert_one(alert)
