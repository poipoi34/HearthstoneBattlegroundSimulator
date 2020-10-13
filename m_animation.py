from time import time

class animation:
    
    def __init__(o):
        o.start_time = time()
        o.time_dependant = True
        o.frame_time = 16

    def elapsed_time(time_dependant):
        if time_dependant:
            return time() - o.start_time
        if not time_dependant:
            return int(time() - o.start_time)

    def jump_frame(o):
        if (o.time_dependant):
            o.update(elapsed_time())
        if not o.time_dependant:
            if start_time > o.frame_time:
                start_time = time() - time() % o.frame_time
                current_frame += 1
                o.update(current_frame)


