import unittest
import pandas as pd 
import os 

class VolareTest(unittest.TestCase):

    def get_data(folder):
        path = os.getcwd() + folder
        files = os.listdir(path)
        df = pd.DataFrame()
        for f in files:
            if (f.endswith('xlsx')):
                data = pd.read_excel(path + f)
                df = pd.concat([df, data], ignore_index=True)
        return df
    
    def test_aug_1_info(self):
        aug_1_data = self.get_data('/data/SFO-Aug/8:1.xlsx')
        total = len(aug_1_data)
        self.assertEqual(total, 294)

    def test_specials(self):
        return
    
    if __name__ == '__main__':
        test_aug_1_info()
        unittest.main()
