import re
import string

def get_proposed_name(name,tg_names):

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


		# add suggestions for common mispellings, common mistakes, adding ^ in front of garbage, etc
	return '',''


def check_TG_name(name, tg_names):
	original_length = len(name)
	reason = ''

	if ' ' in name:
		reason = "spaces"
		return False, reason

	if len(name) > 16:
		reason = "> 16 characters"
		return False, reason
	
	if "^" in name: # Rule 12, ignore custom notes after ^
		name = name[:name.index("^")]

	if name != '':
		#rule #14 (asssuming doesnt matter after z?)
		if name[0] =='z' or name[0] == "_":
			return True, "ignored"

		# check if names starts with a tg compliant name (NOTE TO DO THIS IS INEFFICIENT)
# 		if not name.startswith(tuple(tg_names)): # rule 1
# 			reason = "fails rule 1"
# 			return False, reason
		tg_start = False
		for n in tg_names: 
			if name.startswith(n):
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




	if name == '' or name[0] == "^": # can prob remove this now
#             print("ALL GOODDDDDD")
		return True, reason
	else:
#             print("FAILED~!", target_suffix)
		reason = "Suffix leftover: " + name
		return False, reason


	


def check_target_compliance(target_name,tg_names=[]):
	debug = False
	reason = ''
	#first check if there are spaces, then it's automatically not tg 263 compliant
	if ' ' in target_name:
		reason = "spaces"
		return False, reason

	if len(target_name) > 16:
		reason = "> 16 characters"
		return False, reason
	
	if "^" in target_name: # Rule 9, ignore custom notes after ^
		target_name = target_name[:target_name.index("^")]

	target_prefix = target_name.split("_")[0]
	target_suffix = target_name.replace(target_prefix,'')
	
	if debug:
		print("****")

		print("prefix", target_prefix)
#     print("suffix", target_suffix)

	is_correct = True
	reasoning = ''
  

	# CHECKING PREFIX
	list_allowed_prefixes = ['PTV!','GTV','CTV','ITV','IGTV','ICTV','PTV'] #rule 1
	list_allowed_classifiers = ['n', 'p', 'sb', 'par', 'v', 'vas',''] # rule 2, including none
	#note: ordering of the above mattes, PTV! sb before PTV, and '' should be last -- this is for when removing it from prefix
	
	if not target_prefix.startswith(tuple(list_allowed_prefixes)): # rule 1
		reason = "fails rule 1"
		return False, reason
	
	for p in list_allowed_prefixes: 
		if target_prefix.startswith(p):
			target_prefix = target_prefix.replace(p,'')
			break
   
	if debug:
		print("After Rule 1:",target_prefix)

	
	
	
	if target_prefix != '':
		# if target_prefix[0] == "^": # rule 9
		# 	if debug:
		# 		print("its true, all after ^")
		# 	return True, reason
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
		
		if target_prefix != '' and (len(target_prefix) > 1 or not target_prefix.isdigit()):
			# rule #3 --> could be tricky, saying len sb max 1 becuase i doubt the bunbers would go up to 10
			#but... there could be a random number there that isn't meant to represnet spatially distinct targets.
			reason = "fails rule 3"
			return False, reason
			
	# TO DO -- check if ends with -xx for prefix eg CTVp2-05
	
	# CHECKING SUFFIX
	
	# TO DO: SKIPPING RULES 4 AND 5 FOR NOW
	# for rule 5, check thorugh TG again, however will need to do starts with i believe to accoutn for extra dose etc put at end
	# then need to remove it and analyse rest of structure as before

	if target_suffix != '':
		# rule #5
		split_suffix = target_suffix[1:].split("_")[0]
		print("target", target_suffix)
		print("split",split_suffix)
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
		return True, reason
	else:
#             print("FAILED~!", target_suffix)
		reason = "Suffix leftover: " + target_suffix
		return False, reason