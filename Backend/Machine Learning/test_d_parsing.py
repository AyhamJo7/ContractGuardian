import unittest
import os
import json
from unittest.mock import patch, mock_open
from d_parsing import parse_jsonl, extract_data, compile_data_for_file, generate_report
import pandas as pd

class TestDParsing(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"text": "Sample text RED FLAG", "entities": [{"label": "RED FLAG", "text": "RED FLAG"}]},
            {"text": "Another sample Orange Flag", "entities": [{"label": "Orange Flag", "text": "Orange Flag"}]}
        ]

    def test_parse_jsonl(self):
        test_jsonl_content = '\n'.join(json.dumps(item) for item in self.test_data)
        with patch("builtins.open", mock_open(read_data=test_jsonl_content)) as mock_file:
            result = parse_jsonl("fake_path.jsonl")
            mock_file.assert_called_once_with("fake_path.jsonl", 'r', encoding='utf-8')
            self.assertEqual(result, self.test_data)

    def test_extract_data(self):
        extracted = extract_data(self.test_data)
        self.assertIn("Sample text RED FLAG", extracted)
        self.assertIn("RED FLAG", extracted["Sample text RED FLAG"]["flags"])

    def test_compile_data_for_file(self):
        with patch('d_parsing.parse_jsonl', return_value=self.test_data):
            result = compile_data_for_file("fake_path.jsonl")
            self.assertIn("Sample text RED FLAG", result)

    def test_generate_report(self):
        all_data = {"fake_file.jsonl": extract_data(self.test_data)}
        expected_df = pd.DataFrame([
            {"File": "fake_file.jsonl", "Section": "Sample text RED FLAG", "Flags": "RED FLAG", "Clauses": ""},
            {"File": "fake_file.jsonl", "Section": "Another sample Orange Flag", "Flags": "Orange Flag", "Clauses": ""}
        ])
        
        with patch("pandas.DataFrame") as mock_df:
            generate_report(all_data, "fake_report.csv")
            mock_df.assert_called_once() 
            mock_df.return_value.to_csv.assert_called_once_with("fake_report.csv", index=False) 

if __name__ == '__main__':
    unittest.main()

#Ergebnisse:
"""
....
----------------------------------------------------------------------
Ran 4 tests in 0.004s

OK
"""