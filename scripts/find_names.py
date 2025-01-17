# import glob
import os
import time
# import json
# import pydicom as dcm
import pandas as pd 
import csv
# import re

# from parse_DICOM_RS import load_RS_names, find_RS_files_recursive
# from compliance_check import check_TG_name, check_target_compliance, get_proposed_name,get_additional_names,load_additional_names
# from parse_xml_template import load_xml_data, parse_structure_xml

import TG263ComplianceTool.loaders as loaders
import TG263ComplianceTool.structure_compliance as structure_compliance
import TG263ComplianceTool.target_compliance as target_compliance
import TG263ComplianceTool.parse_xml as parse_xml
from config import config



# # data_to_write = [[x] for x in names_to_convert]
# with open("names_to_convert.csv","w") as f:
# 	writer = csv.writer(f)
# 	writer.writerow(["non-compliant name","TG-263 suggestion"])
# 	writer.writerows(zip(names_to_convert,proposed_names))



# df = pd.DataFrame({"Non-compliant Nomenclature":names_to_convert})
# df.to_csv(index=False)

def main():

	start_time = time.time()

	# to do, add command line option

	path = config['PATH']
	file_type = config['file_type']
	
	fd = os.path.abspath(os.path.dirname(__file__)) # current file directory, for constructing relative paths later

	

	# Load the official TG 263 CSV containing list of allowed names
	# tg_names, tg_names_rev = loaders.load_tg_263(tg_path=os.path.join(fd,"../data/"))



	

	# Get the list of DICOM RS files and the structure names in them
	if file_type == 'dcm':
		rs_files, new_names = loaders.load_RS_data(path,avoid_root_keywords=['kV_CBCT'])
	elif file_type == 'xml':
		rs_files, new_names = loaders.load_xml_data(path)
	else:
		raise Exception("Please specify one of the following file types in config.py: xml or dcm.")



	'''
	rt_names = load_csv()
	# print(rt_names)

	for list_name in new_names:
		for name in list_name:

			# if name.lower() not in rt_names:
			# 	rt_names.append(name.lower())
			if name not in rt_names:
				rt_names.append(name)
			else:
				print(name)

	print(rt_names)
	'''
	
	col_file, col_name, col_length, col_match, col_propname, col_reason, col_type = [], [], [], [], [], [], []
	uniq_name, uniq_length, uniq_match, uniq_propname, uniq_reason, uniq_type, instances = [], [], [], [], [], [], []


	# TO DO # fix this -- right now just makine rs_files the template files

	
	
	

	# @todo: why is this here

	# check_file = True
	# write_files = False
	# print(rs_files, new_names)
	print("done calling load rs data")


	# TO DO: complete disaster why are there so many params lol
	if file_type == 'xml':
		xml_ids, xml_types, temp_apps, temp_sites, last_names,last_dates,last_actions,created_names,created_dates,created_actions, names, vol_types, codes = [],[],[],[],[],[],[],[],[],[],[],[],[]
	

	names_to_convert, to_convert_instances, to_convert_reasons, names_to_convert_proposal = [],[],[],[]

	for i in range(len(rs_files)):
		# print("i",i)
		#TODO: messy calling multiple times
		if file_type == 'xml':
			temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action, ids, namex, vol_type, code = parse_xml.parse_structure_xml(path+rs_files[i])

		for j in range(len(new_names[i])):
			# print("j",j)
			
			col_file.append(rs_files[i].replace(path,""))
			if file_type == 'xml':
				xml_ids.append(temp_id)
				xml_types.append(temp_type)
				temp_apps.append(temp_app)
				temp_sites.append(temp_site)
				# last_approvals.append(last_approval) 
				last_names.append(last_name)
				last_dates.append(last_date)
				last_actions.append(last_action)
				created_names.append(created_name)
				created_dates.append(created_date)
				created_actions.append(created_action)
				names.append(namex[j]) 
				vol_types.append(vol_type[j])
				codes.append(code[j])

			name = new_names[i][j]

			# print(name)

			if name in col_name:
				index = col_name.index(name)
				col_name.append(name)
				col_length.append(len(name))
				col_match.append(col_match[index])
				col_propname.append(col_propname[index])
				col_reason.append(col_reason[index])
				col_type.append(col_type[index])
				# col_rules.append(col_rules[index])

				uniq_index = uniq_name.index(name)
				instances[uniq_index] += 1

				# print("namealready in")
				if name in names_to_convert:
					uniq_index = names_to_convert.index(name)
					to_convert_instances[uniq_index] += 1

			else:
				col_name.append(name)
				

				uniq_name.append(name)
				uniq_length.append(len(name))
				instances.append(1)

				col_length.append(len(name))

				# Check if the structure is a target or non-target, as they have different rules
				if "gtv" in name.lower() or "ctv" in name.lower() or "ptv" in name.lower() or "itv" in name.lower():
					struct_type = "target"
					
				else:
					struct_type = "non-target"
				col_type.append(struct_type)


				if structure_compliance.check_in_TG(name): # Check if name in TG list 
					match = True
					col_match.append("True")
					col_propname.append("")
					col_reason.append("")
					# col_rules.append("")
					proposed_name =""
					reason = ""
					# rules = []

				else:
					if struct_type == "non-target":
						match, reason = structure_compliance.check_TG_name(name)#, tg_names)
						if not match:
							proposed_name, reason = structure_compliance.get_proposed_name(name)#,tg_names)

						# match = False
					else:
						match, reason = target_compliance.check_target_compliance(name)#, tg_names) # Check target name compliance
						
					
					col_match.append(match)
					# if reason == '':
					# 	if 'avoid' in name.lower():
					# 		reason = "avoid"
					# 	elif "z_" in name.lower():
					# 		reason = "z"
					# 	elif "nos" in name.lower():
					# 		reason = "nos"
					# 	# elif "TV" in name:
					# 	# 	reason = "PTV/CTV/GTV"

					col_propname.append(proposed_name)
					col_reason.append(reason) 

					# print(name,match,name in names_to_convert)

					if not match and name not in names_to_convert:
						# print(name)
						# print(names_to_convert)
						names_to_convert.append(name)
						names_to_convert_proposal.append(proposed_name)
						to_convert_reasons.append(reason)
						to_convert_instances.append(1)
					# else:
						# print("NOT MATCH",name)
					# elif name in names_to_convert:
						# print("*************************")
						# print(name)

						# uniq_index = names_to_convert.index(name)
						# to_convert_instances[uniq_index] += 1
						# print(uniq)

				
				uniq_match.append(match)
				uniq_propname.append(proposed_name)
				uniq_reason.append(reason)
				uniq_type.append(struct_type)
				# uniq_rules.append(rules)



	# overwrite = True
	# if not os.path.isfile("full_list_structs.csv") or overwrite == True:

	# 	with open("full_list_structs.csv","w") as f:
	# 		writer = csv.writer(f)
	# 		writer.writerow(["File","In-House Name","Matches TG-263","TG-263 suggestion","Reason"])
	# else:
	# 	with open("full_list_structs.csv","a") as f:
	# 		writer = csv.writer(f)
	# 		writer.writerows(zip(col_file, col_name,col_match,col_propname,col_reason))


	detailed_output = False

	if file_type=='dcm':
		write_csv(os.path.join(fd,"../output/individual_list_structs_dcm.csv"),zip(col_file, col_name,col_length,col_match,col_propname,col_reason,col_type),headers=["File","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type"])
	elif file_type=='xml':
		write_csv(os.path.join(fd,"../output/individual_list_structs_xml.csv"),zip(col_file,xml_ids,xml_types,temp_apps,temp_sites,last_names,last_dates,last_actions,created_names,created_dates,created_actions,names,vol_types,codes, col_name,col_length,col_match,col_propname,col_reason,col_type),
			headers=["File","ID","type","ApprovalStatus","Site","last_name","last_date","last_action","created_name","created_date","created_action","name","volumeType","code","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type"])

	write_csv("NAMES_TO_CONVERT.csv",zip(names_to_convert,to_convert_instances,to_convert_reasons,names_to_convert_proposal),headers=["In-House Name","Instances","Reason for non-compliance","Proposed TG263 name"])
	write_csv(os.path.join(fd,"../output/unique_list_structs.csv"),zip(uniq_name, instances, uniq_length,uniq_match,uniq_propname,uniq_reason,uniq_type), headers = ["In-House Name","Instances","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type"])	
	# write_csv("names_to_convert.csv",content=zip(names_to_convert,names_to_convert_proposal),headers=["In-House Name","Proposed Name"])
	write_csv(os.path.join(fd,"../data/additional_allowed_names.csv"),zip(sorted(structure_compliance.get_additional_names())),overwrite=True)
	# with open("additional_allowed_names.csv", "w") as f:
	# 	writer = csv.writer(f)

	# 	writer.writerows(zip(sorted(compliance_check.get_additional_names())))

	print("Compliance rate:", uniq_match.count(True),"/",len(uniq_match), "-->", round(100*uniq_match.count(True)/len(uniq_match),2),"%")
	print("*********", time.time() - start_time,  "seconds *********")
	print("IMPORTANT: Please review proposed names in NAMES_TO_CONVERT.CSV and fill in the blanks before running rename-structures.")

def write_csv(file_name,content,headers=[],overwrite=True):
	if overwrite: 
		key = 'w'
	else:
		key = 'a'

	with open(file_name,key) as f:
		writer = csv.writer(f)
		if len(headers) > 0:
			writer.writerow(headers)
		writer.writerows(content)


if __name__ == '__main__':
	main()