import TG263ComplianceTool.structure_compliance as check

structure_examples = {
	'rule3': ['Lungs','Kidneys','Hippocampi', 'LNs','Ribs_L'],
	'rule46':['Femur_Head','Ears_External','Bowel_Bag'],
	'rule7': ['Lung_L', 'Lung_LUL', 'Lung_RLL', 'OpticNrv_PRV03_L'],
	'rule8': ['SeminalVes','SeminalVes_Dist'],
	'rule9': ['A_Aorta','A_Carotid','V_Portal','V_Pulmonary','LN_Ax_L1','LN_IMN','CN_IX_L','CN_XII_R',
			 'Glnd_Submand','Bone_Hyoid','Bone_Pelvic','Musc_Masseter','Musc_Sclmast_L','Spc_Bowel','Spc_Retrophar_L',
			 'Sinus_Frontal','Sinus_Maxillary'],
	'rule10': ['Brainstem_PRV','SpinalCord_PRV05','Brainstem_PRV03','OpticChiasm_PRV3'],
	'rule11': ['Brain~','Lung~_L','Lungs~'],
	'rule12': ['Lungs^Ex'],
	'rule13-15': ['Kidney_R', 'Kidney_Cortex_L', 'Kidney_Hilum_R','CaudaEquina','zPTVopt','A_Carotid_A'],
	# 'added':['Eyes_L','Ribs_L']
	

}


for key in structure_examples:
    for structure in structure_examples[key]:
        print("**************** Testing Structure:",structure,"******************************")
        print(check.check_TG_name(structure))
