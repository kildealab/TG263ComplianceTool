import re
import string
# from thefuzz import process
import os

import TG263ComplianceTool.loaders as loaders


common_mispellings = {
	'brachialplexus': 'brachialplex',
	'brachiaplex':'brachialplex',
	'brstem': 'brainstem',
	'greatvessels': 'greatves',
	'left':'L',
	'right':'R',
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


def get_proposed_name(name,tg_names=tg_names,use_fuzzy = False):
	reason = ""
	if (name[0] == 'Z' and len(name) <= 16):
		return 'z' + name[1:], "Capital Z should be z"
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
		
		if ('avoid' in name.lower() or 'nos' in name.lower() or 'ring' in name.lower() or ('opt' in name.lower() and 'optic' not in name.lower()) ):  #what to do with opt? since optic nerve
			if len(name) == 15:
				return "z"+name.replace(" ","_"), "consider adding z in front if not used for dose eval"
			elif len(name) < 15:
				return "z_"+name.replace(" ","_"), "consider adding z in front if not used for dose eval"
			else:
				return "", "need to start with z but name too long"
			
	
	if use_fuzzy:
		# print("in fuz")
		closest_match = process.extractOne(name, tg_names)


		return closest_match[0], 'using fuzzy'

	return '',''

def check_TG_name(name, tg_names=tg_names):
	original_length = len(name)
	original_name = name
	reason = ''

	if ' ' in name:
		reason = "spaces"
		return False, reason

	if len(name) > 16:
		reason = "> 16 characters"
		return False, reason
	
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


	
#*****************************************#
#*			    RULE #1  		  	 	 *#
#*****************************************#
def rule1_target_types(target_prefix):
	list_allowed_prefixes = ['PTV!','GTV','CTV','ITV','IGTV','ICTV','PTV'] # Rule 1
	if not target_prefix.startswith(tuple(list_allowed_prefixes)): # Rule 1: name does not start with an allowed prefix
		return target_prefix, False
		reason = "Fails rule 1 for target structures"
		return target_prefix, False, reason
	
	# If compliant with Rule 1, removes allowed prefix from word
	# Eg: if a name starts with GTVp, at this point the GTV will be removed and the remaining character(s) ('p') will be checked next.
	for p in list_allowed_prefixes: 
		if target_prefix.startswith(p):
			target_prefix = target_prefix.replace(p,'') # remove compliant characters for rule 1
			break
   
	
	return target_prefix, True, ''

#*****************************************#
#*			    RULE #2  		  	 	 *#
#*****************************************#
def rule2_target_classifiers(target_prefix):
	
	if target_prefix == '':
		return target_prefix, True, ''
	list_allowed_classifiers = ['n', 'sb', 'par','p', 'vas', 'v',''] # Rule 2 - target classifiers allowed, including none
		#note: ordering of the above matters, PTV! sb before PTV, and '' should be last -- this is for when removing it from prefix
		#note: similarly, the list allowed classifiers should have the longer names first if the start letter is also a valid classifier (eg vas before v)	
	
   	# If the prefix still contains characters after removing start letters, check if compliant. 
	
	compliant = True
	reason = ''
	# Check if remaining char(s) are an allowed classifier (Rule #2)
	if target_prefix[0].isalpha():
		compliant = False

		for c in list_allowed_classifiers:
			if target_prefix.startswith(c):
				compliant = True
				target_prefix = target_prefix.replace(c,'') # Remove compliant char(s) for rule 2
				
				break
		if not compliant:
			reason = 'Fails rule 2 for target classifiers'
	return target_prefix, compliant, reason

#*****************************************#
#*			    RULE #3  		  	 	 *#
#*****************************************#
def rule3_multiple_targets(target_prefix):
	# Check remaining char(s) in prefix after removing rule 1 and 2
	if target_prefix == '':
		return target_prefix, True, ''
			
	if target_prefix[0].isdigit(): # If next character is a digit, it is compliant (rule 3)
		target_prefix = target_prefix[1:] # Remove compliant digit

	# If there are still remaining char(s) and they do not match rule 8 (eg: ends with '-05' allowed), then fails compliance
	if len(target_prefix) != 0 and not bool(re.match( r'^-\d{2}$',target_prefix)):
		return target_prefix, False, "Non-compliant characters after prefix (target rules 1-3). _ or ^ might be needed."
		
	
	return target_prefix, True, ''


#*****************************************#
#*			    RULE #4 		  	 	 *#
#*****************************************#
def rule4_imaging_modality(target_suffix):
	allowed_modalities = ['CT','PT','MR','SP']

	split_suffix = target_suffix[1:].split("_")[0]

	modality_string = '_'
	while(True):
		if split_suffix.startswith(tuple(allowed_modalities)):

			if len(split_suffix) < 3 or not split_suffix[2].isdigit():
				return '',False, 'Imaging modality should be followed by sequential number (Target rule #4)'
			else:
				modality_string+=split_suffix[0:3]
				split_suffix = split_suffix[3:]
				# print(split_suffix)
		elif split_suffix.upper().startswith(tuple(allowed_modalities)):
			return '',False, 'Imaging modality name should be capitalized.'
		else:
			break

	if modality_string != '_':
		target_suffix = target_suffix.replace(modality_string,'')

	return target_suffix, True, ''


#*****************************************#
	#*			    RULE #5  		  	 	 *#
	#*****************************************#
def rule5_structure_indicators(target_suffix):
	if target_suffix == '':
		return '', True, ''
	
	if target_suffix[0] == "_":
		split_suffix_list = target_suffix[1:].split('_')

		found_struct = False
		if len(split_suffix_list) > 2:
			two_underscore = split_suffix_list[0]+"_"+split_suffix_list[1]+"_"+split_suffix_list[2]
			if check_TG_name(two_underscore)[0]:
				print("third check")
				target_suffix = target_suffix[1:].replace(two_underscore,'')
				found_struct = True


		if not found_struct and len(split_suffix_list) > 1:
			one_underscore =  split_suffix_list[0]+"_"+split_suffix_list[1]
			if check_TG_name(one_underscore)[0]:
				print("second check")
				target_suffix = target_suffix[1:].replace(one_underscore,'')
				found_struct = True

		if not found_struct and check_TG_name(split_suffix_list[0])[0]:
			target_suffix = target_suffix[1:].replace(split_suffix_list[0],'')

	return target_suffix, True, '' # Can't really claim false as words might be part of other rules

	
		
	
#*****************************************#
#*			    RULE #6  		  	 	 *#
#*****************************************#
def rule6_dose(target_suffix):
	if target_suffix == '':
		return '', True, ''

	relative_dose_suffixes = ["_High", "_Mid","_Low"]
	numerical_dose = False

	if target_suffix.startswith(tuple(relative_dose_suffixes)):
		for r in relative_dose_suffixes:
			if target_suffix.startswith(r):
				target_suffix = target_suffix.replace(r,'')

				# Rule 6 subpoint: Mid+2-digit enumerator
				if r == '_Mid':
					if re.match(r'\d{2}',target_suffix[0:2]):
						target_suffix = target_suffix[2:]
				break

	elif bool(re.match(r'^_\d{4}', target_suffix)): #cGy
		target_suffix = target_suffix[5:]
		numerical_dose = True

	elif 'Gy' in target_suffix:
		
		match = re.match(r'\b_\d{1,2}(?:\.\d{1,2}|p\d{1,2})?Gy',target_suffix)

		if match: # Extract the matched string 
			matched_text = match.group(0) # Remove the matched text from target_suffix 
			target_suffix = target_suffix.replace(matched_text, '')
			numerical_dose = True
	elif 'gy' in target_suffix.lower():
		return target_suffix, False, 'Gy should have the first letter capitalized.'
	elif re.match(r'\b_\d{1,2}(?:\.\d{1,2}|p\d{1,2})?',target_suffix):
		return target_suffix, False, 'Dose should be in cGy (4 digits), if not please specify "Gy" after the dose.'


	if numerical_dose: #rule 7, this is optional, only if the # fx are indicated it should be with an x
		target_suffix = rule7_dose_fractions(target_suffix)

	return target_suffix, True, ''

	#*****************************************#
	#*			    RULE #7 		  	 	 *#
	#*****************************************#
def rule7_dose_fractions(target_suffix):

	
	fraction_pattern = r'^x\d{1,2}'
	if bool(re.match(fraction_pattern, target_suffix)):
		fractions = True
		target_suffix = re.sub(fraction_pattern, '', target_suffix)
	return target_suffix
	
#*****************************************#
#*			    RULE #8  		  	 	 *#
#*****************************************#
def rule8_cropped_structure(target_suffix):

	if bool(re.match(r'^-\d{2}', target_suffix)):
		target_suffix = target_suffix[3:]

	return target_suffix, True, ''
	

def check_target_compliance(target_name,tg_names=tg_names):
	'''
	check_target_compliance	XXXXX The code works by going through each part of the target name and removing the parts 
							that comply from beginning to end of word. This means the code can go through the rules one
							at a time to check for compliance. TODOL add link to paper, section 8.2
	'''

	reason = ''
	#first check if there are spaces, then it's automatically not TG 263 compliant
	if ' ' in target_name:
		reason = "spaces"
		return False, reason

	# Names must be max 16 characters
	if len(target_name) > 16:
		reason = "> 16 characters"
		return False, reason

	# Structures starting with 'z' are not used for dose evaluation and are thus ignored 
	if target_name[0] == "z":
		reason = "Ignore after z"
		return True, reason 
	
	#*****************************************#
	#*			    RULE #9  		  	 	 *#
	#*****************************************#
	if "^" in target_name: # Rule 9, ignore custom notes after ^
		target_name = target_name[:target_name.index("^")]

	if target_name in additional_allowed_names:
		return True, reason


	# Split the name up: everything preceding the first '_' is called the prefix, everything following is the suffix
	target_prefix = target_name.split("_")[0]
	target_suffix = target_name.replace(target_prefix,'')
	
	
	


	# CHECKING PREFIX
	# RULE 1
	target_prefix, compliant, reason = rule1_target_types(target_prefix)
	if not compliant:
		return False, reason
	if debug:
		print("Prefix after Rule 1:",target_prefix)

	# RULE 2
	target_prefix, compliant, reason = rule2_target_classifiers(target_prefix)
	if not compliant:
		return False, reason
	if debug:
		print("Prefix after rule 2:",target_prefix)
			
	# RULE 3 - note also accounts for rule 8 if no suffix (eg: PTV-03)
	target_prefix, compliant, reason = rule3_multiple_targets(target_prefix)
	if not compliant:
		return False, reason
	if debug:
		print("After Rule 3: Prefix:",target_prefix, ", Suffix:", target_suffix)
			

	# CHECKING SUFFIX
	
	

	if target_suffix != '': # If there were character(s) after '_' in the original target name, check their compliance

		# RULE 4
		target_suffix, compliant, reason = rule4_imaging_modality(target_suffix)
		if not compliant:
			return False, reason
		if debug:
			print("Target suffix after rule 4:", target_suffix)

		#RULE 5
		target_suffix, compliant, reason = rule5_structure_indicators(target_suffix)
		if not compliant:
			return False, reason
		if debug:
			print("After rule 5", target_suffix)

		# RULEs 6 & 7
		target_suffix, compliant, reason = rule6_dose(target_suffix)
		if debug:
			print("After rules 6 & 7: ", target_suffix)

		# RULE 8
		target_suffix, compliant, reason = rule8_cropped_structure(target_suffix)
		if debug:
			print("after rule 8:", target_suffix)

	
	# Remaining suffix whould be empty or '^' followed by custom text (Rule 9)
	if target_suffix == '' or target_suffix[0] == "^":

		if target_name not in additional_allowed_names:
			additional_allowed_names.append(target_name)
		return True, reason
	else:
		reason = "Suffix leftover: " + target_suffix
		return False, reason

def get_additional_names():
	return additional_allowed_names

