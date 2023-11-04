from datetime import datetime


def extract_bus_lines(database):
    bus_lines = {}
    for element in database:
        bus_id = element["bus_id"]
        if bus_id not in bus_lines:
            bus_lines.update({bus_id: {
                "stop_ids": [],
                "stop_names": [],
                "next_stops": [],
                "stop_types": [],
                "a_times": []
            }})
        bus_lines[bus_id]["stop_ids"].append(element["stop_id"])
        bus_lines[bus_id]["stop_names"].append(element["stop_name"])
        bus_lines[bus_id]["next_stops"].append(element["next_stop"])
        bus_lines[bus_id]["stop_types"].append(element["stop_type"])
        bus_lines[bus_id]["a_times"].append(datetime.strptime(element["a_time"], '%H:%M'))
    return bus_lines


def extract_stops(database):
    stops = []
    for element in database:
        stops.append(element["stop_name"])
    return stops


def extract_stop_types(database):
    stop_types = []
    for element in database:
        stop_types.append(element["stop_type"])
    return stop_types
