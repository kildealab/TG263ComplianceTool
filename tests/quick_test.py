import TG263ComplianceTool.target_compliance as check

target_examples = {

        'targets_rules_123':  ['GTV','PTV','CTV','ITV','IGTV','ICTV','PTV!','PTVn','GTVp','CTVsb','GTVpar','CTVv','CTVvas','PTV1','PTV2','GTVp1','GTVp2'],
        'targets_rules_45': ['PTVp1_CT1PT1','GTV_CT2','CTV_A_Aorta','CTV_A_Celiac','GTV_Preop','PTV_Boost','PTV_Eval','PTV_MR2_Prostate'],
        'targets_rule_6': ['PTV_High','CTV_High','GTV_High','PTV_Low','CTV_Low','GTV_Low','PTV_Mid','CTV_Mid','GTV_Mid','PTV_Mid01','PTV_Mid02','PTV_Mid03','PTV_5040','PTV_50.4Gy','PTV_50p4Gy'],
        'targets_rules_78': ['PTV_Liver_2000x3','PTV_Liver_20Gyx3','PTV_Eval_7000-08','PTV-03','CTVp2-05'],
        'targets_rule_9': ['PTV^Physician1','GTV_Liver^ICG'],
        'targets_user_added':['PTV_Liver_20Gy','PTV_20Gy-03']
    }

for key in target_examples:
    for target in target_examples[key]:
        print("**************** Testing Target:",target,"******************************")
        print(check.check_target_compliance(target))
