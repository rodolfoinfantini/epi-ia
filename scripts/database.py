import pymongo
from datetime import datetime, timezone, timedelta

client = pymongo.MongoClient(
    "mongodb+srv://root:h1E5dIxVZo26CjpW@luster0.enxl3qe.mongodb.net/")
db = client["epi_ia"]
collection = db["alerts"]


def save_alert(alert_class, timestamp, filename):
    timestamp = datetime.strptime(
        timestamp.replace('.mp4', ''), "%Y%m%d_%H%M%S")
    br_tz = timezone(timedelta(hours=-3))
    br_timestamp = timestamp.replace(tzinfo=br_tz)
    alert = {
        "class": alert_class,
        "timestamp": br_timestamp,
        "record": filename,
        "thumb": filename.replace(".mp4", ".png"),
    }

    collection.insert_one(alert)
