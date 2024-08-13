import glob
import os
import time
import json
import pydicom as dcm
import pandas as pd 

start_time = time.time()



def find_RS_files_recursive(PATH):
	# rs_files = glob.glob()
	# list_all_files = []
	rs_files = []

	for root, dirs, files in os.walk(PATH):
		# list_all_files.append()
		# print(root,len(files))
		# print(os.path.join(root, file))

		for file in [f for f in files if f[0:2]=='RS']:
			rs_files.append(os.path.join(root, file))
		#     print(os.path.join(root, file))

	# rs_files = glob.glob(os.path.join(PATH, '**', 'RS*'), recursive=True)
	# for file in rs_files:
	# 	print(file)
	return rs_files

# def initialize_json(json_path="."):

# 	if not os.path.isfile(os.path.join(json_path,"name_conversions.json")):

# def load_json(json_path="."):
# 	json_file = os.path.join(json_path,"name_conversions.json")
# 	if os.path.isfile(json_file):
# 		with open(json_file) as f:
# 			json_data = json.load(f)
# 			return json_data
# 	else:
# 		return {}



def find_ROI_names(RS, keyword='', avoid=[]):
    '''
    find_ROI_names  finds all contour names in RT Structure Set File containing keyword, 
                    while ignoring those containing 'nos' and 'z_'.
    
    :param RS: the RS file opened by pydicom
    :param keyword: The keyword to search the ROIs for. If blank returns all ROIs.
    
    :returns: list of ROI names containing keyword.
    '''
    ROI_names = []

    for seq in RS.StructureSetROISequence:
        roi_name = seq.ROIName
        # TO DO -- custom avoid
        # if keyword.lower() in roi_name.lower() and 'nos' not in roi_name.lower() and 'z_' not in roi_name.lower():
        if keyword.lower() in roi_name.lower():
            ROI_names.append(seq.ROIName)
    return ROI_names

def load_RS_names(rs_files):
	list_names = []
	for file in rs_files:
		RS = dcm.read_file(file)
		list_names.append(find_ROI_names(RS))
	return list_names



def load_csv(csv_path="."):
	csv_file = os.path.join(csv_path,"name_conversions.csv")
	if os.path.isfile(csv_file):
		df = pd.read_csv(csv_file)
		cols = list(df)

		return df[cols[0]].to_list()
	else:
		return []

def load_tg_263(tg_path=".",tg_name="TG263_Nomenclature_Worksheet_20170815(TG263 v20170815).csv"):
	df = pd.read_csv(os.path.join(tg_path,tg_name))
	tg_names = df['TG263-Primary Name'].to_list()
	tg_names_rev = df['TG-263-Reverse Order Name'].to_list()
	return tg_names, tg_names_rev

rs_files = find_RS_files_recursive('/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/')
print(rs_files)

# json_data = load_json()
# print(json_data)

new_names = load_RS_names(rs_files)
print(new_names)

print(len(rs_files))
print(len(new_names))

rt_names = load_csv()
print(rt_names)

for list_name in new_names:
	for name in list_name:

		# if name.lower() not in rt_names:
		# 	rt_names.append(name.lower())
		if name not in rt_names:
			rt_names.append(name)
		else:
			print(name)

# print(rt_names)

tg_names, tg_names_rev = load_tg_263()
print(len(tg_names))
print(len(tg_names_rev))

for name in rt_names:
	if name in tg_names:
		print("YES:",name)
	else:
		print("NO:",name)


print("*********", time.time() - start_time,  "*********")

