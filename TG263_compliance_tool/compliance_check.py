import re
import string
from thefuzz import process
import os

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

additional_allowed_names = []


def get_proposed_name(name,tg_names,use_fuzzy = False):
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

def check_TG_name(name, tg_names):
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


	


def check_target_compliance(target_name,tg_names=[]):
	'''
	check_target_compliance	XXXXX The code works by going through each part of the target name and removing the parts 
							that comply from beginning to end of word. This means the code can go through the rules one
							at a time to check for compliance. TODOL add link to paper, section 8.2
	'''
	debug = False
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
	
	if "^" in target_name: # Rule 9, ignore custom notes after ^
		target_name = target_name[:target_name.index("^")]

	# Split the name up: everything preceding the first '_' is called the prefix, everything following is the suffix
	target_prefix = target_name.split("_")[0]
	target_suffix = target_name.replace(target_prefix,'')
	
	if debug:
		print("****")

		print("prefix", target_prefix)
#     print("suffix", target_suffix)

	is_correct = True
	# reasoning = ''
	
	if target_name in additional_allowed_names:
		return True, reason

	# CHECKING PREFIX
	list_allowed_prefixes = ['PTV!','GTV','CTV','ITV','IGTV','ICTV','PTV'] # Rule 1
	list_allowed_classifiers = ['n', 'p', 'sb', 'par', 'v', 'vas',''] # Rule 2 - target classifiers allowed, including none
	#note: ordering of the above matters, PTV! sb before PTV, and '' should be last -- this is for when removing it from prefix
	
	if not target_prefix.startswith(tuple(list_allowed_prefixes)): # Rule 1: name does not start with an allowed prefix
		reason = "Fails rule 1 for target structures"
		return False, reason
	
	# If compliant with Rule 1, removes allowed prefix from word
	# Eg: if a name starts with GTVp, at this point the GTV will be removed and the remaining character(s) ('p') will be checked next.
	for p in list_allowed_prefixes: 
		if target_prefix.startswith(p):
			target_prefix = target_prefix.replace(p,'') # remove compliant characters for rule 1
			break
   
	if debug:
		print("After Rule 1:",target_prefix)

	
	
	
   	# If the prefix still contains characters after removing start letters, check if compliant. 
	if target_prefix != '':
#         if target_prefix[0] == "^": # rule 9
#             if debug:
#                 print("its true, all after ^")
#             return True, reason
		
		# need to check rule 8 again, since could show up in prefix if no _
		
		# Check if remaining char(s) are an allowed classifier (Rule #2)
		if target_prefix[0].isalpha():
			compliant = False
			for c in list_allowed_classifiers:
				if target_prefix.startswith(c):
					compliant = True
					target_prefix = target_prefix.replace(c,'') # Remove compliant char(s) for rule 2
					break
			if not compliant:
				reason = "Fails rule 2 for target structures"
				return False, reason
		if debug:
			print("After rule 2:",target_prefix)
			
		'''
		prefix_no_digits = target_prefix.rstrip(string.digits)
		if debug:
			print("prefix no digits:",prefix_no_digits)
		if not prefix_no_digits in list_allowed_classifiers: #rule 2
			reason = "Fails rule 2"
			return False, reason
		
		
		for c in list_allowed_classifiers:
			if target_prefix.startswith(c):
				target_prefix = target_prefix.replace(c,'')
				break
		if debug:
			print("After rule 2:",target_prefix)
		'''
		
		# Check remaining char(s) in prefix after removing rule 1 and 2
		if target_prefix != '':
			if target_prefix[0].isdigit(): # If next character is a digit, it is compliant (rule 3)
				target_prefix = target_prefix[1:] # Remove compliant digit
			
			# If there are still remaining char(s) and they do not match rule 8 (eg: ends with '-05' allowed), then fails compliance
			if len(target_prefix) != 0 and not bool(re.match( r'^-\d{2}$',target_prefix)):
				reason = "Non-compliant characters after prefix (target rules 1-3). _ or ^ might be needed."
				return False, reason
		
		'''
		if target_prefix != '' and (len(target_prefix) > 1 or not target_prefix.isdigit()):
			# rule #3 --> could be tricky, saying len sb max 1 becuase i doubt the bunbers would go up to 10
			#but... there could be a random number there that isn't meant to represnet spatially distinct targets.
			reason = "fails rule 3"
			return False, reason
		'''
			
			
	# TO DO -- check if ends with -xx for prefix eg CTVp2-05 ^^ this is achieved above
	
	# CHECKING SUFFIX
	
	# TO DO: SKIPPING RULES 4 AND 5 FOR NOW
	# for rule 5, check thorugh TG again, however will need to do starts with i believe to accoutn for extra dose etc put at end
	# then need to remove it and analyse rest of structure as before


	if target_suffix != '': # If there were character(s) after '_' in the original target name, check their compliance
		# rule #5
		split_suffix = target_suffix[1:].split("_")[0]
		# print("target", target_suffix)
		# print("split",split_suffix)
		if target_suffix[0] == "_" and split_suffix in tg_names:
			target_suffix = target_suffix[1:].replace(split_suffix,'')

		# rule #6
	

		relative_dose_suffixes = ["_High", "_Mid","_Low"]
		if debug:
			print("suffix", target_suffix)

		numerical_dose = False
		if target_suffix.startswith(tuple(relative_dose_suffixes)):
			#ok it is relavice dose
			# TO DO: add 01 02 etc
			for r in relative_dose_suffixes:
				if target_suffix.startswith(r):
					target_suffix = target_suffix.replace(r,'')
					break

			placeholder = 1

		elif bool(re.match(r'^_\d{4}', target_suffix)): #cGy
			target_suffix = target_suffix[5:]
			placeholder = 2
			numerical_dose = True
	#     elif : TO DO : Gy

		if debug:
			print("After rule 6: ", target_suffix)
		if numerical_dose: #rule 7, this is optional, only if the # fx are indicated it should be with an x
			fraction_pattern = r'^x\d{1,2}'
			if bool(re.match(fraction_pattern, target_suffix)):
				fractions = True
				target_suffix = re.sub(fraction_pattern, '', target_suffix)

			if debug:
				print("After rule 7: ", target_suffix)

		#rule 8
		if bool(re.match(r'^-\d{2}', target_suffix)):
			target_suffix = target_suffix[3:]

			if debug:
				print("after rule 8:", target_suffix)

		# rule 9
	if target_suffix == '' or target_suffix[0] == "^":
#             print("ALL GOODDDDDD")
		if target_name not in additional_allowed_names:
			additional_allowed_names.append(target_name)
		return True, reason
	else:
#             print("FAILED~!", target_suffix)
		reason = "Suffix leftover: " + target_suffix
		return False, reason

def get_additional_names():
	return additional_allowed_names

