import unittest
from analyze_states import clean,candidates

class DetectionTests(unittest.TestCase):
    def test_numeric_county_record(self):
        found=candidates(clean('{"code":"us-ma-001","usd":12345}'))
        self.assertIn('json_literal',{k for k,v in found})
        self.assertIn('county_marker_candidate',{k for k,v in found})
    def test_encoded_request_is_not_a_record(self):
        self.assertEqual(candidates(clean('[https://example.test/?jq=%7Bcode%3A%22us-ma-001%22%2Cusd%3A12345%7D Result]')),[])
    def test_data_with_source_url_is_retained(self):
        found=candidates(clean('{"source":"https://example.test/a","code":"us-ma-001","usd":12345}'))
        self.assertIn('json_literal',{k for k,v in found})
    def test_county_table(self):
        found=candidates(clean('| Barnstable | 2019 | 12345 |'))
        self.assertIn('table_candidate',{k for k,v in found})
    def test_plain_numeric_rows(self):
        self.assertIn('numeric_row',{k for k,v in candidates('Alabama: 448077,452440,457191')})
    def test_timestamp_is_not_decimal_result(self):
        self.assertEqual(candidates('Final concise meta J 1781814741.3219419'),[])

if __name__=='__main__':unittest.main()
