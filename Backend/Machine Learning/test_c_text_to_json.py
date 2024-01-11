import unittest
import os
import json
from unittest.mock import patch, mock_open
from c_text_to_json import read_file, split_into_sections, save_jsonl

class TestTextToJson(unittest.TestCase):
    def test_read_file(self):
        test_content = "Sample text content"
        with patch("builtins.open", mock_open(read_data=test_content)) as mock_file:
            result = read_file("fake_path.txt")
            mock_file.assert_called_once_with("fake_path.txt", 'r', encoding='utf-8')
            self.assertEqual(result, test_content)

    def test_split_into_sections(self):
        test_text = "§1 This is section one. §2 This is section two."
        expected_result = ["§1 This is section one.", "§2 This is section two."]
        result = split_into_sections(test_text)
        self.assertEqual(result, expected_result)

    def test_save_jsonl(self):
        test_data = [{"text": "Section 1"}, {"text": "Section 2"}]
        expected_file_content = '\n'.join(json.dumps(d, ensure_ascii=False) for d in test_data) + '\n'

        with patch("builtins.open", mock_open()) as mock_file:
            save_jsonl(test_data, "output.jsonl")
            mock_file.assert_called_once_with("output.jsonl", 'w', encoding='utf-8')

            written_content = ''.join(call_args[0][0] for call_args in mock_file().write.call_args_list)
            self.assertEqual(written_content, expected_file_content)


if __name__ == '__main__':
    unittest.main()

#Ergebnisse:
""" 
...
----------------------------------------------------------------------
Ran 3 tests in 0.005s

OK 
"""