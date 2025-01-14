import pydicom as dcm
import os

import loaders

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

def rename_dicom_rt(name_dict,PATH, save_path):
	#TO DO: go thru dicom names
	#to do -- make efficient, save list?
	files = loaders.find_RS_files_recursive(PATH,avoid_root_keywords=['kV_CBCT'])
	print(files)
	for file in files:
		RS = dcm.read_file(file)
		for i,seq in enumerate(RS.StructureSetROISequence):
			roi_name = seq.ROIName
			if roi_name in name_dict:
				print(roi_name, name_dict[roi_name])
				print(seq)
				if name_dict[roi_name] == '':
					print("WARNING: NO REPLACEMENT FOR NAME", roi_name)
				else:
					RS.StructureSetROISequence[i].ROIName = name_dict[roi_name]
					print(seq)
					

		# TO DO: created path if not exists

		RS.save_as(save_path+file.split("/")[-1])        

