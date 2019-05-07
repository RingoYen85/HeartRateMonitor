# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 15:35:23 2016

@author: ringoyen
"""


def main():
    
    """ 
    These functions will be used for a threshold algorithm to determine the number
        of heart beats per unit time, an estimate of the heart rate
        
    """



def low_pass_filter(ecg_data, window_size = 5):

    import numpy as np
    kernel = np.ones(window_size)

    ecg_data = ecg_data.flatten()
    ecg_values = np.convolve(ecg_data, kernel, 'same')
    ecg_smooth = np.divide(ecg_values, len(kernel))

    return ecg_smooth


def remove_dc_offset(ecg_smooth):
    """

    This function will remove DC offsets that may be present in the data set.
    This is accomplished by subtracting the mean from the data

    :param:



    :return:

    """

    import numpy as np

    ecgtotal = np.sum(ecg_smooth)
    ecgsize = len(ecg_smooth)

    ecgmean = ecgtotal/ecgsize
    ecg_data = ecg_smooth - ecgmean

    return ecg_data


def findThreshold(ecg_data, f_s, factor=5, threshold_multiply=0.85):
    """ 
    This function takes in the ECG data that is determined in readBinary
    and then takes in a window of the data and then finds the max value
    
    :param: ecgData - the ECG array determined in the previous function. num_val - 
            a default value of samples to take in, and have the maximum value determined
            thresholdMult - a constant to multiply to the maximum to set a threshold value.
            
    :returns:ecgThreshold - the threshold ECG Value that dictates a peak in the heart rate signal
    
    """
    # Finding maximum ECG Value
    ecg_window = max(ecg_data[:f_s*factor])
    
    # Finding ECG Threshold
    ecg_threshold = threshold_multiply*ecg_window
     
    return ecg_threshold

     
def find_instantaneous_heart_rate(ecgData,ecgTime,ecgThreshold):
    """
    This function determines the number of number of ECG Waveforms, by locating the peaks of each waveform
    and recording the time of these peaks.  The peaks are located by using the threshold value set, and the condition 
    that the peak value should be larger then the value before and after it.
    
    :param: ecgData - the ECG Array determined. ecgTime - the ECG Time Array determined. ecgThreshold - the threshold
            ecg value determined.
            
    :returns: beattime  - the time values that occur at each peak of the ECG Waveforms.
    
    
    """
    import numpy as np
    
    counts = np.empty(shape=[0, len(ecgData)], dtype=int)  # Initialize Empty Array of ECG waveform counts.
    beat_time = np.empty(shape=[0, len(ecgData)], dtype=float)  # Initialize Empty Array of times when ECG
    # waveform counts are recorded.

    # The for loop determines the peak and appends the peak ECG Value and the time to arrays.
    for k in range(0,len(ecgData)):
        if ecgData[k] >= ecgThreshold and ecgData[k] > ecgData[k-1] and ecgData[k] > ecgData[k+1]:
            counts = np.append(counts, ecgData[k])
            beat_time = np.append(beat_time, ecgTime[k])
        elif ecgData[k] >= ecgThreshold and ecgData[k] == ecgData[k-1] and ecgData[k] > ecgData[k+1]:
            counts = np.append(counts, ecgData[k])
            beat_time = np.append(beat_time, ecgTime[k])

    instant_hr = np.zeros(len(beat_time) - 1)
    for i in range(0,len(beat_time) - 1):
        instant_hr[i] = (1 / (beat_time[i+1] - beat_time[i])) * 60  # in bpm

    instant_hr_actual = np.sum(instant_hr)/len(instant_hr)

    return instant_hr_actual







if __name__ == '__main__':
     main()

