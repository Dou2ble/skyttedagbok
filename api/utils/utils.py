import datetime
from datetime import datetime, timedelta
import flask as fl

TIME_FORMAT = "%H:%M:%S.%f"

def sotime_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, TIME_FORMAT)



def error(message: str) -> fl.Response:
    return fl.jsonify({"error": message})
MISSING_STARTLIST_ID = "Missing startlist_id"
FAILED_TO_PARSE_XML = "Failed to parse XML data from Skytteonline"