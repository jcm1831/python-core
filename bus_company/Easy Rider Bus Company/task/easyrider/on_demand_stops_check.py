from data_extraction import extract_bus_lines
from special_stops_check import get_transfer_stops, get_starting_stops, get_final_stops


def check_on_demand_stops(database):
    bus_lines = extract_bus_lines(database)
    starting_stops, stypes_starting = get_starting_stops(bus_lines)
    transfer_stops, stypes_transfer = get_transfer_stops(database)
    final_stops, stypes_final = get_final_stops(bus_lines)

    anomalies = []
    stops = starting_stops + transfer_stops + final_stops
    stypes = stypes_starting + stypes_transfer + stypes_final
    for stop, stype in zip(stops, stypes):
        if stype == "O":
            anomalies.append(stop)

    print("On demand stops test:")
    if len(anomalies) == 0:
        print("OK")
    else:
        print(f"Wrong stop type: {sorted(anomalies)}")
