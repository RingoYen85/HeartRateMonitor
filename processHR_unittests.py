# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:51:13 2016

@author: ringoyen
"""

import unittest


class mytester(unittest.TestCase):
    
    def test_oneMinAvg(self):
     
        from processHR_functions import one_minute_avg
        
        # Define inputs for function

        ecg_time_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ecg_data_1 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_1 = 3
        time_counter_1 = 50
        interval_sec = 60

        ecg_time_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        ecg_data_2 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_2 = 3
        time_counter_2 = 75
        interval_sec = 60

        # Define known outputs for function

        one_min_avg_output_1 = 0.0
        one_min_avg_output_2 = 4.0

        # Place known values in function

        one_min_avg_func_1 = one_minute_avg(ecg_time_1, ecg_data_1, threshold_1, time_counter_1, interval_sec)
        one_min_avg_func_2 = one_minute_avg(ecg_time_2, ecg_data_2, threshold_2, time_counter_2, interval_sec)

        self.assertEqual(one_min_avg_output_1, one_min_avg_func_1, msg = 'one min average is wrong!, should not be anything yet')
        self.assertEqual(one_min_avg_output_2, one_min_avg_func_2, msg='one min avg is wrong !')


    def test_fiveMinAvg(self):

       from processHR_functions import five_minute_avg

       ecg_time_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
       ecg_data_1 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
       threshold_1 = 3
       time_counter_1 = 50
       interval_sec = 300

       ecg_time_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
       ecg_data_2 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
       threshold_2 = 3
       time_counter_2 = 300
       interval_sec = 300

       # Define known outputs for function

       five_min_avg_output_1 = 0.0
       five_min_avg_output_2 = 0.8

       # Place known values in function

       five_min_avg_func_1 = five_minute_avg(ecg_time_1, ecg_data_1, threshold_1, time_counter_1, interval_sec)
       five_min_avg_func_2 = five_minute_avg(ecg_time_2, ecg_data_2, threshold_2, time_counter_2, interval_sec)

       self.assertEqual(five_min_avg_output_1, five_min_avg_func_1, msg='one min average is wrong!, should not be anything yet')
       self.assertEqual(five_min_avg_output_2, five_min_avg_func_2, msg='one min avg is wrong !')


if __name__ == '__main__':
    unittest.main()


