# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 12:51:13 2016

@author: ringoyen
"""






def main():
    
    pass


def one_minute_avg(ecg_data, threshold, time_counter, interval_sec = 60):


    """
    :param: ecgTime - the times in which the heartbeats occur. HR, which is the array of heart rate data. interval sec: default set to 60 seconds
    because we want 1 min averages.
    :returns: one_min_avg - the array of one min averaged heart rate values.
    
    """

    import numpy as np

    if time_counter >= 60:


        hr_counts = np.zeros(1, dtype=float)
        for j in range(0,len(ecg_data)):
            if ecg_data[j] >= threshold and ecg_data[j] > ecg_data[j-1] and ecg_data[j] > ecg_data[j+1]:
                hr_counts[0] += 1.0
            elif ecg_data[j] >= threshold and ecg_data[j] == ecg_data[j-1] and ecg_data[j] > ecg_data[j+1]:
                hr_counts[0] += 1.0
        one_min_avg = (hr_counts/interval_sec) * 60  # in bpm

        return one_min_avg
    
    else:
        return 0.0


def five_minute_avg(ecg_data, threshold, time_counter, interval_sec = 300):
    
    """


    
    """
    import numpy as np

    if time_counter >= 300:

        hr_counts = np.zeros(1, dtype=float)

        for r in range(0, len(ecg_data)):
            if ecg_data[r] >= threshold and ecg_data[r] > ecg_data[r - 1] and ecg_data[r] > ecg_data[r + 1]:
                hr_counts += 1.0
            elif ecg_data[r] >= threshold and ecg_data[r] == ecg_data[r-1] and ecg_data[r]>ecg_data[r+1]:
                hr_counts += 1.0

        five_min_avg = (hr_counts / interval_sec) * 60  # in bpm

        return five_min_avg

    else:
        return 0.0
    

    
    
    
    
    
    
    







if __name__ == '__main__':
     main()

