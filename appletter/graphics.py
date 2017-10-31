from utils import *
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from scipy.interpolate import spline
import numpy as np

def create_activity_dinamics(media, type, interval_count, username):
	sorted_media = sorted(media, key=lambda k: k["created_time"], reverse = False)
	splitted_list = list(iter_baskets_contiguous(sorted_media,interval_count))
	
	x = range(interval_count)
	x_labels = []
	y = []


	for l in splitted_list:
		x_labels.append(get_formated_time(float(l[len(l)-1]["created_time"])))
		y.append(get_mediana(l,type))

	x_sm = np.array(x)
	y_sm = np.array(y)
	x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
	y_smooth = spline(x, y, x_smooth)
	
	plt.xticks(x, x_labels, rotation='horizontal')
	plt.title("Dynamic of "+type+" on your profile")
	plt.plot(x_smooth, y_smooth)
	plt.xlabel('Time')
	plt.ylabel('Average count of likes')
	plt.savefig("appletter/static/appletter/grapdyn_"+type+"_"+username+".jpg", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()