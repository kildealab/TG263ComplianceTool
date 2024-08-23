import xml.etree.ElementTree as ET

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
		last_approval = it.get("ApprovalHistory").split(";")[-1]

	return temp_id, temp_type, temp_app, temp_site, last_approval


def get_structure_elements(root):
	ids = []
	names = []
	vol_type = []
	codes = []


	for structure in root.findall('.//Structure'):
		structure_id = structure.get("ID")
		name = structure.get('Name')
		volume_type = structure.find('Identification/VolumeType').text
		struct_code = structure.find('Identification/StructureCode').get("Code")
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
	temp_id, temp_type, temp_app, temp_site, last_approval = get_preview_elements(root)
	ids, names, vol_type, codes = get_structure_elements(root)
	return temp_id, temp_type, temp_app, temp_site, last_approval, ids, names, vol_type, codes


path = '/mnt/iDriveShare/Kayla/StructureTemplates/StructureTemplate_27718.xml'