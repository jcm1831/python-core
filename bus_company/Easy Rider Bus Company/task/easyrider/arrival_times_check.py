from busline_extraction import extract_bus_lines


def check_arrival_times(database):
    bus_lines = extract_bus_lines(database)
    anomalies = {}

    for bus_id in bus_lines:
        arrival_times = bus_lines[bus_id]["a_times"]
        adjacent_times = zip(arrival_times, arrival_times[1:])
        for idx, time_pair in enumerate(adjacent_times):
            diff = (time_pair[1] - time_pair[0]).total_seconds()
            if diff <= 0:
                anomalies.update({bus_id: bus_lines[bus_id]["stop_names"][idx + 1]})
                break

    print("Arrival time test:")
    if len(anomalies) == 0:
        print("OK")
    else:
        for bus_id, stop_name in anomalies.items():
            print(f"bus_id line {bus_id}: wrong time on station {stop_name}")
