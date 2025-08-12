import os
import csv
import pandas as pd
import csv

import TG263ComplianceTool.parse_dcm as parse_dcm
import TG263ComplianceTool.parse_xml as parse_xml


def load_csv(csv_path="."):
	'''
	load_csv	Load	

	:param csv_path:
	:return:
	'''
	csv_file = os.path.join(csv_path,"name_conversions.csv")
	if os.path.isfile(csv_file):
		df = pd.read_csv(csv_file)
		cols = list(df)

		return df[cols[0]].to_list()
	else:
		return []



def load_tg_263(tg_path="../data/",tg_name="TG263_Nomenclature_Worksheet_20170815(TG263 v20170815).csv"):
	'''
	load_tg_263	Reads the TG263 csv file obtained from https://www.aapm.org/pubs/reports/RPT_263_Supplemental/
				Note: Should keep this updated if ever there are changes, or link directly to the live spreadsheet.	

	:param tg_path: Path to where the TG 263 spreadhseet is located.
	:param tg_name: Name of the TG 263 csv. 
	:return: the list of allowed names, and the list of allowed names in the reversed nomenclature.
	'''

	df = pd.read_csv(os.path.join(tg_path,tg_name))
	tg_names = df['TG263-Primary Name'].to_list()
	tg_names_rev = df['TG-263-Reverse Order Name'].to_list()
	return tg_names, tg_names_rev

def load_additional_names(file_name="additional_allowed_names.csv"):
	if os.path.isfile(file_name):
		with open(file_name, 'r') as fil:
			additional_allowed_names = [line.rstrip('\n') for line in fil]
	else:
		additional_allowed_names = [] 
	return additional_allowed_names

def find_RS_files_recursive(PATH,avoid_root_keywords=[]):
	# rs_files = glob.glob()
	# list_all_files = []
	rs_files = []

	for root, dirs, files in os.walk(PATH):
		# list_all_files.append()
		# print(root,len(files))
		# print(os.path.join(root, file))

		for file in [f for f in files if f[0:2]=='RS']:
			# file_path = os.path.join(root, file)
			# print(root)
			if not any(keyword in root for keyword in avoid_root_keywords):
			# if "_CBCT_" not in root and 'old' not in root:
				# print(root)
				rs_files.append(os.path.join(root, file))

		#     print(os.path.join(root, file))

	# rs_files = glob.glob(os.path.join(PATH, '**', 'RS*'), recursive=True)
	# for file in rs_files:
	# 	print(file)
	return rs_files


def load_RS_data(path,check_file = False, write_files = False,avoid_root_keywords=[]):
	'''
	load_RS_data	Recursively searches for all DICOM Structure Set Files (assumes file name starts with 'RS') 
					within a given path.

	:param path: Path to search recursively for RS riles.
	:param check_file: @todo
	:param write_files: @todo
	:param avoid_root_keywords: List of keywords found in directory names to ignore during search.

	:return: a list of RS file paths, and a list of the structure names in these files

	'''

	if check_file and os.path.isfile('names_to_convert.csv'):
		with open('names_to_convert.csv','r') as f:
			rs_files = [row[0] for row in csv.reader(f)]
	else:
		rs_files = find_RS_files_recursive(path,avoid_root_keywords)#,avoid_root_keywords=["_CBCT_","PlanAdapt","QA","old","TEST"])
		data_to_write = [[x] for x in rs_files]
		if write_files:
			with open("names_to_convert.csv","w") as f:
				writer = csv.writer(f)
				writer.writerows(data_to_write)

	# print(rs_files)
	rs_files.sort()
	# json_data = load_json()
	# print(json_data)

	new_names = parse_dcm.load_RS_names(rs_files)
	# print(new_names)

	return rs_files, new_names


def load_xml_data(PATH):
	xml_files = []
	names = []

	for root, dirs, files in os.walk(PATH):
		# list_all_files.append()
		# print(root,len(files))
		# print(os.path.join(root, file))

		for file in [f for f in files if f.lower().endswith(".xml")]: # to do can also check the type inside the xml file
			xml_files.append(file)

	for file in xml_files:
		_, _,_,_,_,_, _,_,_,_,name,_,_,_ = parse_xml.parse_structure_xml(PATH+file)
		names.append(name)

	return xml_files, names