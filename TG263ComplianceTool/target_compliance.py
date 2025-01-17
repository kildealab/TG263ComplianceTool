import re
import TG263ComplianceTool.structure_compliance as structure_compliance

additional_allowed_names = structure_compliance.get_additional_names()	

debug = False

#*****************************************#
#*			    RULE #1  		  	 	 *#
#*****************************************#
def rule1_target_types(target_prefix):
	list_allowed_prefixes = ['PTV!','GTV','CTV','ITV','IGTV','ICTV','PTV'] # Rule 1
	if not target_prefix.startswith(tuple(list_allowed_prefixes)): # Rule 1: name does not start with an allowed prefix
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
			if structure_compliance.check_TG_name(two_underscore)[0]:
				print("third check")
				target_suffix = target_suffix[1:].replace(two_underscore,'')
				found_struct = True


		if not found_struct and len(split_suffix_list) > 1:
			one_underscore =  split_suffix_list[0]+"_"+split_suffix_list[1]
			if structure_compliance.check_TG_name(one_underscore)[0]:
				print("second check")
				target_suffix = target_suffix[1:].replace(one_underscore,'')
				found_struct = True

		if not found_struct and structure_compliance.check_TG_name(split_suffix_list[0])[0]:
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
	

def check_target_compliance(target_name):
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
