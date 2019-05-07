# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 01:57:05 2016

@author: ringoyen
"""
import numpy as np
import unittest

class MyTest(unittest.TestCase):

    
    def test_reading_data(self):
        """

    
        """
        import numpy as np
        from readingDataSets import reading_data

        # Define known outputs

        # actual outputs for .bin file

        fs_actual = [1.]
        pp_actual = [3, 5, 7, 9]
        ecg_actual = [2,4,6,8,10]



        # Define output, with the input.bin file
        a, b, c = reading_data("unit_test.bin")


        self.assertEqual(fs_actual,a, msg = 'fs data incorrect' )
        self.assertEqual(np.all(pp_actual),np.all(b),msg = 'ecg data incorrect')
        self.assertEqual(np.all(ecg_actual), np.all(c), msg = 'pp data incorrect')

    
    def test_ecg_time(self):
        """
        This tests if the function properly generates a corresponding ECG time array
        
        """
        
        from readingDataSets import ecg_time

        actual_data = [0, 1.25, 2.5, 3.75, 5]
        ecg_test_data = [1, 2, 3, 4, 5]
        ecg_Time_Vals = ecg_time(ecg_test_data,1)
        
        self.assertEqual(ecg_Time_Vals[0],actual_data[0])
        self.assertEqual(ecg_Time_Vals[1],actual_data[1])
        self.assertEqual(ecg_Time_Vals[2],actual_data[2])
        self.assertEqual(ecg_Time_Vals[3],actual_data[3])
        self.assertEqual(ecg_Time_Vals[4],actual_data[4])
        
        self.assertEqual(len(ecg_Time_Vals),len(ecg_test_data))
        
        
        
        
        
        
        
   
    
if __name__ == '__main__':
    unittest.main()