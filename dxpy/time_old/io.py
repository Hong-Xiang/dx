from time import gmtime, strftime

def readable_duration(time_delta):
    if time_delta < 60.0:
        msg_run = "{:.3f} secs".format(time_delta)
    elif time_delta < 60.0*60.0:
        msg_run = strftime("%M mins, %S secs", gmtime(time_delta))
    elif time_delta < 60.0*60.0*24.0:
        msg_run = strftime("%H hurs, %M mins, %S secs", gmtime(time_delta))
    else:
        msg_run = strftime("%d d, %H h, %M m, %S s", gmtime(time_delta))
    return msg_run