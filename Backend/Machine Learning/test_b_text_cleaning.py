import unittest
from b_text_cleaning import TextCleaning

class TestTextCleaning(unittest.TestCase):
    def setUp(self):
        # Mock directories for testing
        self.extracted_text_directory = 'mock_extracted_text_directory'
        self.cleaned_text_directory = 'mock_cleaned_text_directory'

        self.cleaner = TextCleaning(self.extracted_text_directory, self.cleaned_text_directory)

    def test_remove_pagination(self):
        test_text = "This is a test text.Seite 12 von 34 End of text."
        expected_result = "This is a test text. End of text."
        self.assertEqual(self.cleaner.remove_pagination(test_text), expected_result)

    def test_correct_hyphenation(self):
        test_text = "This is a hyphen-\nated test text."
        expected_result = "This is a hyphenated test text."
        self.assertEqual(self.cleaner.correct_hyphenation(test_text), expected_result)

    def test_standardize_formatting(self):
        test_text = "This is a test. New   Sentence."
        expected_result = "This is a test. \nNew Sentence."
        self.assertEqual(self.cleaner.standardize_formatting(test_text), expected_result)

    def test_remove_irrelevant_info(self):
        test_text = "Path: \\\\some\\path\\file.docx and contract number 1234567A."
        expected_result = "Path:  and contract number ."
        self.assertEqual(self.cleaner.remove_irrelevant_info(test_text), expected_result)

    def test_remove_spaces_from_title(self):
        test_text = "G E S E L L S C H A F T S V E R T R A G"
        expected_result = "GESELLSCHAFTSVERTRAG"
        self.assertEqual(self.cleaner.remove_spaces_from_title(test_text), expected_result)

if __name__ == '__main__':
    unittest.main()


#Ergebnisse:
""" 
.....
----------------------------------------------------------------------
Ran 5 tests in 0.002s

OK 
"""