import unittest
from TG263_compliance_tool import compliance_check

class TestComplianceCheck(unittest.TestCase):
    def test_common_misspellings(self):
        self.assertEqual(compliance_check.common_mispellings['brachialplexus'], 'brachialplex')
        self.assertEqual(compliance_check.common_mispellings['brstem'], 'brainstem')

    def test_check_in_TG(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertTrue(compliance_check.check_in_TG('brainstem', tg_names))
        self.assertFalse(compliance_check.check_in_TG('unknown_name', tg_names))

    def test_get_proposed_name(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertEqual(compliance_check.get_proposed_name('Zbrainstem', tg_names), ('zbrainstem', "Capital Z should be z"))
        self.assertEqual(compliance_check.get_proposed_name('z brainstem', tg_names), ('z_brainstem', "spaces"))

    def test_check_TG_name(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertTrue(compliance_check.check_TG_name('brainstem', tg_names))
        self.assertFalse(compliance_check.check_TG_name('unknown_name', tg_names))

    def test_check_target_compliance(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertTrue(compliance_check.check_target_compliance('brainstem', tg_names))
        self.assertFalse(compliance_check.check_target_compliance('unknown_target', tg_names))

    def test_special_characters(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertEqual(compliance_check.get_proposed_name('brainstem_1', tg_names), ('brainstem_1', ''))

    def test_length_restriction(self):
        tg_names = ['brainstem', 'brachialplex']
        self.assertFalse(compliance_check.check_target_compliance('longname_exceeding_16_characters', tg_names))

    def test_prv_handling(self):
        tg_names = ['PRV_liver', 'brainstem']
        self.assertEqual(compliance_check.get_proposed_name('PRV_liver_1', tg_names), ('PRV_liver_1', ''))

    def test_additional_allowed_names(self):
        self.assertIn('submand', compliance_check.additional_allowed_names)

if __name__ == '__main__':
    unittest.main()

