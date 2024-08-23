# import glob
import os
import time
# import json
# import pydicom as dcm
import pandas as pd 
import csv
# import re

from parse_DICOM_RS import load_RS_names, find_RS_files_recursive
from compliance_check import check_TG_name, check_target_compliance, get_proposed_name
from parse_xml_template import load_xml_data, parse_structure_xml

start_time = time.time()




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


def load_RS_data(path,check_file = False, write_files = False):


	if check_file and os.path.isfile('names_to_convert.csv'):
		with open('names_to_convert.csv','r') as f:
			rs_files = [row[0] for row in csv.reader(f)]
	else:
		rs_files = find_RS_files_recursive(path)#,avoid_root_keywords=["_CBCT_","PlanAdapt","QA","old","TEST"])
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


path = '/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/'
# path = '/mnt/iDriveShare/Kayla/CBCT_images/Kayla_extracted/'



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
tg_names, tg_names_rev = load_tg_263()
print(len(tg_names))
print(len(tg_names_rev))
'''
names_to_convert = []

# note: ~ used to denote partial structures, e.g. Brain~, Lung~_L
temp_struct_avoid = []#['nos','~','z_']
for name in rt_names:
	if not any(keyword in name for keyword in temp_struct_avoid):
		if name in tg_names:
			k = 1
			# print("YES:",name)
		else:
			# print("NO",name)
			names_to_convert.append(name)

print(len(names_to_convert))


proposed_names = []
# TO DO : fix this weird loop/if mess

for name in names_to_convert:
	found = False
	# print(name)
	for tg_name in tg_names:
		if not found and name.lower() == tg_name.lower():
			proposed_names.append(tg_name)
			found = True
			# print(tg_name)
		elif not found and name.lower() in tg_name.lower():
			proposed_names.append(tg_name)
			found = True
			# print(tg_name)
		elif not found and tg_name.lower() in name.lower():
			proposed_names.append(tg_name)
			found = True
			# print(tg_name)
		# 
	if not found:
		proposed_names.append('')
		# print(tg_name)

print(proposed_names)

print(len(names_to_convert))

print(len(proposed_names))
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

# path =

path = '/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/'

# path = '/mnt/iDriveShare/Kayla/CBCT_images/Kayla_extracted/'

rs_files, new_names = load_RS_data(path)

path = '/mnt/iDriveShare/Kayla/StructureTemplates/'
rs_files, new_names = load_xml_data(path)

check_file = True
write_files = False
print(rs_files, new_names)
print("done calling load rs data")

xml_ids, xml_types, temp_apps, temp_sites, last_approvals, names, vol_types, codes = [],[],[],[],[],[],[],[]

for i in range(len(rs_files)):
	print(i)
	#TODO: messy calling multiple times
	temp_id, temp_type, temp_app, temp_site, last_approval, ids, namex, vol_type, code =parse_structure_xml(path+rs_files[i])

	for j in range(len(new_names[i])):
		print(j)
		
		col_file.append(rs_files[i].replace(path,""))
		xml_ids.append(temp_id)
		xml_types.append(temp_type)
		temp_apps.append(temp_app)
		temp_sites.append(temp_site)
		last_approvals.append(last_approval) 
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


			if name in tg_names:
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
					match, reason = check_target_compliance(name, tg_names)
					
				
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
'''
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
	writer.writerow(["File","ID","type","ApprovalStatus","Site","lastApproval","name","volumeType","code","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
	writer.writerows(zip(col_file,xml_ids,xml_types,temp_apps,temp_sites,last_approvals,names,vol_types,codes, col_name,col_length,col_match,col_propname,col_reason,col_type,col_rules))

with open("unique_list_structs_xml.csv","w") as f:
	writer = csv.writer(f)
	writer.writerow(["In-House Name","Instances","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
	writer.writerows(zip(uniq_name, instances, uniq_length,uniq_match,uniq_propname,uniq_reason,uniq_type,uniq_rules))




print("*********", time.time() - start_time,  "*********")


# # data_to_write = [[x] for x in names_to_convert]
# with open("names_to_convert.csv","w") as f:
# 	writer = csv.writer(f)
# 	writer.writerow(["non-compliant name","TG-263 suggestion"])
# 	writer.writerows(zip(names_to_convert,proposed_names))



# df = pd.DataFrame({"Non-compliant Nomenclature":names_to_convert})
# df.to_csv(index=False)
