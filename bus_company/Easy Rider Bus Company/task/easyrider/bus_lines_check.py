def check_bus_line_info(database):
    stops_per_line = {
        128: set(),
        256: set(),
        512: set()
    }
    for element in database:
        bus_id = element["bus_id"]
        stop_id = element["stop_id"]
        if bus_id in stops_per_line:
            stops_per_line[bus_id].add(stop_id)
        else:
            stops_per_line.update({bus_id: {stop_id}})

    print(f"Line names and number of stops:")
    for bus_id, stop_ids in stops_per_line.items():
        print(f"bus_id: {bus_id}, stops: {len(stop_ids)}")