# import glob
import os
import time
# import json
# import pydicom as dcm
import pandas as pd 
import csv
# import re

from parse_DICOM_RS import load_RS_names, find_RS_files_recursive
from compliance_check import check_TG_name, check_target_compliance, get_proposed_name,get_additional_names,load_additional_names
from parse_xml_template import load_xml_data, parse_structure_xml


def load_csv(csv_path="."):
	'''
	load_csv	

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

	new_names = load_RS_names(rs_files)
	# print(new_names)

	return rs_files, new_names







# # data_to_write = [[x] for x in names_to_convert]
# with open("names_to_convert.csv","w") as f:
# 	writer = csv.writer(f)
# 	writer.writerow(["non-compliant name","TG-263 suggestion"])
# 	writer.writerows(zip(names_to_convert,proposed_names))



# df = pd.DataFrame({"Non-compliant Nomenclature":names_to_convert})
# df.to_csv(index=False)

def main():

	start_time = time.time()

	# Load the official TG 263 CSV containing list of allowed names
	tg_names, tg_names_rev = load_tg_263()
	print(len(tg_names))
	print(len(tg_names_rev))


	# Loads the CSV with additional nomenclatures that are TG 263 compliant, but not explicitly in the original CSV
	# Names were automatically added after passing through the compliance check in this code. 
	# This CSV is unecessary, but saves time for repeated words that have already been checked.
	load_additional_names() 




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
	

	col_file = []
	col_name = []
	col_length = []
	col_match = []
	col_propname = []
	col_reason = []
	col_type = []
	col_rules = []

	uniq_name = []
	uniq_length = []
	uniq_match = []
	uniq_propname = []
	uniq_reason = []
	uniq_type = []
	uniq_rules = []
	instances=[]
	# TO DO # fix this -- right now just makine rs_files the template files

	
	# to do, automatic or command line param
	file_type = 'dcm'
	
	# TODO: put path in config file
	path = '/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/'
	# path = '/mnt/iDriveShare/Kayla/CBCT_images/Kayla_extracted/'

	# Get the list of DICOM RS files and the structure names in them
	rs_files, new_names = load_RS_data(path)

	# path = '/mnt/iDriveShare/Kayla/StructureTemplates/'
	# rs_files, new_names = load_xml_data(path)

	# path = '/mnt/iDriveShare/Kayla/EclipseStructureTemplates/'
	# path = './'
	# rs_files, new_names = load_xml_data(path)
	print(rs_files)

	# @todo: why is this here

	check_file = True
	write_files = False
	# print(rs_files, new_names)
	print("done calling load rs data")


	# TO DO: complete disaster why are there so many params lol
	xml_ids, xml_types, temp_apps, temp_sites, last_names,last_dates,last_actions,created_names,created_dates,created_actions, names, vol_types, codes = [],[],[],[],[],[],[],[],[],[],[],[],[]
	names_to_convert = []
	names_to_convert_proposal = []

	for i in range(len(rs_files)):
		# print(i)
		#TODO: messy calling multiple times
		if file_type == 'xml':
			temp_id, temp_type, temp_app, temp_site, last_name,last_date,last_action,created_name,created_date,created_action, ids, namex, vol_type, code =parse_structure_xml(path+rs_files[i])

		for j in range(len(new_names[i])):
			# print(j)
			
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
				col_rules.append(col_rules[index])

				uniq_index = uniq_name.index(name)
				instances[uniq_index] += 1

				# print("namealready in")

			else:
				col_name.append(name)
				

				uniq_name.append(name)
				uniq_length.append(len(name))
				instances.append(1)

				col_length.append(len(name))

				if "gtv" in name.lower() or "ctv" in name.lower() or "ptv" in name.lower() or "itv" in name.lower():
					struct_type = "target"
					
				else:
					struct_type = "non-target"
				col_type.append(struct_type)


				if name in tg_names: # Check if name in TG list 
					match = True
					col_match.append("True")
					col_propname.append("")
					col_reason.append("")
					col_rules.append("")
					proposed_name =""
					reason = ""
					rules = []

				else:
					if struct_type == "non-target":
						match, reason = check_TG_name(name, tg_names)
						if not match:
							proposed_name, reason = get_proposed_name(name,tg_names)

						# match = False
					else:
						match, reason = check_target_compliance(name, tg_names) # Check target name compliance
						
					
					col_match.append(match)
					if reason == '':
						if 'avoid' in name.lower():
							reason = "avoid"
						elif "z_" in name.lower():
							reason = "z"
						elif "nos" in name.lower():
							reason = "nos"
						# elif "TV" in name:
						# 	reason = "PTV/CTV/GTV"

					col_propname.append(proposed_name)
					col_reason.append(reason) 

					rules = []
					if struct_type == "target":
						rules.append("TBD")
					else:
						if len(name) > 16: 
							rules.append(1)
						#to do: rules 2, 3, etc.
						if reason=="casing":
							rules.append(4)
						if " " in name:
							rules.append(5)
					col_rules.append(rules)

					if not match and name not in names_to_convert:
						names_to_convert.append(name)
						names_to_convert_proposal.append(proposed_name)

				
				uniq_match.append(match)
				uniq_propname.append(proposed_name)
				uniq_reason.append(reason)
				uniq_type.append(struct_type)
				uniq_rules.append(rules)



	# overwrite = True
	# if not os.path.isfile("full_list_structs.csv") or overwrite == True:

	# 	with open("full_list_structs.csv","w") as f:
	# 		writer = csv.writer(f)
	# 		writer.writerow(["File","In-House Name","Matches TG-263","TG-263 suggestion","Reason"])
	# else:
	# 	with open("full_list_structs.csv","a") as f:
	# 		writer = csv.writer(f)
	# 		writer.writerows(zip(col_file, col_name,col_match,col_propname,col_reason))


	# TO DO make it a fn for headers and vars , for now hard coding

	with open("full_list_structs.csv","w") as f:
		writer = csv.writer(f)
		writer.writerow(["File","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
		writer.writerows(zip(col_file, col_name,col_length,col_match,col_propname,col_reason,col_type,col_rules))

	with open("unique_list_structs.csv","w") as f:
		writer = csv.writer(f)
		writer.writerow(["In-House Name","Instances","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
		writer.writerows(zip(uniq_name, instances, uniq_length,uniq_match,uniq_propname,uniq_reason,uniq_type,uniq_rules))
	'''
	with open("full_list_structs_xml.csv","w") as f:
		writer = csv.writer(f)
		writer.writerow(["File","ID","type","ApprovalStatus","Site","last_name","last_date","last_action","created_name","created_date","created_action","name","volumeType","code","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
		writer.writerows(zip(col_file,xml_ids,xml_types,temp_apps,temp_sites,last_names,last_dates,last_actions,created_names,created_dates,created_actions,names,vol_types,codes, col_name,col_length,col_match,col_propname,col_reason,col_type,col_rules))

	with open("unique_list_structs_xml.csv","w")  as f:
		writer = csv.writer(f)
		writer.writerow(["In-House Name","Instances","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
		writer.writerows(zip(uniq_name, instances, uniq_length,uniq_match,uniq_propname,uniq_reason,uniq_type,uniq_rules))
	'''
	with open("names_to_convert.csv","w") as f:
		writer = csv.writer(f)
		writer.writerow(["In-House Name","Proposed Name"])
		writer.writerows(zip(names_to_convert,names_to_convert_proposal))

	# to do , dont overwrite if exists
	with open("additional_allowed_names.csv", "w") as f:
		writer = csv.writer(f)

		writer.writerows(zip(sorted(get_additional_names())))

	print("Compliance rate:", uniq_match.count(True),"/",len(uniq_match), "-->", round(100*uniq_match.count(True)/len(uniq_match),2),"%")
	print("*********", time.time() - start_time,  "*********")



if __name__ == '__main__':
	main()