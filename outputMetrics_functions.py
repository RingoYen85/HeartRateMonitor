# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 16:20:03 2016

@author: ringoyen
"""


from time import sleep
import matplotlib.pyplot as plt

def main():
    
    pass


def display_metrics(instant_hr, ecg_time, one_min_avg, five_min_avg, bradycardia=60, tachycardia=100):
    
    """ 
    This function should take the Heart Rate Data Array, 1 min average array, 5 min average array, Heart Rate Time Array
    and print out the data to the terminal.  There will also be a condition to send an "alarm" if there
    are bradycardia or tachycardia conditions
    
    :param: HR_Data = heart rate array. oneMinAvg = array of oneMin HR values, averaged.  fiveMinAvg = array of fiveMin HR values.

            HR_time = array of time that heart rate occurs at.



    
    """

    if instant_hr < bradycardia:
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print('Danger: Bradycardia Detected!!')
        sleep(2)

        print("The Signal Time is", ecg_time, "min")
        sleep(2)

        print("The one minute average heart rate is", one_min_avg, "bpm")
        sleep(2)

        print("The five average heart rate is", five_min_avg, "bpm")

        return 0

    elif instant_hr > tachycardia:
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print('Danger: Tachycardia Detected!!')
        sleep(2)

        print("The Signal Time is", ecg_time, "min")
        sleep(2)

        print("The one minute average heart rate is",one_min_avg, "bpm")
        sleep(2)

        print("The five average heart rate is", five_min_avg, "bpm")

        return 0

    else:
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print("The Signal Time is", ecg_time, "min")
        sleep(2)

        print("The one minute average heart rate is", one_min_avg, "bpm")
        sleep(2)

        print("The five minute average heart rate is", five_min_avg, "bpm")

        return 0


def plot_heart_rate(hr_data, time_data):
    x = time_data
    y = hr_data
    plt.plot(x, y)
    plt.xlabel('Time in min')
    plt.ylabel('Heart Rate Trace (bpm)')
    plt.show()

    return 0

if __name__ == '__main__':
     main()


