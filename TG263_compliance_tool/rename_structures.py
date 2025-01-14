import csv

# path_to_conversion = './names_to_convert.csv'
# path_original_files = '/mnt/iDriveShare/Kayla/EclipseStructureTemplates/'
# path_original_files_dcm = '/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/618_old/20230529_CT_25_MAY_2023/'
save_path = './'
save_path_dcm = './NEW_dicoms/'

from parse_xml import rename_xml_template
from parse_dcm import rename_dicom_rt
from config import config


# rs_files, new_names = load_xml_data(path)

# temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action, ids, namex, vol_type, code =parse_structure_xml(path+rs_files[i])


# print(name_dict['Brachial_Plex_R'])
'''
def get_name_dict(path_to_conversion='./names_to_convert.csv'):
	with open(path_to_conversion) as csv_file:
		reader = csv.reader(csv_file)
		name_dict = dict(reader)
		# print(name_dict)
	return name_dict
'''

def get_name_dict(path_to_conversion='./NAMES_TO_CONVERT.csv'):
	name_dict = {}
	with open(path_to_conversion) as csv_file:
		reader = csv.DictReader(csv_file)
		# name_dict = dict(reader)
		for row in reader:
			name_dict[row['In-House Name']] = row['Proposed TG263 name']
		# print(name_dict)
	return name_dict

def main():
	
	name_dict = get_name_dict()

	file_type = config['file_type']
	PATH = config['PATH']
	
	if file_type == 'dcm':
		rename_dicom_rt(name_dict, PATH, save_path)
	elif file_type == 'xml':
		rename_xml_template(name_dict,PATH,save_path)
	else:
		raise Exception("Please specify one of the following file types in config.py: xml or dcm.")




if __name__ == '__main__':
	main()
