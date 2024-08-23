import re
import string

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
	debug = False
	reason = ''
	#first check if there are spaces, then it's automatically not tg 263 compliant
	if ' ' in target_name:
		reason = "spaces"
		return False, reason

	if len(target_name) > 16:
		reason = "> 16 characters"
		return False, reason
	
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
		if target_prefix[0] == "^": # rule 9
			if debug:
				print("its true, all after ^")
			return True, reason
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
	# rule #6
	
	if target_suffix != '':
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