# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.conf import settings
import requests
import json 
import datetime
import time
from appletter.utils import *
from appletter.graphics import *


MIN_PUBS_COUNT = 6
GRAPHS_INTERVAL_COUNT = 6
MIN_VIDEO_PERC = -1

def create_letter(request, user_name):
    r = requests.get("https://www.instagram.com/"+user_name+"/?__a=1")
    if (r.status_code == 200):
        data = r.json()
        common_data = data["user"]

        start = time.time()
        
        # Dictionary for letter
        d = {}
        d["username"] = user_name
        d["user_id"] = common_data["id"]
        d["followers"] = common_data["followed_by"]["count"]
        d["follows"] = common_data["follows"]["count"]
        d["full_name"] = common_data["full_name"]
        d["publication_count"] = common_data["media"]["count"]

        # Count of publications is not enough (< defined count of pubs)
        if (d["publication_count"] < MIN_PUBS_COUNT):
            return HttpResponseForbidden(u"Not enough publications: "+ str(d["publication_count"]))


        media = get_all_media(d["user_id"])
        # Profile doesn't exist
        if (media == None):
            return HttpResponseForbidden(u"Profile is private")
        
        # Total of creating array
        d["load_time"] = get_formated_time(time.time()-start, '%M:%S.%f')
        
        # Calculate mediana of each kind of user activity
        d["average_likes"] = "%.2f" %get_mediana(media, "likes")
        d["average_comments"] = "%.2f" %get_mediana(media, "comments")
        if (get_video_count(media) != 0):
            d["average_views"] = "%.2f" %get_mediana(get_videos(media), "views")

        d["likes_to_comments"] = 100/get_mediana(media, "likes")/get_mediana(media, "comments")
        # Get top pubs for each kind of activity
        # 3rd parameter - count of returned media  
        d["top_likes"] = get_top(media, "likes", 5, user_name)
        d["top_comments"] = get_top(media, "comments", 5, user_name)
        d["top_views"] = get_top(get_videos(media), "views", 5, user_name)

        # Get top1 media for each kin of activity
        d["top1_likes"] = d["top_likes"][0]
        d["top1_comments"] = d["top_comments"][0]
        if (d["top_views"] and len(d["top_views"]) > 2):
            d["top1_views"] = d["top_views"][0]


        # Create likes dynamics graph
        create_activity_dinamics(media, "likes", GRAPHS_INTERVAL_COUNT, user_name, "b")
        d["activity_likes_graph"] = "appletter/grapdyn_likes_"+user_name+".jpg"

        # Create comments dynamic graph
        #create_activity_dinamics(media, "comments", GRAPHS_INTERVAL_COUNT, user_name, "b")
        #d["activity_comments_graph"] = "appletter/grapdyn_comments_"+user_name+".jpg"
        
        # Create views dynamic graph
        #if (len(get_videos(media)) > GRAPHS_INTERVAL_COUNT):
        #    create_activity_dinamics(get_videos(media), "views", GRAPHS_INTERVAL_COUNT, user_name, "y")
        #    d["activity_views_graph"] = "appletter/grapdyn_views_"+user_name+".jpg"


        if (get_video_percent(media) > MIN_VIDEO_PERC):
            create_video_percantege_chart(media, user_name)
            d["video_chart"] = "appletter/video_chart_"+user_name+".jpg"
        
        # Total time of computing
        d["total_time"] = get_formated_time(time.time()-start, '%M:%S.%f')
        return render(request, 'appletter/letter.html', {"input":d})
    else:
        return HttpResponseBadRequest(u"Haven't found profile")


