import json

with open("./sample_data/players_id.json", "r") as json_file:
    player_ids = json.load(json_file)

def find_ids(name):
    id_list = []
    for i in player_ids:
        for j in i.values():
            if j["이름"] == name:
                id_list.append(j["ID"])
    return list(set(id_list))

def change_sigle_name_to_id(data,name):
    id_list = find_ids(name)
    if len(id_list) == 1:
        return id_list[0]
    else:
        return "동명이인이 존재하는 이름입니다."