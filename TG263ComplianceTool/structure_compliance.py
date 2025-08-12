import re
import string
# from thefuzz import process, fuzz
import os

import TG263ComplianceTool.loaders as loaders


common_mispellings = {
	'brachialplexus': 'brachialplex',
	'brachiaplex':'brachialplex',
	'bronchialtree':'bronchus',
	'bronchtree':'bronchus',
	'brstem': 'brainstem',
	'greatvessels': 'greatves',
	'left':'L',
	'right':'R',
	'nonadj':'nadj',
	'upper':'S',
	'inf':'I',
	'optchiasm':'opticchiasm',
	'optnerv':'opticnrv',
	'optnrv':'opticnrv',
	'opticnerve':'opticnrv',
	'optnerv':'opticnrv',
	'optnrv':'opticnrv',
	'spine':'spinal',
	'submandibular': 'submand',
	'submandibula':'submand',
	'submndsalv':'submand',
	'surgbed':'surgicalbed',
	'templobe':'temporallobe'
	
	
	
}
debug = True

print("Loading TG names...")
# Loads the CSV with additional nomenclatures that are TG 263 compliant, but not explicitly in the original CSV
# Names were automatically added after passing through the compliance check in this code. 
# This CSV is unecessary, but saves time for repeated words that have already been checked.
fd = os.path.abspath(os.path.dirname(__file__)) # current file directory, for constructing relative paths later
additional_allowed_names = loaders.load_additional_names(os.path.join(fd,"../data/additional_allowed_names.csv"))
tg_names, tg_names_rev = loaders.load_tg_263(tg_path=os.path.join(fd,"../data/"))


def check_in_TG(name,tg_names=tg_names):
	if name in tg_names:
		return True
	return False


def get_proposed_name(name,tg_names=tg_names, use_fuzzy = False):
	reason = ""
	if (name[0] == 'Z' and len(name) <= 16):
		return 'z' + name[1:].replace(" ","_"), "Capital Z should be z"
	if (name[0] == 'z' or name[0] == "_") and ' ' in name and len(name)<= 16:
		return name.replace(" ","_"), "spaces"
	
	# print("Added names:" , additional_allowed_names)
		
	name_nosymbols = re.sub(r'[0-9]','',re.sub(r'[^\w]', '', name).lower()).replace(" ","").replace("_","")
	# print(name_nosymbols)
	tg_names = tg_names + additional_allowed_names
	if any(substring in name_nosymbols for substring in common_mispellings.keys()):
		for key in common_mispellings.keys():
			if key in name_nosymbols:
				name_nosymbols = name_nosymbols.replace(key,common_mispellings[key])
				name = name.replace(key,common_mispellings[key])
				reason = "common mispelling of TG term"

	tg_names.sort(key=len, reverse=False)
	for tg_name in tg_names:
		# to do: inefficient, do this one time only for removeing symbols
		tg_name_nosymbols = re.sub(r'[0-9]','',re.sub(r'[^\w]', '', tg_name).lower()).replace("_","")
	#         print(tg_name_nosymbols)
	#         print()


		if name.lower() == tg_name.lower():
			# print("casing")
			return tg_name, "casing"

		elif name.lower().replace(" ", "") == tg_name.lower():
			# print()
			return tg_name, "spaces"

		elif (tg_name_nosymbols == name_nosymbols):
			if 'prv' in tg_name_nosymbols:
				two_num = True
				
				if bool(re.search(r'PRV\d{2}', name)):
					insert_index = tg_name.find('PRV') + len('PRV') 
					# print(tg_name.find('PRV'))
					digits_to_insert = re.search(r'PRV\d{2}', name).group(0)[-2:]
					# print(insert_index)
					if len(tg_name) < 15:
						new_string = tg_name[0:insert_index] + digits_to_insert + tg_name[insert_index:]
						
						return new_string, "error with symbols or casing" 
					elif len(tg_name) ==15:
						new_string = tg_name[0:insert_index] + digits_to_insert[-1] + tg_name[insert_index:]
						return new_string, "error with PRV numbers" 
				
				elif bool(re.search(r'PRV\d{1}', name)):
					insert_index = tg_name.find('PRV') + len('PRV') 
					# print("insert_index")
					digits_to_insert = re.search(r'PRV\d{1}', name).group(0)[-1]
					
					
					if len(tg_name) < 15:
						new_string = tg_name[0:insert_index] + "0"+digits_to_insert + tg_name[insert_index:]
						return new_string, "error with PRV numbers" 
					elif len(tg_name) ==15:
						new_string = tg_name[0:insert_index] + digits_to_insert + tg_name[insert_index:]
						return new_string, "error with symbols or casing" 
						
					
			return tg_name, reason

		elif name_nosymbols.replace(" ","") in tg_name_nosymbols:
			return tg_name, "Missing part of name?"
		else:
			split_name = name.lower().split("_")
			split_name.reverse()
			tg_name_rev = ''
			split_tg = tg_name.lower().split("_")
#             print(len(split_tg))
			
			if len(split_tg)>1:
				for t in reversed(split_tg):
					tg_name_rev = tg_name_rev + t
  

				if tg_name_rev[0] == "r" or tg_name_rev[0]=='l':
					
					tg_name_rev = tg_name_rev[1:] +tg_name_rev[0]
					# if 'temporal' in tg_name.lower():
					# 		print(tg_name_rev)

			if split_name == tg_name.lower().split("_"):
				return tg_name, "Wrong order of words"
			elif tg_name_rev == name_nosymbols.lower():
				return tg_name, "Wrong ordering of words and missing _"
		
#         elif name.lower().split("_").reverse() == tg_name.lower().split("_"):
#             return tg_name, "Wrong order of words"
		'''
		elif tg_name_nosymbols in name_nosymbols.replace(" ",""):
			return tg_name, "too many letters in name??"
		'''

		'''
		elif re.sub(r'[^\w]', '', name.lower().replace(' ','')) in re.sub(r'[^\w]', '', tg_name.lower().replace(' ','')):
			return tg_name, ""
		elif re.sub(r'[^\w]', '', tg_name.lower().replace(' ','')) == re.sub(r'[^\w]', '', name.lower().replace(' ','')):
			return tg_name, ""
		'''

		# add suggestions for common mispellings, common mistakes, adding ^ in front of garbage, etc
		
		if ('avoid' in name.lower() or 'nos' in name.lower() or 'ring' in name.lower() or ('opt' in name.lower() and 'optic' not in name.lower())):  #what to do with opt? since optic nerve
			if len(name) == 15:
				return "z"+name.replace(" ","_"), "consider adding z in front if not used for dose eval"
			elif len(name) < 15:
				return "z_"+name.replace(" ","_"), "consider adding z in front if not used for dose eval"
			else:
				return "", "need to start with z but name too long"
			
	
	if use_fuzzy:
		# print("in fuz")
		closest_match = process.extractOne(name, tg_names)
		return closest_match[0], fuzz.ratio(name,closest_match)

	return '',''

def check_TG_name(name, tg_names=tg_names):
	original_length = len(name)
	original_name = name
	reason = ''

	

	# RULE 1
	if len(name) > 16:
		reason = "Structure names should be 16 characters or less."
		return False, reason

	# RULE 5
	if ' ' in name:
		reason = "spaces"
		return False, reason

	# RULE 12
	if "^" in name: # Rule 12, ignore custom notes after ^
		name = name[:name.index("^")]

	if name in additional_allowed_names:
		return True, ''

	if name != '':
		#rule #14 (asssuming doesnt matter after z?)
		if name[0] =='z' or name[0] == "_":
			return True, "ignored"

		# check if names starts with a tg compliant name (NOTE TO DO THIS IS INEFFICIENT)
# 		if not name.startswith(tuple(tg_names)): # rule 1
# 			reason = "fails rule 1"
# 			return False, reason
		tg_start = False
		tg_names.sort(key=len, reverse=True) # sort longest to shortest so to avoid picking brain before brainstem
		for n in tg_names: 
			if 'PRV' in n:
				n = n.replace('_PRVxx','').replace("_PRVx",'').replace('_PRV','')
			if name.startswith(n):
# 				if len(name) > len(n) and name[len(n)].isalpha():
# 					continue
				tg_start = True
				name = name.replace(n,'')
				break
			elif n.endswith("s") and (name.startswith(n[:-1]+"~") or (name.startswith(n[:-1]+"_PRV") and (name.endswith("_L") or name.endswith("_R")))):
				tg_start = True
				name = name.replace(n[:-1],'')
				break
			
		if not tg_start:
			return False, "Does not start with a TG compliant structure name"

		# Rule 3
		if name.startswith('s'):
			name = name[1:]
			
			if name[0:2] =="_L" or name[0:2]=="_R":
				name = name[2:]

		#Rule 11
		if name.startswith("~"):
			# need to check about for eg STRUCT~_L_PRV or STRUCT~_PRV_L
			name = name[1:]
			if name[0:2] =="_L" or name[0:2]=="_R":
				name = name[2:]
		''' version if not cutting outtg name from prefix
		if "~" in name:
			split_name = name.split("~")
			if split_name[0] in tg_names:
				if split_name[1].startswith("_L"):
					name = name.replace
			 and (len(split_name[1])==0 or split_name[1]=="_L" or split_name[1]=="_R":
		'''
		# rule 10
		if name.startswith("_PRV"):
			name = name.replace('_PRV','')
			
			# check for xx digits after PRV
			if bool(re.match(r'^\d{2}(?!\d)', name)):# if exactly 2 digits follow
				name = name[2:]
			elif bool(re.match(r'^\d{1}(?!\d)', name)) and original_length != 16:
				return False, "PRV should have 2 digits for mm since doesn't exceed 16 characters"
			elif bool(re.match(r'^\d{1}(?!\d)', name)):
				name = name[1:]

			# check if _L or _R follow PRV
			if len(name)>1 and (name[0:2] == "_L" or name[0:2] == "_R"):
				name = name[2:]


			# roi_name = seq.ROIName


	if name == '' or name[0] == "^": # can prob remove this now
#             print("ALL GOODDDDDD")
		if original_name not in additional_allowed_names and original_name not in tg_names:
			additional_allowed_names.append(original_name)
		return True, reason
	else:
#             print("FAILED~!", target_suffix)
		reason = "Suffix leftover: " + name
		return False, reason



def get_additional_names():
	return additional_allowed_names

