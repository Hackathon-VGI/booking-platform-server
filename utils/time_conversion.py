def time_in_seconds(time):
    splitted_time = time.split(":")
    hours = int(splitted_time[0])
    mins = int(splitted_time[1])
    seconds = int(splitted_time[2])

    time_seconds = (hours*3600) + (mins*60) + (seconds)
    return time_seconds


def adjust_time(time_str):
    parts = time_str.split(":")
    hours = int(parts[0])
    if hours >= 24:
        hours -= 24
        parts[0] = f"{hours:02d}"
    return ":".join(parts)