from time import time

class chrono:
    def __init__(o):
        o.elasped_time = None
        o.start_time = None

    def start(o):
        o.start_time = time()

    def elapsed_time(o):
        return time() - o.start_time

    def stop():
        o.elapsed_time = time() - o.start_time

    def resume():
        o.start_time = time() - o.elapsed_time #restart on time en ajoutant le elapsed deja elapsé

    def rewind(ms):
        o.start_time - ms


class animation2:
    
    def __init__(o, displayer):
        o.chrono = Chrono()
        o.frame_time = 16
        o.displayer = displayer

        
    def start_animation(o, event):
        if event.event_type == "on_minion_attack":
            displayer.get_pos(event.param["attacking"])
            displayer.get_pos(event.param["attacked"])
            displayer.changing_object = [id(event.param["attacking"]), event.param["attacked"]]


        o.chrono.start()

    def jump_frame(o, elapsed_time):
        if (o.time_dependant):
            frame_to_jump = chrono.elapsed_time() // o.frame_time
            o.current_frame += frame_to_jump
            o.rewind(frame_to_jump * o.frame_time)
        if not o.time_dependant:
            if (o.chrono.elapsed_time() >= o.frame_time)
                o.current_frame +=1
                o.chrono.start()