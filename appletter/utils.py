import requests
import json 
import datetime
import time
import urllib

TOKEN = "5357446710.0be8de7.e8bbb791ba7f4ffdbc44ef1977cd49a3"

# Get all media from instagram
def get_all_media(user_id):
    r = requests.get("https://api.instagram.com/v1/users/"+user_id+"/media/recent/?count=33&access_token="+TOKEN)
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

# Get top by "type" criteria (for example likes)
def get_top(media, type, count, username):
    if (len(media) != 0):
        if (count > len(media)):
            count = len(media)
        
        sorted_list = sorted(media, key=lambda k: int(k[type]["count"]), reverse = True)
        return sorted_list[0:count]
    else:
        return None

# Get mediana by "type" criteria (for example likes)
def get_mediana(media, type):
    if (len(media) == 0):
        return None
    s = 0.0
    for m in media:
        s = s + int(m[type]["count"])
    return s/len(media)

# Get formated time from unix timestamp
def get_formated_time(time, fmt = '%Y-%m-%d'):
    return datetime.datetime.fromtimestamp(float(time)).strftime(fmt)

# Convert seconds to days
def convert_to_days(time_delta):
    return int(time_delta/3600/24)

# Get date of the first publication
def get_first_publication_date(media):
    return get_formated_time(sorted(media, key=lambda k: float(k["created_time"]), reverse = False)[0]["created_time"])

# Get count of days from the moment of the first publication
def get_days_from_first_pub(media):
    return convert_to_days(time.time() - float(sorted(media, key=lambda k: float(k["created_time"]), reverse = False)[0]["created_time"]))

# Get all videos from media    
def get_videos(media):
    videos = []
    for m in media:
        if (m["type"] == "video"):
            videos.append(m)
    return videos

# Get count of views for each media (explore used because API doesn't provide with views count)
def get_views(m):
    if (m["type"] == "video"):
        r = requests.get(m["link"]+"?__a=1")
        return r.json()["graphql"]["shortcode_media"]["video_view_count"]
    else:
        return -1

# Get annotation type for dynamics of "type" activite
# 0 - OK
# 1 - Drop on the last period
# 2 - Dynamics getting slower
def get_dynamic_message(media, type, interval_count):
    sorted_media = sorted(media, key=lambda k: k["created_time"], reverse = False)
    splitted_list = list(iter_baskets_contiguous(sorted_media,interval_count))
    y = []
    for l in splitted_list:
        y.append(get_mediana(l,type))

    per = [] # percantage of dynamics   
    for i in range(len(y)):
        if (i > 0):
            per.append(y[i]/y[i-1]-1)
   
    # if last element below zero then popularity drop
    if (per[len(per) -1] < 0):
        return 1
    # dynamics drop 
    if (per[len(per)-1] - per[len(per)-2] < -0.2) and (per[len(per) -1] < 0.15):
        return 2
    return 0

# Get count of videos
def get_video_count(media):
    return len(get_videos(media))

# Get percantage of videos
def get_video_percent(media):
    return 100.*get_video_count(media)/len(media)

#generates balanced baskets from iterable, contiguous contents provide item_count if providing a iterator that doesn't support len()
def iter_baskets_contiguous(items, maxbaskets):
    item_count = len(items)
    baskets = min(item_count, maxbaskets)
    items = iter(items)
    floor = item_count // baskets 
    ceiling = floor + 1
    stepdown = item_count % baskets
    for x_i in xrange(baskets):
        length = ceiling if x_i < stepdown else floor
        yield [items.next() for _ in xrange(length)]