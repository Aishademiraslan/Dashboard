from datetime import datetime, timedelta

def api_modular_time(hours_offset:int, minutes_offset:int, futurepast:str):
    '''
    Outputs a datetime string with a T divider between date and time
    Used to get an end time to input into the Emissions and Emissions Prognosis APIs
    
    Parameters
    ----------
    hours_offset : int
        Hours to offset time by
    minutes_offset : int
        Minutes to offset time by
    futurepast : str
        Go back or forwards in time
    '''
    now = datetime.now()
    if futurepast == "future":
        new_time = str(now + timedelta(hours=hours_offset))
    elif futurepast == "past":
        new_time = str(now - timedelta(hours=hours_offset, minutes=minutes_offset))
    new_time = list(new_time)[:-10]
    new_time = "".join(new_time)
    new_time = new_time.replace(" ", "T")
    # print(nine_hours_later)
    return new_time

def time_reformat(time):
    if len(time)>16:
        formatted = list(time)[:16]
        formatted = "".join(formatted)
    formatted = formatted.replace("T", " ")
    return formatted


def cut_off_at_minutes(data):
    for i in range(len(data)):
        j = list(data[i])
        timestamp = j[2][:16]
        time = j[4][:5]
        j[2] = timestamp
        j[4] = time
        data[i] = tuple(j)
    return data
