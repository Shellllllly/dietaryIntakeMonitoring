import csv
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
import os
import time

def upscale(processed, l, r, th):
	for i in range(l, r+1):
		processed[i]*=th
	return processed

def downscale(processed, l, r, th):
	for i in range(l, r+1):
		processed[i]*=th
	return processed

def post(weights, file):
	processed = weights[:]
	for i in range(len(weights)):
		# TIME
		image_name = str(file[i][1])
		image_path = args.imgs + image_name
		ttttt = time.localtime(os.path.getmtime(image_path))
		hh = ttttt.tm_hour - 14
		if hh<0:
			hh = hh + 24
		mi = ttttt.tm_min
		img_time = hh*100 + mi
		if img_time>1415 and img_time<1630:
			processed[i]*=0.8

		# CONTINUOUTY
		if i-5>=0:
			l = i-5
		else:
			l = 0
		if i+5<len(weights):
			r = i+5
		else:
			r = len(weights)-1
		sub = sum(weights[l:r])
		if sub<3.3:
			processed[i] = 0.1

		# DENSITY
		if i-10>=0:
			prev = i-10
		else:
			prev = 0
		if i+10<len(weights):
			nxt = i+10
		else:
			nxt = len(weights)-1
		prob = sum(weights[prev:nxt])/(nxt-prev+1)
		if prob>0.4:
			upscale(processed, prev, nxt, 1.2)
		elif prob<0.3:
			downscale(processed, prev, nxt, 0.8)


	return processed

# gd = pd.read_excel('hh10_aim_boy_798.xlsx', sheet_name='Sheet1').values.tolist()
# preds = pd.read_csv('labelNum.csv').values.tolist()
def main(filename):
	file = pd.read_excel(filename, sheet_name='Sheet1').values.tolist()

	total = 0
	gd_label = []
	preds_label = []
	weights = []

	ori = 0

	for i in range(len(file)):
		total+=1
		target = int(file[i][2])
		pred = int(file[i][0])

		gd_label.append(target)
		if pred>0:
			preds_label.append(1)
			weights.append(0.7)
			ori+=1
		else:
			preds_label.append(0)
			weights.append(0.2)

	processedLabelFile = 'output.csv'

	if os.path.exists(processedLabelFile):
		os.remove(processedLabelFile)
	det_file = open(processedLabelFile, 'a', newline='')
	fieldnames = ['label']
	writer = csv.DictWriter(det_file, fieldnames=fieldnames)
	writer.writeheader()

	processed = post(weights, file)
	for i in range(len(processed)):
		# print(processed[i], weights[i])
		if processed[i]>0.7:
			writer.writerow({'label': 1})
			processed[i] = 1
		else:
			writer.writerow({'label': 0})
			processed[i] = 0


	# print(len(gd_label))
	print(len(preds_label))
	print(ori)

	conf = confusion_matrix(gd_label, preds_label, labels=[1, 0])
	tp, fn, fp, tn = conf.ravel()
	precision = tp/(tp+fp)
	recall = tp/(tp+fn)
	f1 = 2*((precision*recall)/(precision+recall))
	acc = accuracy_score(gd_label, preds_label)

	print("---------------------------- before ----------------------------")
	print("Total #images: {}".format(total))
	print("confusion matrix: \n{}".format(conf))
	print("precision: {}".format(precision))
	print("recall: {}".format(recall))
	print("f1: {}".format(f1))
	print("acc: {}".format(acc))
	print("---------------------------- end ----------------------------")

	conf2 = confusion_matrix(gd_label, processed, labels=[1, 0])
	tp2, fn2, fp2, tn2 = conf2.ravel()
	precision2 = tp2/(tp2+fp2)
	recall2 = tp2/(tp2+fn2)
	f12 = 2*((precision2*recall2)/(precision2+recall2))
	acc2 = accuracy_score(gd_label, processed)
	print('---------------------------- after ----------------------------')
	print("Total #images: {}".format(total))
	print("confusion matrix: \n{}".format(conf2))
	print("precision: {}".format(precision2))
	print("recall: {}".format(recall2))
	print("f1: {}".format(f12))
	print("acc: {}".format(acc2))
	print('---------------------------- end ----------------------------')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='path to label file')
    parser.add_argument('imgs', type=str, help='path to image directory')
    args = parser.parse_args()
    main(args.file)

