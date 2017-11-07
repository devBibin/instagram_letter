from utils import *
import matplotlib
matplotlib.use('Agg')
from scipy.interpolate import spline
from matplotlib import pyplot as plt
from matplotlib import cm

import numpy as np
import os


def create_activity_dinamics(media, type, interval_count, username, clr="b"):
	if (len(media) == 0):
		return False
	
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
	
	delta = max(y_sm) - min(y_sm)

	plt.xticks(x, x_labels, rotation=5)
	#plt.title("Dynamic of "+type+" on your profile")
	plt.xlabel('Time')
	plt.ylabel('Average count of '+type)
		

	plt.plot(x_smooth, y_smooth, color=clr)
	
	# Annotate
	a_clr = ""
	for i in range(len(x)):
		plt.scatter(x[i],y[i],s=10, color=clr)
		if (i > 0):
			text = str("%.1f" %((y[i]/get_mediana(media[0:i],"likes")-1)*100))+"%"
			if (y[i]/y[i-1]-1 > 0):
				a_clr = "g"
			else:
				a_clr = "r"
		else:
			text = ""
		plt.annotate(text, xy=(x[i]-0.15,y[i]+delta*0.05), textcoords='data', color = a_clr)
	
	plt.ylim(min(y_sm) - delta * 0.4, max(y_sm) + delta * 0.4)
	plt.savefig("appletter/static/appletter/grapdyn_"+type+"_"+username+".jpg",
		dpi=199, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()
	return True

def create_video_percantege_chart(media, username):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	labels = 'Videos', 'Photos'
	v_percentage = get_video_percent(media)
	sizes = [v_percentage, 100 - v_percentage]

	fig1, ax1 = plt.subplots()
	ax1.set_color_cycle(['y', 'b'])
	ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
	        shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	plt.savefig("appletter/static/appletter/video_chart_"+username+".jpg",
		dpi=199, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
	plt.close()