from threading import Event

def setInterval(func, time, params = None):
    event = Event()

    while not event.wait(time):
        if params is not None:
            # spread the iterable to the function
            func(*params)
        else:
            func()