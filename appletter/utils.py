import requests
import json 
import datetime
import time

TOKEN = "5357446710.0be8de7.e8bbb791ba7f4ffdbc44ef1977cd49a3"

def get_all_media(user_id, cnt):
    r = requests.get("https://api.instagram.com/v1/users/"+user_id+"/media/recent/?count=20&access_token="+TOKEN)
    if (r.json()["meta"]["code"] == 200):
        media = []
        recievied_count = 0
        flag = True
        while (flag):
            temp_media_json = r.json()

            for el in temp_media_json["data"]:
                media.append(el)
            
            if (temp_media_json["pagination"] != {}):
                r = requests.get(temp_media_json["pagination"]["next_url"])
            else:
                flag = False
    else:
        return None

    return media

def get_top(media, type, count):
    sorted_list = sorted(media, key=lambda k: int(k[type]["count"]), reverse = True)
    return json_to_date(sorted_list[0:count])

def json_to_date(media):
    for i in range(len(media)):
        media[i]["created_time"] = datetime.datetime.fromtimestamp(int(media[i]["created_time"])).strftime('%Y-%m-%d %H:%M:%S')
    return media