import json
from m_displayer import Displayer
import m_interfaces

class Battle_manager(object):
    def __init__(o, json_dict = None):
        o.env = {}
        o.displayer = Displayer(o)
        if json_dict != None:
            o.battle_data = [m_interfaces.Board_interface(board, env) for board in json_dict["data"]]
            

    def read_json(o, json_dict):
        o.battle_data = [m_interfaces.Board_interface(board, o.env) for board in json_dict["data"]]

    def read_json_file(o, file_path_name):
        with open(file_path_name) as json_file:
            json_dict = json.load(json_file)
        o.read_json(json_dict)
        
    def print_env(o):
        p_env = {}
        for id in o.env:
            p_env[id_to_str(id)] = o.env[id]
        print(p_env)
    def play(o):
        o.displayer.play(o.battle_data)
def id_to_str(id):
	res = str(hex(id))
	return '@' + res[len(res)-5:len(res)]

