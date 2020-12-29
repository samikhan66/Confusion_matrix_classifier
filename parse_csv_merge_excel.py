# DEVELOPED BY SAMI KHAN 12/29/2020
# This provides a script to help parse various csv files and merge into an excel file
# This later can be used for a confusion matrix to help measure your model performance.
# This a testing tool and helps you visualize your model results while helping you manipulate while drawing statistical inference using Excel

import os
import csv
import pandas as pd
from collections import defaultdict, Counter
import sys
import glob, os
from pandas import DataFrame, ExcelWriter


#define your labels. This is used to generate the labels that you will see in on your x and y axes of your confusion matrix.
labels = {
	'label_1': 1,
	'label_2': 2,
	}

def attributes():
	"""This function is used to spit out attributes such as filename, true_group, predicted_group, confidence, correct_category, correct_group """
	with open("train_inference.csv", 'r') as csvfile:
		for row in csvfile:
			r = row.split("/")
			if len(r) > 1:
				filetypes = [".pdf", ".tif", ".jpg"]
				for filetype in filetypes:
					if filetype in r[9].lower():
						true_category = r[8]
						true_group = r[8].split("-")[0] 
						filename = r[9].lower().split(filetype)[0] + str(filetype)
						category_numbers = r[9].lower().split(filetype)[1]
						predicted_category_number = category_numbers.split(" ")[0].strip(",")
						confidence = category_numbers.split(" ")[1]
						reverse_dic = {v: k for k, v in labels.items()}
						predicted_category = reverse_dic[int(predicted_category_number)]
						predicted_group = predicted_category.split("-")[0]
						correct_category = ""
						if predicted_category == true_category:
							correct_category = 1
						else:
							correct_category = 0
						if predicted_group == true_group:
							correct_group = 1
						else:
							correct_group = 0

						yield filename, true_category, predicted_category, true_group, predicted_group, confidence, correct_category, correct_group


def write_sheet_one():
	"""Writes the attributes to a csv """
	with open("sheet_one.csv", "w") as file:
		writer = csv.DictWriter(file, fieldnames = ["filename", 
			"true_category", "predicted_category", "true_group", 
			"predicted_group", "confidence", "correct_category", "correct_group"])
		writer.writeheader()
		for elements in attributes():
			filename, true_category, predicted_category, true_group, predicted_group, confidence, correct_category, correct_group = elements
			writer.writerow({"filename": filename, 
				"true_category": true_category, "predicted_category": predicted_category, "true_group": true_group, 
				"predicted_group": predicted_group, "confidence": confidence, "correct_category": correct_category, "correct_group": correct_group})


def sheet_two_attributes():
	"""used to find the correct categories """
	true_categories = {}
	correct_categories = {}
	with open("sheet_one.csv", "r") as f:
		reader = csv.reader(f, delimiter = ',')

		for row in reader:
			true_cat = row[1] 
			pred_cat = row[2]
			if true_cat not in true_categories:
				true_categories[true_cat] = 0
			true_categories[true_cat] += 1

			if true_cat not in correct_categories:
				correct_categories[true_cat] = 0
			correct_categories[true_cat] += (true_cat == pred_cat)

	vtrues = []
	for ktrue, vtrue in true_categories.items():
		vtrues.append(vtrue)
	
	vpreds = []
	for kpred, vpred in correct_categories.items():
		vpreds.append(vpred)

	category_accuracies = [round((i / j)*100, 1) for i, j in zip(vpreds, vtrues)]
	

	return true_categories, correct_categories, category_accuracies


def write_sheet_two():
	true_categories, correct_categories, category_accuracies = sheet_two_attributes()

	with open("sheet_two.csv", "w") as file:
			writer = csv.DictWriter(file, fieldnames = ["category", 
				"number_of_files", "number_of_correct_predictions", "accuracy"])
			writer.writeheader()
			ktrue = []
			vtrue = []
			for ktrues, vtrues in true_categories.items():
				ktrue.append(ktrues)
				vtrue.append(vtrues)

			vcorrect = []	
			for _, vcorrects in correct_categories.items():	
				vcorrect.append(vcorrects)
			# print(vcorrect)
			# exit()	
			
			for category, number_of_files, number_of_correct_predictions, accuracy in zip(ktrue, vtrue, vcorrect, category_accuracies):
				writer.writerow({"category": category, 
				"number_of_files": number_of_files,	
			    "number_of_correct_predictions": number_of_correct_predictions,
			    "accuracy": accuracy})	
					

def sheet_three_attributes():
	""" Used to find the accuracies of the group """
	true_groups = {}
	correct_groups = {}
	with open("sheet_one.csv", "r") as f:
		reader = csv.reader(f, delimiter = ',')

		for row in reader:
			true_grp = row[3] 
			pred_grp = row[4]
			if true_grp not in true_groups:
				true_groups[true_grp] = 0
			true_groups[true_grp] += 1

			if true_grp not in correct_groups:
				correct_groups[true_grp] = 0
			correct_groups[true_grp] += (true_grp == pred_grp)

	vtrues = []
	for ktrue, vtrue in true_groups.items():
		vtrues.append(vtrue)
	
	vpreds = []
	for kpred, vpred in correct_groups.items():
		vpreds.append(vpred)

	group_accuracies = [round((i / j)*100, 1) for i, j in zip(vpreds, vtrues)]
	
	return true_groups, correct_groups, group_accuracies

def write_sheet_three():
	true_groups, correct_groups, group_accuracies = sheet_three_attributes()

	with open("sheet_three.csv", "w") as file:
			writer = csv.DictWriter(file, fieldnames = ["group", 
				"number_of_files", "number_of_correct_predictions", "accuracy"])
			writer.writeheader()
			ktrue = []
			vtrue = []
			for ktrues, vtrues in true_groups.items():
				ktrue.append(ktrues)
				vtrue.append(vtrues)

			vcorrect = []	
			for _, vcorrects in correct_groups.items():	
				vcorrect.append(vcorrects)
			# print(vcorrect)
			# exit()	
			
			for group, number_of_files, number_of_correct_predictions, accuracy in zip(ktrue, vtrue, vcorrect, group_accuracies):
				writer.writerow({"group": group, 
				"number_of_files": number_of_files,	
			    "number_of_correct_predictions": number_of_correct_predictions,
			    "accuracy": accuracy})	

write_sheet_one()
write_sheet_two()
write_sheet_three()



root = os.getcwd()

writer = ExcelWriter("compiled.xlsx")
for fname in os.listdir(root):
	if os.path.splitext(fname)[1] == ".csv":
	    df_csv = pd.read_csv(fname)

	    (_, f_name) = os.path.split(fname)
	    (f_shortname, _) = os.path.splitext(f_name)

	    df_csv.to_excel(writer, f_shortname, index=False)

	writer.save()


# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# #export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
