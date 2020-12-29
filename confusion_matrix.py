# DEVELOPED BY SAMI KHAN 12/29/2020
# This provides a skeleton to generate a confusion matrix to help measure your model performance.

import pandas as pd 
import csv
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import os
import numpy as np
import mplcursors
from matplotlib.ticker import MultipleLocator
import shutil

def read_dataframes():
	#read original csv and use the model results. Merge it into single column(full_path)
	df = pd.read_csv("original.csv", header=0)
	df = df.fillna("")
	df = df.loc[:,["FULL_PATH", "FILENAME", "SUB_CATEGORY"]]
	df['FULL_PATH'] = df[["FULL_PATH", "FILENAME"]].apply(lambda x: '/'.join(x), axis = 1)
	df["SUB_CATEGORY"] = df["SUB_CATEGORY"].replace('Mudlog Gas Chromatography', 'Composite Geological Log')
	# replace values if necessary
	df["x"] = df["x"].replace('y', 'z')

	#delete columns if necessary
	del df["FILENAME"]

	# read the predicted results that you get from different csv file
	predictions = pd.read_csv("model_prediction_results.csv", header=0)
	predictions = predictions.fillna("")
	# define your own path
	predictions["FULL_PATH"] = predictions["FULL_PATH"].map(lambda x: x.lstrip('/home/xyz/path/...'))
	# replace values if necessary
	predictions["x"] = predictions["x"].replace('y', 'z')
	# merge the two data frames into one csv that will be used to generate the confusion matrix
	merged_dataframes = pd.merge(predictions, bhp, on = "FULL_PATH", how = "inner") 
	merged_dataframes.to_csv("merged_dataframes_new.csv", encoding='utf-8', index=False)

read_dataframes()

#define your labels. This is used to generate the labels that you will see in on your x and y axes of your confusion matrix.
labels = {
	'label_1': 1,
	'label_2': 2,
	}
	
label_list = [k for k in labels.keys()]

labels = {str(v):k for k,v in labels.items()}
root = os.getcwd()

dirpath = os.path.join(root, "merged_dataframes_new.csv")
file = open(dirpath)
csv_reader = csv.reader(file, delimiter = ",")
pred_cat_list = []
old_cat_list = []
for i, row in enumerate(csv_reader):
	if i > 0:
		pred_cat_list.append(row[1])
		old_cat_list.append(row[3])


pred_cat = np.array([r for r in pred_cat_list])
old_cat = np.array([r for r in old_cat_list])

pred_unique =  np.unique(pred_cat)
old_unique = np.unique(old_cat)
print("length of pred_unique", len(pred_unique))
print("length of old_unique", len(old_unique))

missing = [x for x in labels.values() if not x in list(old_unique) + list(pred_unique)]
print("Missing", missing)


## create confusion matrix
np.set_printoptions(precision=2)
comfmat = confusion_matrix(y_true = old_cat, y_pred = pred_cat, labels=label_list,  normalize="true")
accuracies = []
i = 0

for rows in comfmat:
	print(rows[i])
	accuracies.append(round(rows[i], 3))
	i += 1

labels_list  = []
for keys, values in labels.items():
	labels_list.append(values)

with open("accuracies.csv", "w") as file:
	writer = csv.DictWriter(file, fieldnames = ["Category", 
		"accuracy"])
	writer.writeheader()

	for cat, acc in zip(labels_list, accuracies):
		writer.writerow({"Category": cat, 
		"accuracy": acc})	


print(comfmat.shape)


## create subplot
fig, ax = plt.subplots(figsize = (150,150))

## convert 2D matrix of the confusion matrix to color coded image
ax.matshow(comfmat, cmap=plt.cm.Blues, alpha=1.0)


## turn off all ticks at bottom 
ax.tick_params(axis='x', which='both', bottom=False)


## set minor ticks
ax.set_xticks(np.arange(0,comfmat.shape[0]), minor = False)
ax.set_yticks(np.arange(0,comfmat.shape[1]), minor= False)

#set spaces in between the labels
print(ax.get_xticks())

#limit the text to the size of the figure
plt.xlim(-0.5, comfmat.shape[0])
plt.ylim(comfmat.shape[1], -0.5)

#set x and y labels
ax.set_xticklabels([labels[str(k+1)] for k in np.arange(comfmat.shape[0])], size=5)
ax.set_yticklabels([labels[str(k+1)] for k in np.arange(comfmat.shape[1])], size=5)

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(which="both"), rotation=45, ha="left",
     rotation_mode="anchor")


## populate matshow values with comfmat values
for i in range(comfmat.shape[0]):
	for j in range(comfmat.shape[1]):
		ax.text(x=j, y=i, s=int(comfmat[i,j]*100), va='center', ha='center', size="7")
		# ax.text(x=j, y=i, s=int(comfmat[i,j]*100), va='center', ha='center')


mplcursors.cursor(hover=False).connect("add", lambda sel: sel.annotation.set_text(labels[str(sel.target.index[0] + 1)] +","+ labels[str(sel.target.index[1] + 1)]))
# mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(df[(df['x']==[sel.target.index[0]])]['name']))

mplcursors.cursor

plt.xlabel("Predicted Category")
plt.ylabel("Old Category")
ax.yaxis.set_label_position("right")
plt.show()




