# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 16:20:03 2016

@author: ringoyen
"""


from time import sleep
import matplotlib.pyplot as plt

def main():
    
    """ 
    This function should take the Heart Rate Data Array, 1 min average array, 5 min average array
    and print out the data to the terminal.  There will also be a condition to send an "alarm" if there
    are bradycardia or tachycardia conditions
    
    This file serves as a TEST FIle to ensure that the function prints out the proper values when they are input 
    as arguments to the function.
        
    """
    import numpy as np
    # test input values
    instant_hr = 2
    time = 3
    oneMinAvg = 1
    fiveMinAvg = 1.68
    plot_hr = np.array([1.0, 4.0])
    print(len(plot_hr))

    HR_Time = np.array([1.0, 2.0])
    print(len(HR_Time))


    a = display_metrics(instant_hr, time, oneMinAvg, fiveMinAvg, 60, 60)
    b = plotter(plot_hr, HR_Time)



def display_metrics(instant_hr, ecg_time, one_min_avg, five_min_avg, bradycardia=60, tachycardia=100):

        """
        This function should take the Heart Rate Data Array, 1 min average array, 5 min average array, Heart Rate Time Array
        and print out the data to the terminal.  There will also be a condition to send an "alarm" if there
        are bradycardia or tachycardia conditions

        :param: HR_Data = heart rate array. oneMinAvg = array of oneMin HR values, averaged.  fiveMinAvg = array of fiveMin HR values.
                HR_time = array of time that heart rate occurs at.

        """

        if instant_hr < bradycardia:
            print(instant_hr, "bpm")
            sleep(1)

            print('Danger: Bradycardia Detected!!')
            sleep(2)

            print(ecg_time, "min")
            sleep(2)

            print(one_min_avg, "bpm")
            sleep(2)

            print(five_min_avg, "bpm")

            return 0



        elif instant_hr > tachycardia:
            print(instant_hr)
            sleep(1)

            print('Danger: Tachycardia Detected!!')
            sleep(2)

            print(ecg_time, "min")
            sleep(2)

            print(one_min_avg, "bpm")
            sleep(2)

            print(five_min_avg, "bpm")

            return 0



        else:
            print(instant_hr)
            sleep(1)

            print(ecg_time, "min")
            sleep(2)

            print(one_min_avg, "bpm")
            sleep(2)

            print(five_min_avg, "bpm")

            return 0


def plotter(plot_hr, plot_time):

    plt.plot(plot_hr, plot_time)
    plt.xlabel('Time in min')
    plt.ylabel('Heart Rate Trace (bpm)')
    plt.show()
    return 0


if __name__ == '__main__':
     main()


