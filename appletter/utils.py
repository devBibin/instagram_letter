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
            temp_media_json = {}
            temp_media_json = r.json()

            for el in temp_media_json["data"]:
                node = {}
                node["count"] = get_views(el)
                el["views"] = node
                media.append(el)
            
            if (temp_media_json["pagination"] != {}):
                r = requests.get(temp_media_json["pagination"]["next_url"])
            else:
                flag = False
    else:
        return None

    return media

def get_top(media, type, count):
    if (count > len(media)):
        count = len(media)
    sorted_list = sorted(media, key=lambda k: int(k[type]["count"]), reverse = True)
    return json_to_date(sorted_list[0:count])

def get_mediana(media, type):
    if (len(media) == 0):
        return None
    s = 0.0
    for m in media:
        s = s + int(m[type]["count"])
    return s/len(media)

def json_to_date(media):
    for i in range(len(media)):
        media[i]["created_time"] = get_formated_time(int(media[i]["created_time"]))
    return media

def get_formated_time(time):
    return datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')

def get_videos(media):
    videos = []
    for m in media:
        if (m["type"] == "video"):
            videos.append(m)
    return videos

def get_views(m):
    if (m["type"] == "video"):
        r = requests.get(m["link"]+"?__a=1")
        return r.json()["graphql"]["shortcode_media"]["video_view_count"]
    else:
        return -1