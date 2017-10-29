# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import requests
import json 
import datetime
import time

TOKEN = "5357446710.0be8de7.e8bbb791ba7f4ffdbc44ef1977cd49a3"

def get_all_media(user_id, cnt):
    r = requests.get("https://api.instagram.com/v1/users/"+user_id+"/media/recent/?count=20&access_token="+TOKEN)
    print r.json()["meta"]["code"]
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

def create_letter(request, user_name):
    r = requests.get("https://www.instagram.com/"+user_name+"/?__a=1")
    if (r.status_code == 200):
        data = r.json()
        common_data = data["user"]

        d = {}

        d["user_id"] = common_data["id"]
        d["followers"] = common_data["followed_by"]["count"]
        d["follows"] = common_data["follows"]["count"]
        d["full_name"] = common_data["full_name"]
        d["publication_count"] = common_data["media"]["count"]

        media = get_all_media(d["user_id"], d["publication_count"])
        if (media == None):
            return HttpResponse("Profile is private")

        d["top_likes"] = get_top(media, "likes", 5)
        d["top_comments"] = get_top(media, "comments", 5)

        return render(request, 'appletter/index.html', {"input":d})
    else:
        return HttpResponse("User not found")


