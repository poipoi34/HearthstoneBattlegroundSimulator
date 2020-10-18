from m_battle import Battle_manager

battle = Battle_manager()
battle.read_json_file("data.txt")
print(battle.battle_data)
battle.print_env()
battle.play()