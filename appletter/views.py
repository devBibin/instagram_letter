# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import requests
import json 
import datetime
import time
from utils import *


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


