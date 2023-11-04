import re


def check_stop_name(stop_name):
    pattern = r'^([A-Z][a-z]+ )+(Road|Avenue|Boulevard|Street)$'
    return check_impl(pattern, stop_name)


def check_stop_type(stop_type):
    if stop_type == "":
        return 0
    pattern = r'^(S|O|F)$'
    return check_impl(pattern, stop_type)


def check_arrival_time(arrival_time):
    pattern = r'^([0-2]\d:[0-5]\d)$'
    return check_impl(pattern, arrival_time)


def check_impl(pattern, string):
    match = re.match(pattern, string)
    return 0 if match else 1


def check_correct_syntax(database):
    error_counts = {
        'stop_name': 0,
        'stop_type': 0,
        'a_time': 0
    }
    for element in database:
        for key, value in element.items():
            if key == 'stop_name':
                error_counts[key] += check_stop_name(value)
            elif key == 'stop_type':
                error_counts[key] += check_stop_type(value)
            elif key == 'a_time':
                error_counts[key] += check_arrival_time(value)

    total_error = 0
    for _, value in error_counts.items():
        total_error += value

    print(f"Format validation: {total_error} errors")
    for key, value in error_counts.items():
        print(f"{key}: {value}")
