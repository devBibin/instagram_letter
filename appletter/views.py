# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import requests
import json 
import datetime
import time
from appletter.utils import *


def create_letter(request, user_name):
    r = requests.get("https://www.instagram.com/"+user_name+"/?__a=1")
    if (r.status_code == 200):
        data = r.json()
        common_data = data["user"]

        start = time.time()
        d = {}

        d["top_likes_img"] = "appletter/likes_"+user_name+".jpg"
        d["top_comments_img"] = "appletter/comments_"+user_name+".jpg"
        d["top_views_img"] = "appletter/views_"+user_name+".jpg"

        d["username"] = user_name
        d["user_id"] = common_data["id"]
        d["followers"] = common_data["followed_by"]["count"]
        d["follows"] = common_data["follows"]["count"]
        d["full_name"] = common_data["full_name"]
        d["publication_count"] = common_data["media"]["count"]

        media = get_all_media(d["user_id"], d["publication_count"])
        if (media == None):
            return HttpResponse("Profile is private")

        d["average_likes"] = get_mediana(media, "likes")
        d["average_comments"] = get_mediana(media, "comments")
        d["average_views"] = get_mediana(get_videos(media), "views")

        d["top_likes"] = get_top(media, "likes", 5, user_name)
        d["top_comments"] = get_top(media, "comments", 5, user_name)
        d["top_views"] = get_top(get_videos(media), "views", 5, user_name)

        d["total_time"] = datetime.datetime.fromtimestamp(time.time()-start).strftime('%M:%S.%f')

        return render(request, 'appletter/index.html', {"input":d})
    else:
        return HttpResponse("User not found")


