import datetime

def display():
    current_time = datetime.datetime.now()
    year = current_time.year
    month = current_time.month
    day = current_time.day
    hours = current_time.hour
    minutes = current_time.minute
    seconds = current_time.second

    displaydate = f"{day}:{month}:{year}"
    displaytime = f"{hours}:{minutes}:{seconds}"
    return displaytime,displaydate ;
