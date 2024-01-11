import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from e_flags import process_flags

class TestProcessFlags(unittest.TestCase):
    def setUp(self):
        self.sample_data = pd.DataFrame({
            'Flags': ['RED FLAG', 'Orange Flag', None, 'Green Flag'],
            'OtherColumn': [1, 2, 3, 4]
        })

    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_process_flags(self, mock_to_csv, mock_read_csv):
        mock_read_csv.return_value = self.sample_data

        processed_df = process_flags('fake_input.csv', 'fake_output.csv')
        mock_read_csv.assert_called_once_with('fake_input.csv')
        mock_to_csv.assert_called_once_with('fake_output.csv', index=False)

        self.assertIn('Has_Red_Flag', processed_df.columns)
        self.assertIn('Has_Orange_Flag', processed_df.columns)
        self.assertIn('Has_Green_Flag', processed_df.columns)

        expected_flags = pd.DataFrame({
            'Has_Red_Flag': [1, 0, 0, 0],
            'Has_Orange_Flag': [0, 1, 0, 0],
            'Has_Green_Flag': [0, 0, 1, 1]
        }).astype(processed_df['Has_Red_Flag'].dtype) 

        pd.testing.assert_frame_equal(processed_df[['Has_Red_Flag', 'Has_Orange_Flag', 'Has_Green_Flag']], expected_flags)

if __name__ == '__main__':
    unittest.main()

#Ergebnisse:
""" 
.
----------------------------------------------------------------------
Ran 1 test in 0.003s

OK 
"""