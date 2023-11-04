from data_extraction import extract_bus_lines, extract_stops, extract_stop_types


def get_stop_types(bus_lines):
    starting_stops, final_stops = [], []
    for bus_id in bus_lines:
        stop_types = bus_lines[bus_id]["stop_types"]
        if stop_types.count('S') != 1 or stop_types.count('F') != 1:
            print(f"There is no start or end stop for the line: {bus_id}.")
            raise ValueError
        else:
            stop_names = bus_lines[bus_id]["stop_names"]
            starting_stops.append(stop_names[0])
            final_stops.append(stop_names[-1])
    return starting_stops, final_stops


def get_starting_stops(bus_lines):
    starting_stops, stop_types = [], []
    for bus_id in bus_lines:
        stypes = bus_lines[bus_id]["stop_types"]
        stop_names = bus_lines[bus_id]["stop_names"]
        starting_stops.append(stop_names[0])
        stop_types.append(stypes[0])
    return starting_stops, stop_types


def get_final_stops(bus_lines):
    final_stops, stop_types = [], []
    for bus_id in bus_lines:
        stypes = bus_lines[bus_id]["stop_types"]
        stop_names = bus_lines[bus_id]["stop_names"]
        final_stops.append(stop_names[-1])
        stop_types.append(stypes[-1])
    return final_stops, stop_types


def get_transfer_stops(database):
    stops = extract_stops(database)
    stypes = extract_stop_types(database)
    transfer_stops, stop_types = [], []
    unique_stops = set()

    for stop, stype in zip(stops, stypes):
        if stop not in unique_stops:
            unique_stops.add(stop)
        else:
            transfer_stops.append(stop)
            stop_types.append(stype)

    for stop, stype in zip(stops, stypes):
        if stop in transfer_stops and stype == "O":
            stop_types[transfer_stops.index(stop)] = stype

    return transfer_stops, stop_types


def check_special_stops(database):
    # determine stop types
    try:
        starting_stops, final_stops = get_stop_types(extract_bus_lines(database))
    except ValueError:
        return

    # determine transfer stops
    transfer_stops = get_transfer_stops(database)

    # print results
    print(f"Start stops: {len(starting_stops)} {sorted(starting_stops)}")
    print(f"Transfer stops: {len(transfer_stops)} {sorted(transfer_stops)}")
    print(f"Finish stops: {len(final_stops)} {sorted(final_stops)}")
