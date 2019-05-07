# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:54:45 2016

@author: ringoyen
"""
import numpy as np
import unittest

class tester(unittest.TestCase):

    def test_low_pass_filter(self):
        """
        Unit Test for a moving averager (convolution) to serve as a low pass filter to remove noise

        :return:
        """

        from estimateHeartRate import low_pass_filter
        import numpy as np

        # define inputs for function

        ecg_data_1 = np.array([1, 2, 3, 4, 5, 6, 7])
        ecg_data_2 = np.array([2, 2, 2, 2, 2, 2, 2])

        # define outputs for function



        ecg_clean_1 = np.array([1.2,  2.,  3.,  4.,  5.,  4.4,  3.6])
        ecg_clean_2 = np.array([1.2,  1.6,  2.,  2.,  2.,  1.6,  1.2])
        # Place inputs in function

        clean_ecg_1 = low_pass_filter(ecg_data_1)
        clean_ecg_2 = low_pass_filter(ecg_data_2)

        # Unit Tests

        self.assertEquals(np.all(ecg_data_1),np.all(clean_ecg_1), msg = 'low pass filter does not work!')
        self.assertEquals(np.all(ecg_data_2), np.all(clean_ecg_2), msg='low pass filter does not work!')
        self.assertEquals(len(ecg_data_1),len(clean_ecg_1), msg = 'low pass filter gives wrong output length!')

    def test_remove_dc_offset(self):
        """

        Unit Test for removing DC offset from data

        :return:
        """

        from estimateHeartRate import remove_dc_offset
        import numpy as np

        # define inputs for function
        a = np.array([5.0,5.0,5.0,5.0])
        b = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        c = np.array([3.45, 2.46, 4.32, 5.56])

        # Define known output of function
        ecgKnown_1 = [0.0, 0.0, 0.0, 0.0]
        ecgKnown_2 = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ecgKnown_3 = [-0.4975, -1.4875, 0.3725, 1.61]

        # Place values in function
        noOffset_1 = remove_dc_offset(a)
        noOffset_2 = remove_dc_offset(b)
        noOffset_3 = remove_dc_offset(c)

        self.assertEqual(np.all(ecgKnown_1), np.all(noOffset_1), msg ='ECG values incorrect')
        self.assertEqual(np.all(ecgKnown_2), np.all(noOffset_2), msg='ECG values incorrect')
        self.assertEqual(np.all(ecgKnown_3),np.all(noOffset_3), msg = 'ECG values incorrect')
        self.assertEqual(len(ecgKnown_1), len(noOffset_1))
        self.assertEqual(len(ecgKnown_2), len(noOffset_2))


    def test_findThreshold(self):
        
        """
        This tests the ability of the function to determine the maximum value in a given data
        stream, and use it to determine the threshold value
        
        """
        
        from estimateHeartRate import findThreshold
        
        # Define inputs for function
        a = np.linspace(1, 1000, 1000)

        f_s_1 = 100
        f_s_2 = 200
        
        # Define known output for function
        # should be 750, but changed to 800 to check git
        threshknown_1 = 425
        threshknown_2 = 850
        
        # Place values in function
        thresh_1 = findThreshold(a, f_s_1)
        thresh_2 = findThreshold(a, f_s_2)
        
        self.assertEqual(threshknown_1,thresh_1, msg='Threshold not correct')
        self.assertEqual(threshknown_2,thresh_2, msg='Threshold not correct')


    def test_find_instantaneous_heart_rate(self):
        """ 
        This tests the ability of the function to determine the times and ECG values
        when there is an actual heartbeat occuring.  This is supposed to happen at the peaks (max values) of the
        traces.  There are 2 sets of test arrays I am using
        
        """

        from estimateHeartRate import find_instantaneous_heart_rate

        #Define inputs vectors for function
        ecg_vals_1 = [1, 1, 1, 5, 6, 1, 1, 10, 1, 1, 11, 5]
        ecg_time_1 = [1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12.]
        
        ecg_vals_2 =[1,4.5,1,1,1,6,1]
        ecg_time_2 =[1.,2.,3.,4.,5.,6.,7.]

        ecg_threshold = 4
        
        # Define known outputs of function
        instant_hr_1 = [20.]
        instant_hr_2 = [15.]


        # Define function with inputs
        actual_hr_1 = find_instantaneous_heart_rate(ecg_vals_1,ecg_time_1,ecg_threshold)
        actual_hr_2 = find_instantaneous_heart_rate(ecg_vals_2,ecg_time_2,ecg_threshold)
        
        self.assertEqual(instant_hr_1,actual_hr_1, 'msg = instant hr is wrong!')
        self.assertEqual(instant_hr_2, actual_hr_2, 'msg = instant hr is wrong!')





if __name__ == '__main__':
    unittest.main()