import glob
import os
import time
import json
import pydicom as dcm
import pandas as pd 
import csv
import re

start_time = time.time()



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

# def initialize_json(json_path="."):

# 	if not os.path.isfile(os.path.join(json_path,"name_conversions.json")):

# def load_json(json_path="."):
# 	json_file = os.path.join(json_path,"name_conversions.json")
# 	if os.path.isfile(json_file):
# 		with open(json_file) as f:
# 			json_data = json.load(f)
# 			return json_data
# 	else:
# 		return {}



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

# def list_to_csv(data_list,col_names=[]):

# path = '/mnt/iDriveShare/Kayla/CBCT_images/test_rt_struct/'
path = '/mnt/iDriveShare/Kayla/CBCT_images/Kayla_extracted/'

check_file = True
write_files = False
if check_file and os.path.isfile('names_to_convert.csv'):
	with open('names_to_convert.csv','r') as f:
		rs_files = [row[0] for row in csv.reader(f)]
else:
	rs_files = find_RS_files_recursive(path,avoid_root_keywords=["_CBCT_","PlanAdapt","QA","old","TEST"])
	data_to_write = [[x] for x in rs_files]
	if write_files:
		with open("names_to_convert.csv","w") as f:
			writer = csv.writer(f)
			writer.writerows(data_to_write)

print(rs_files)
rs_files.sort()
# json_data = load_json()
# print(json_data)

new_names = load_RS_names(rs_files)
# print(new_names)



print(len(rs_files))
print(len(new_names))
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
def check_name_TG(name,tg_names):

	for tg_name in tg_names:
		if name.lower() == tg_name.lower():
			return tg_name, "casing"
		elif re.sub(r'[^\w]', '', name.lower().replace(' ','')) == re.sub(r'[^\w]', '', tg_name.lower().replace(' ','')):
			if "~" in name:
				if name.endswith("~") or name.endswith("~_R") or name.endswith("~_L"):
					return tg_name,"SB OK"
				return tg_name, "CHECK ~"
			return tg_name, "symbols"
		elif re.sub(r'[^\w]', '', name.lower().replace(' ','')) in re.sub(r'[^\w]', '', tg_name.lower().replace(' ','')):
			return tg_name, ""
		elif re.sub(r'[^\w]', '', tg_name.lower().replace(' ','')) == re.sub(r'[^\w]', '', name.lower().replace(' ','')):
			return tg_name, ""
		# 
	return '',''

def check_target_compliance(target_name):

	target_prefix = name[0:3]
	target_suffix = name[3:]
	print("prefix", target_prefix)
	print("suffix", target_suffix)

	is_correct = True
	reasoning = ''


	# #1 check first characters (to do add ICTV etc) -- todo change to starts with to add all
	if target_prefix != 'PTV' and != 'GTV' and != 'CTV':
		return False,'wrong prefix'
	
	# #2 check classifier
	if target_suffix[0] in ['n', 'p', 'sb', 'par', 'v', 'vas']:
		r

	# check if PTV_High, Mid, Low, etc.

	if target_suffix in ["_High", "_Mid","_Low"]
		return True, 'high/low/mid'


	# check if cGy dose
	if target_suffix[0] =="_" and len(target_suffix[1:]) == 4 and target_suffix[1:].isdigit():
		return True, "dose in cGy"





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


for i in range(len(rs_files)):
	print(i)
	for j in range(len(new_names[i])):
		
		col_file.append(rs_files[i].replace(path,""))

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

			if "gtv" in name.lower() or "ctv" in name.lower() or "ptv" in name.lower():
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
					proposed_name, reason = check_name_TG(name,tg_names, struct_type)
				else:
					#TODO call fn
				match = False
				col_match.append("False")
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

with open("full_list_structs.csv","w") as f:
	writer = csv.writer(f)
	writer.writerow(["File","In-House Name","Length","Matches TG-263","TG-263 suggestion","Reason","Structure Type","Rules"])
	writer.writerows(zip(col_file, col_name,col_length,col_match,col_propname,col_reason,col_type,col_rules))

with open("unique_list_structs.csv","w") as f:
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
