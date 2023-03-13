import flask as fl
import requests
import xmltodict
import json
from datetime import datetime, timedelta

import utils


so = fl.Blueprint("so", __name__)






@so.route("get-user-events", methods=["GET"])
def get_user_events():
    startlist_id = fl.request.args.get("startlist_id")
    if not startlist_id:
        return utils.error(utils.MISSING_STARTLIST_ID)
    
    request = requests.get(
        "http://skytteonline.se/shooter/!display",
        params={
            "action": "section",
            "id": 6343,
            "start_list_id": startlist_id,
        }   
    )

    try:
        raw_data = xmltodict.parse(request.text)["rows"]["row"]
    except Exception as e:
        return utils.error(utils.FAILED_TO_PARSE_XML)
    
    result = []
    for event in raw_data:
        result.append({
            "id": int(event.get("ID").split("-")[0]),
            "location": event.get("LOCATION"),
            "date": event.get("EVENT_DATE"),
            "primary_score": float(event.get("SCORE_TOT40")),
            "secondary_score": float(event.get("SCORE_DEC40")),
        })
    return fl.jsonify(result)
    
@so.route("query-users", methods=["GET"])
def query_users():
    query = fl.request.args.get("query")
    if not query:
        return utils.error("Missing query")
    elif len(query) < 3:
        return utils.error("Query must be at least 3 characters long")
    
    request = requests.get(
        "http://skytteonline.se/shooter/!display",
        params={
            "action": "section",
            "id": 6771,
            "term": query,
        }
    )

    if request.text.contains("ORA-20001"):
        return utils.error("Query failed")

    return fl.jsonify(json.loads(request.text))


@so.route("get-shots", methods=["GET"])
def get_shots():
    startlist_id = fl.request.args.get("startlist_id")
    if not startlist_id:
        return utils.error(utils.MISSING_STARTLIST_ID)

    request = requests.get(
        "http://skytteonline.se/shooter/!display",
        params={
            "action": "section",
            "id": 6347,
            "start_list_id": startlist_id,
        }
    )

    try:
        raw_data = xmltodict.parse(request.text)["rows"]["row"]
    except Exception as e:
        return utils.error(utils.FAILED_TO_PARSE_XML)
    
    result = []
    for i, shot in enumerate(raw_data):
        time: timedelta
        if i == 0:
            time = timedelta()
        else:
            time = utils.sotime_to_datetime(shot.get("TIME_MARK")) - utils.sotime_to_datetime(raw_data[i-1].get("TIME_MARK"))

        result.append({
            "number": int(shot.get("POS")),
            "primary_score": float(shot.get("PRIMARY_SCORE")),
            "secondary_score": float(shot.get("SECONDARY_SCORE")),
            "type": shot.get("SHOOT"),
            "series": shot.get("MOD10"),
            "timestamp": utils.sotime_to_datetime(shot.get("TIME_MARK")).strftime(utils.TIME_FORMAT),
            "time": str(time),
            "x_pos": float(shot.get("X")),
            "y_pos": float(shot.get("Y")),
        })
    
    return fl.jsonify(result)


    