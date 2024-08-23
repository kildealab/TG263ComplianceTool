import pydicom as dcm
import os

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
				print(root)
				rs_files.append(os.path.join(root, file))

		#     print(os.path.join(root, file))

	# rs_files = glob.glob(os.path.join(PATH, '**', 'RS*'), recursive=True)
	# for file in rs_files:
	# 	print(file)
	return rs_files




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

