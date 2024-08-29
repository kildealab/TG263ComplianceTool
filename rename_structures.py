import csv

path_to_conversion = './names_to_convert.csv'
path_original_files = '/mnt/iDriveShare/Kayla/EclipseStructureTemplates/'
save_path = './'

from parse_xml_template import rename_xml_template

# rs_files, new_names = load_xml_data(path)

# temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action, ids, namex, vol_type, code =parse_structure_xml(path+rs_files[i])

with open(path_to_conversion) as csv_file:
	reader = csv.reader(csv_file)
	name_dict = dict(reader)
	print(name_dict)

print(name_dict['Brachial_Plex_R'])
rename_xml_template(name_dict,path_original_files,save_path)



