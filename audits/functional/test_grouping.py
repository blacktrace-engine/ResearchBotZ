import unittest
from urllib.parse import quote
from analyze import classify

class GroupingTests(unittest.TestCase):
    base='https://www.sec.gov/files/county.json'
    def test_nonce_only_is_retained_as_variant(self):
        a,b=classify(self.base+'?uniq=1'),classify(self.base+'?uniq=2')
        self.assertEqual(a['group_id'],b['group_id'])
        self.assertNotEqual(a['transport_id'],b['transport_id'])
    def test_unknown_parameter_is_not_discarded(self):
        self.assertNotEqual(classify(self.base+'?foo=1')['group_id'],classify(self.base+'?foo=2')['group_id'])
    def test_year_is_not_masked(self):
        self.assertNotEqual(classify(self.base+'?Year=2019')['group_id'],classify(self.base+'?Year=2020')['group_id'])
    def test_double_slash_is_not_collapsed(self):
        self.assertNotEqual(classify(self.base)['group_id'],classify(self.base.replace('/files/','/files//'))['group_id'])
    def test_scheme_is_preserved(self):
        a,b=classify(self.base),classify(self.base.replace('https:','http:'))
        self.assertEqual(a['group_id'],b['group_id']);self.assertNotEqual(a['transport_id'],b['transport_id'])
    def test_transform_expression_retained(self):
        a=classify('https://jqp.vercel.app/api/v0?url='+quote(self.base,safe='')+'&jq='+quote('.regCF_county_2019',safe=''))
        b=classify('https://jqp.vercel.app/api/v0?url='+quote(self.base,safe='')+'&jq='+quote('.regCF_county_2020',safe=''))
        self.assertEqual(a['functional']['resource'],'www.sec.gov/files/county.json')
        self.assertNotEqual(a['group_id'],b['group_id'])
    def test_output_limit_retained_and_ambiguous_scope_flagged(self):
        a=classify('https://md.succ.ai/'+self.base+'?max_tokens=500')
        b=classify('https://md.succ.ai/'+self.base+'?max_tokens=1000')
        self.assertEqual(a['group_id'],b['group_id']);self.assertNotEqual(a['transport_id'],b['transport_id'])
        self.assertIn('path_wrapper_query_scope_ambiguous',a['flags'])
    def test_rendering_not_raw_retrieval(self):
        self.assertNotEqual(classify(self.base)['group_id'],classify('https://r.jina.ai/'+self.base)['group_id'])
    def test_shortener_unresolved(self):
        self.assertIn('shortener_destination_unknown',classify('https://is.gd/abc')['flags'])
    def test_counter_mutation_separate(self):
        self.assertEqual(classify('https://api.counterapi.dev/v1/example/key/up')['functional']['operation'],'counter-mutation-reference')
    def test_nested_wrapper(self):
        target='https://allorigins.hexlet.app/raw?url='+quote(self.base,safe='')
        a=classify('https://jqp.vercel.app/api/v0?url='+quote(target,safe='')+'&jq=.regCF_county_2019')
        self.assertEqual(a['functional']['resource'],'www.sec.gov/files/county.json')
        self.assertEqual([h['host'] for h in a['transport']['hops']],['jqp.vercel.app','allorigins.hexlet.app'])
    def test_undecodable_bare_host_wrapper_is_not_guessed(self):
        a=classify('https://md.succ.ai/www.sec.gov/files/county.json')
        self.assertIn('wrapper_unresolved_or_not_embedded',a['flags'])

if __name__=='__main__':unittest.main()
