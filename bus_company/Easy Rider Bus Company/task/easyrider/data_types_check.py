def check_data_types(database):
    error_counts = {
        'bus_id': 0,
        'stop_id': 0,
        'stop_name': 0,
        'next_stop': 0,
        'stop_type': 0,
        'a_time': 0
    }

    for element in database:
        for key, value in element.items():
            if key in ['bus_id', 'stop_id', 'next_stop'] and type(value) is not int:
                error_counts[key] += 1
            elif key in ['stop_name', 'stop_type', 'a_time'] and type(value) is not str:
                error_counts[key] += 1
            elif key == 'stop_type' and type(value) is str and len(value) > 1:
                error_counts[key] += 1
            elif key != 'stop_type' and type(value) is str and len(value) == 0:
                error_counts[key] += 1

    total_error = 0
    for _, value in error_counts.items():
        total_error += value

    print(f"Type and required field validation: {total_error} errors")
    for key, value in error_counts.items():
        print(f"{key}: {value}")
