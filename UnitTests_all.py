
import numpy as np
import unittest


class MyTest(unittest.TestCase):

    def test_reading_data(self):
        """ This function tests the reader function. A .bin file is run through and tested to see if the reader can properly
        detect it and read it using the proper reader method in the function.

        """
        import numpy as np
        from readingDataSets import reading_data

        # Define known outputs
        # actual outputs for .bin file
        fs_actual = [1.]
        pp_actual = [3, 5, 7, 9]
        ecg_actual = [2, 4, 6, 8, 10]

        # Define output, with the input.bin file
        a, b, c = reading_data("unit_test.bin")

        self.assertEqual(fs_actual, a, msg='fs data incorrect')
        self.assertEqual(np.all(pp_actual), np.all(b), msg='ecg data incorrect')
        self.assertEqual(np.all(ecg_actual), np.all(c), msg='pp data incorrect')

    def test_ecg_time(self):
        """ This tests if the function properly generates a corresponding ECG time array.

        """

        from readingDataSets import ecg_time

        actual_data = [0, 1.25, 2.5, 3.75, 5]
        ecg_test_data = [1, 2, 3, 4, 5]
        ecg_Time_Vals = ecg_time(ecg_test_data, 1)

        self.assertEqual(ecg_Time_Vals[0], actual_data[0])
        self.assertEqual(ecg_Time_Vals[1], actual_data[1])
        self.assertEqual(ecg_Time_Vals[2], actual_data[2])
        self.assertEqual(ecg_Time_Vals[3], actual_data[3])
        self.assertEqual(ecg_Time_Vals[4], actual_data[4])

        self.assertEqual(len(ecg_Time_Vals), len(ecg_test_data))

    def test_low_pass_filter(self):
        """ This is a unit test to check if the function will successfully smooth out the function and remove noise.

        """

        from estimateHeartRate import low_pass_filter
        import numpy as np

        # define inputs for function

        ecg_data_1 = np.array([1, 2, 3, 4, 5, 6, 7])
        ecg_data_2 = np.array([2, 2, 2, 2, 2, 2, 2])

        # define outputs for function

        ecg_clean_1 = np.array([1.2, 2., 3., 4., 5., 4.4, 3.6])
        ecg_clean_2 = np.array([1.2, 1.6, 2., 2., 2., 1.6, 1.2])
        # Place inputs in function

        clean_ecg_1 = low_pass_filter(ecg_data_1)
        clean_ecg_2 = low_pass_filter(ecg_data_2)

        # Unit Tests

        for i in range(0, len(ecg_data_1)):
            self.assertEquals(ecg_clean_1[i], (clean_ecg_1[i]), msg='low pass filter does not work!')

        self.assertEquals(np.all(ecg_data_2), np.all(clean_ecg_2), msg='low pass filter does not work!')
        self.assertEquals(len(ecg_data_1), len(clean_ecg_1), msg='low pass filter gives wrong output length!')

    def test_remove_dc_offset(self):
        """ This tests to see if the function can remove a dc offset from an array of ecg values.

        """

        from estimateHeartRate import remove_dc_offset
        import numpy as np

        # define inputs for function
        a = np.array([5.0, 5.0, 5.0, 5.0])
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

        for i in range (0, len(ecgKnown_1)):
            self.assertEqual((ecgKnown_1[i]), (noOffset_1[i]), msg='ECG values incorrect')

        self.assertEqual(np.all(ecgKnown_2), np.all(noOffset_2), msg='ECG values incorrect')
        self.assertEqual(np.all(ecgKnown_3), np.all(noOffset_3), msg='ECG values incorrect')
        self.assertEqual(len(ecgKnown_1), len(noOffset_1))
        self.assertEqual(len(ecgKnown_2), len(noOffset_2))

    def test_findThreshold(self):
        """ This tests the ability of the function to determine the maximum value in a given data
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

        self.assertEqual(threshknown_1, thresh_1, msg='Threshold not correct')
        self.assertEqual(threshknown_2, thresh_2, msg='Threshold not correct')

    def test_find_instantaneous_heart_rate(self):
        """ This tests the ability of the function to find the instantaneous heart rate

        """

        from estimateHeartRate import find_instantaneous_heart_rate

        # Define inputs vectors for function
        ecg_vals_1 = [1, 1, 1, 5, 6, 1, 1, 10, 1, 1, 11, 5]
        ecg_time_1 = [1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11., 12.]

        ecg_vals_2 = [1, 4.5, 1, 1, 1, 6, 1]
        ecg_time_2 = [1., 2., 3., 4., 5., 6., 7.]

        ecg_threshold = 4

        # Define known outputs of function
        instant_hr_1 = [20.]
        instant_hr_2 = [15.]

        # Define function with inputs
        actual_hr_1 = find_instantaneous_heart_rate(ecg_vals_1, ecg_time_1, ecg_threshold)
        actual_hr_2 = find_instantaneous_heart_rate(ecg_vals_2, ecg_time_2, ecg_threshold)

        self.assertEqual(instant_hr_1, actual_hr_1, 'msg = instant hr is wrong!')
        self.assertEqual(instant_hr_2, actual_hr_2, 'msg = instant hr is wrong!')

    def test_oneMinAvg(self):
        """ This tests to see if the function can properly find a one minute heart rate average

        """

        from processHR_functions import one_minute_avg

        # Define inputs for function

        ecg_data_1 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_1 = 3
        time_counter_1 = 50
        interval_sec = 60

        ecg_data_2 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_2 = 3
        time_counter_2 = 75
        interval_sec = 60

        # Define known outputs for function

        one_min_avg_output_1 = 0.0
        one_min_avg_output_2 = 4.0

        # Place known values in function

        one_min_avg_func_1 = one_minute_avg(ecg_data_1, threshold_1, time_counter_1, interval_sec)
        one_min_avg_func_2 = one_minute_avg(ecg_data_2, threshold_2, time_counter_2, interval_sec)

        self.assertEqual(one_min_avg_output_1, one_min_avg_func_1,
                         msg='one min average is wrong!, should not be anything yet')
        self.assertEqual(one_min_avg_output_2, one_min_avg_func_2, msg='one min avg is wrong !')

    def test_fiveMinAvg(self):
        """ This tests to see if the function can properly find a five min average of heart rate.

        """
        from processHR_functions import five_minute_avg

        ecg_data_1 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_1 = 3
        time_counter_1 = 50
        interval_sec = 300

        ecg_data_2 = [2, 2, 2, 3, 3, 3, 2, 6, 2, 10, 2, 5, 3]
        threshold_2 = 3
        time_counter_2 = 300
        interval_sec = 300

        # Define known outputs for function

        five_min_avg_output_1 = 0.0
        five_min_avg_output_2 = 0.8

        # Place known values in function

        five_min_avg_func_1 = five_minute_avg(ecg_data_1, threshold_1, time_counter_1, interval_sec)
        five_min_avg_func_2 = five_minute_avg(ecg_data_2, threshold_2, time_counter_2, interval_sec)

        self.assertEqual(five_min_avg_output_1, five_min_avg_func_1,
                         msg='one min average is wrong!, should not be anything yet')
        self.assertEqual(five_min_avg_output_2, five_min_avg_func_2, msg='one min avg is wrong !')

    if __name__ == '__main__':
        unittest.main()