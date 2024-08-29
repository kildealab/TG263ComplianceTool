import xml.etree.ElementTree as ET
import os

def extract_root(path):
	tree = ET.parse(path)
	root = tree.getroot()
	return root

def get_preview_elements(root):
	for it in root.iter('Preview'): # TO DO can customize to get whatever ids with config file -- or just do get fns for each 
		# do one to get preview then to gets for elems?
		temp_id = it.get("ID")
		temp_type = it.get('Type')
		temp_app = it.get("ApprovalStatus")
		temp_site = it.get("TreatmentSite")
		approval_history = it.get("ApprovalHistory").split(";")
		last_approval = approval_history[-1]
		created = approval_history[0]
		print(last_approval)
		last_name = last_approval.split(' ')[0]
		last_date = last_approval.split('[ ')[-1].strip(' ]')
		last_action =last_approval.split(' ')[1]

		created_name = created.split(' ')[0]
		created_date = created.split('[ ')[-1].strip(' ]')
		created_action =created.split(' ')[1]


		# if last_approval == created:
			# last_approval = ''



	return temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action


def get_structure_elements(root):
	ids = []
	names = []
	vol_type = []
	codes = []


	for structure in root.findall('.//Structure'):
		structure_id = structure.get("ID")
		name = structure.get('Name')
		volume_type = structure.find('Identification/VolumeType').text
		try:
			struct_code = structure.find('Identification/StructureCode').get("Code")
		except:
			struct_code = ''
	#     print(structure.find('Identification/StructureCode').get("CodeScheme"))
	#     colour_style = structure.find('ColorAndStyle').text

		ids.append(structure_id)
		names.append(name)
		vol_type.append(volume_type)
		codes.append(struct_code)

	 
	# print(len(ids))
	# print(len(names))
	# print(len(vol_type))
	# print(len(codes))

	if not all(len(ids) == len(l) for l in [names, vol_type,codes]):
		raise ValueError('not all lists have same length!')

	return ids, names, vol_type, codes


def parse_structure_xml(path):
	root = extract_root(path)
	temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action = get_preview_elements(root)
	ids, names, vol_type, codes = get_structure_elements(root)
	# print(len(o))
	return temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action, ids, names, vol_type, codes



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
		_, _,_,_,_,_, _,_,_,_,name,_,_,_ = parse_structure_xml(PATH+file)
		names.append(name)

	return xml_files, names


# path = '/mnt/iDriveShare/Kayla/StructureTemplates/StructureTemplate_27718.xml'