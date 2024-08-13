import glob
import os
import time
import json
import pydicom as dcm

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

def load_json(json_path="."):
	json_file = os.path.join(json_path,"name_conversions.json")
	if os.path.isfile(json_file):
		with open(json_file) as f:
			json_data = json.load(f)
			return json_data
	else:
		return {}

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



# def initialize_csv(csv_path="."):
# 	if not os.path.isfile(os.path.join(json_path,"name_conversions.csv")):


rs_files = find_RS_files_recursive('/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/')
print(rs_files)

json_data = load_json()
print(json_data)

names = load_RS_names(rs_files)
print(names)

print(len(rs_files))
print(len(names))


print("*********", time.time() - start_time,  "*********")

