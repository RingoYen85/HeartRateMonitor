# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 22:31:50 2016

@author: ringoyen
"""


def main():

    """In this main function, there are a set of args parse functions that allow the user to utilize args parse to
    choose arguments when running this script in the command window.  The code begins by reading in the data file and
    creating 3 outputs which represent the sampling frequency, the pulse plethysmograph data and the ecg data.
    The ecg data and the sampling frequency are use to construct a linear time array that corresponds to the ecg
    data.  4 empty numpy arrays are initialized.  One array is for ecg data used to calculate the one min heart rate
    average.  The second array is used to calculate the five min heart rate average data.  The third array is to store
    the instantaneous heart rate data, so that it can be used to plot a trace of the heart rate vs time, after
    the end of the code.  The fourth empty array is used to capture the time in minutes so it can be plotted with the
    heart rate trace.  Once the data is read in, it is incremented into indices (chunks) and then processed.  Each chunk
    taken is about 10 seconds long (sampling frequency times 10 seconds).  The chunk is used to find the instantaenous
    heart rate and then it is stored.  The one min averages and five minute averages are not calculated until the time
    counter reaches 60 seconds and 300 seconds, respectively.  Once the time counters reach those points, the one min
    and five min averages constantly update.  An array holding 1 min and another array holding 5 minutes of ecg data are
    are updated (oldest 10 seconds of data dumped, newest 10 seconds added in) and those arrays are used to calculate
    updating 1 and 5 min heart rate averages.

    """

    args = parse_hr()

    data_file = args.data_file

    bradycardia = args.bradycardia
    tachycardia = args.tachycardia

    interval_sec_one_min = args.interval_sec_one_min
    data_choice = args.data_choice

    try:
        import numpy as np

        fs, pp_data, ecg_data = reading_data("HR_mat_long.mat", " ")

        print(len(ecg_data))

        ecg_time_values = ecg_time(ecg_data, fs)

        # initializing empty arrays for the storage of the ecg data for calculating updated one min averages, five min
        # averages the heart rate trace log

        ecg_data_one_min = np.empty(shape=[0,len(ecg_time_values)], dtype=float)
        ecg_data_five_min = np.empty(shape=[0,len(ecg_time_values)], dtype=float)
        ecg_instant_hr_log = np.empty(shape=[0, len(ecg_time_values)], dtype=float)
        ecg_time_log = np.empty(shape=[0, len(ecg_time_values)], dtype=float)
        time_counter_sec = 0

        chunk_increment = fs * 10
        chunk_increment_cast = np.array(chunk_increment, dtype='uint32')

        i = np.array(0, dtype='uint32')  # This is necessary other wise the for loop will fail
        for i in range(0, len(ecg_data), chunk_increment_cast):
            ecg_data_chunk = ecg_data[i:i+chunk_increment_cast]
            print("The length of the ECG Data Chunk is:", len(ecg_data_chunk))
            time_data_chunk = ecg_time_values[i:i+chunk_increment_cast]

            time_counter_sec += 10
            time_counter_minutes = (time_counter_sec/60)  # for displaying elapsed signal time
            ecg_smooth_chunk = low_pass_filter(ecg_data_chunk)
            ecg_chunk_processed = remove_dc_offset(ecg_smooth_chunk)

            ecg_threshold = find_threshold(ecg_chunk_processed, fs, 5, 0.85)

            print("ECG threshold is:", ecg_threshold)
            instant_hr = find_instantaneous_heart_rate(ecg_chunk_processed, time_data_chunk, ecg_threshold)

            if time_counter_sec <= 60:
                ecg_data_one_min = np.append(ecg_data_one_min, ecg_chunk_processed)

            elif time_counter_sec > 60:
                indices = list(range(0, chunk_increment, 1))  # pick first indices
                ecg_data_one_min = np.delete(ecg_data_one_min, indices)  # remove old data at earliest indices
                ecg_data_one_min = np.append(ecg_data_one_min, ecg_chunk_processed)  # add new data

            if time_counter_sec <= 300:
                ecg_data_five_min = np.append(ecg_data_five_min, ecg_chunk_processed)

            elif time_counter_sec > 300:
                indices = list(range(0, chunk_increment, 1))
                ecg_data_five_min = np.delete(ecg_data_five_min, indices)
                ecg_data_five_min = np.append(ecg_data_five_min, ecg_chunk_processed)

            one_min_avg = one_minute_avg(ecg_data_one_min, ecg_threshold, time_counter_sec, 60)
            five_min_avg = five_minute_avg(ecg_data_five_min, ecg_threshold, time_counter_sec, 300)

            value_1 = display_metrics(instant_hr, time_counter_minutes, one_min_avg, five_min_avg, bradycardia=60, tachycardia=100)

            ecg_instant_hr_log = np.append(ecg_instant_hr_log, instant_hr)
            ecg_time_log = np.append(ecg_time_log, time_counter_minutes)

        value_2 = plot_heart_rate(ecg_instant_hr_log, ecg_time_log)

    except EOFError:
        print("End of File, plot of heart rate trace will be shown!!")
        value_2 = plot_heart_rate(ecg_instant_hr_log, ecg_time_log)


def reading_data(data_file, data_choice):
    """ This function is adapted to take in any 3 files of the following types: .bin, .mat or h5.  The reader is designed
    to read in uint16 cast data.  A try except structure is utilized in order to accommodate the 3 file types.  The entire
    data file is read in with the reader functions chosen.  The .bin reader is designed to read in the uint16 data that is
    multiplexed.  It is assumed that the fs is the first data point, the ECG data comes first and then the PP data
    comes next.

    :param data_file: The uint16 data file to be loaded into the function. It can be a .mat, h5 or .bin.
    :param data_choice: A string input that dictates if the output of the function will yield Fs, ECG and PP data,
                        or just fs and ecg data. If you enter in "ECG" only the fs and ECG data is returned. The default
                        is to allow the data_choice input be " " so all 3 data types are returned.
    :return: The function will return 3 data sets, the sampling frequency in Hz (fs), the pp data and ECG data.

    """

    try:

        import numpy as np
        from scipy.io import loadmat

        m = loadmat(data_file)
        x = dict(m)

        fs = x.get('fs')
        fs = np.array(fs)
        fs = fs.flatten()

        pp = x.get('pp')
        pp = np.array(pp)
        pp = pp.flatten()

        ecg = x.get('ecg')
        ecg = np.array(ecg)
        ecg = ecg.flatten()

        if data_choice == 'ECG':
            return fs, ecg

        else:
            return fs, pp, ecg

    except ValueError:
        try:
            import numpy as np
            import h5py

            # for h5py

            with h5py.File(data_file, 'r') as hf:
                fs = hf.get('fs')
                fs = np.array(fs)
                fs = fs.flatten()

                pp = hf.get('pp')
                pp = np.array(pp)
                pp = pp.flatten()

                ecg = hf.get('ecg')
                ecg = np.array(ecg)
                ecg = ecg.flatten()

            if data_choice == 'ECG':
                return fs, ecg

            else:
                return fs, pp, ecg

        except IOError:
            from numpy import fromfile, empty, append

            fs = fromfile(data_file, dtype='uint16', count=1, sep='')

            hrData = fromfile(data_file, dtype='uint16', count=-1, sep='')

            ecg = empty(shape=[0, len(hrData)], dtype=int)  # Initialize Empty Arrays
            pp = empty(shape=[0, len(hrData)], dtype=int)  # Initialize Empty Arrays

            for i in range(1, len(hrData), 2):
                ecg = append(ecg, hrData[i])

            for k in range(2, len(hrData), 2):
                pp = append(pp, hrData[k])

            if data_choice == 'ECG':  # This is the if statement that allows one to choose if you want to
                                        # ECG data available or both ECG and PP data.
                return fs, ecg

            else:
                return fs, pp, ecg


def ecg_time(ecg_data, f_s):
    """ This function takes in the sampling frequency and the ECG data array found above
    and determines an array for the ECG Time.  There are logging functionalities to allow for debugging.

    :param f_s: This is the sampling frequency in hertz.
    :param ecg_data: This is the array of ecg data that comes from the reader function.
    :return: ecg_time_values, which is an array of time values in seconds that correspond to the ecg data.

    """

    from numpy import linspace
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug('Debug: Just constructed the ECG Time array!!')

    n_ecg = len(ecg_data)  # total number of points for ecg data array

    try:
        ecg_time_total = n_ecg / f_s  # total time elapsed for ecg data array
    except TypeError:
        print("Error: Sampling Frequency is not a number")

    ecg_time_values = linspace(0, ecg_time_total, n_ecg)  # time array for ecg values.

    return ecg_time_values


def low_pass_filter(ecg_data, window_size=5):
    """ This function takes an an array of ecg data and applies a convolution with a rect of ones (5 length). After the
    convolution, the array of ecg data is then divided by the kernel length.  This process is essentially a low pass
    filter, removing high frequency noise in the signal.

    :param ecg_data: This is the array of ecg_data that is being smoothed.
    :param window_size:  The window size is by default 5, and it dictates the size of the kernel.
    :return: ecg_smooth, which is an array of ecg_data which should have noise smoothed out and reduced.

    """
    import numpy as np

    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')

    kernel = np.ones(window_size)
    ecg_data = ecg_data.flatten()
    ecg_values = np.convolve(ecg_data, kernel, 'same')

    logging.debug("Debug: Convolved the ECG signal with the kernel")
    ecg_smooth = np.divide(ecg_values, len(kernel))
    logging.debug("Debug: Divided the convolved signal with the kernel")

    return ecg_smooth


def remove_dc_offset(ecg_smooth):
    """ This function will remove DC offsets that may be present in the data set.  This is accomplished by
    subtracting the mean from the data.

    :param ecg_smooth: The input is the ecg data array, that is smoothed and low pass filtered.
    :return: ecg_data, which is an array of ecg data which has any possible dc offset removed.

    """

    import numpy as np
    import logging

    ecgtotal = np.sum(ecg_smooth)
    ecgsize = len(ecg_smooth)

    try:
        ecgmean = ecgtotal / ecgsize

    except ZeroDivisionError:
        print('ECG mean is invalid, size of ecg should not be zero!')

    ecg_data = ecg_smooth - ecgmean

    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug('Debug: Just calculated and removed the DC offset from signal!')

    return ecg_data


def find_threshold(ecg_data, f_s, factor=5, threshold_multiply=0.85):
    """ This function takes in about 5 seconds worth of ecg samples (assuming the ecg_data array entered is at least 5
    seconds long) and uses that 5 second array to set a threshold for the peak detect algorithm
    used in the code to determine heart rates.  This is done by taking the max of the 5 seconds worth of data and then
    multiplying that max by 0.85.

    :param ecg_data: The array of ecg data that is entered. It should be at least 5 seconds long.
    :param f_s: The sampling frequency
    :param factor: This is default 5, to represent 5 seconds of ecg data.
    :param threshold_multiply: This is set to 0.85 default.
    :return: ecgThreshold - the threshold ECG Value that dictates a peak in the heart rate signal.

    """
    import logging
    # Finding maximum ECG Value
    ecg_window = max(ecg_data[:f_s * factor])

    # Finding ECG Threshold
    ecg_threshold = threshold_multiply * ecg_window

    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug('debug: The ECG Threshold has just been found')

    return ecg_threshold


def find_instantaneous_heart_rate(ecgData, ecgTime, ecgThreshold):
    """ This function determines the number of number of ECG Waveforms, by locating the peaks of each waveform
    and recording the time of these peaks.  The peaks are located by using the threshold value set, and the condition
    that the peak value should be larger then the value before and after it.  Once this is done, the time of these peaks
    is used to find the instantaneous heart rate.  This is done by taking the difference in time in between 2 peaks
    and inverting this difference. This is then multiplied by 60.  There should be multiple heart rates in the array,
    the values are averaged to get 1 value for the instantaneous heart rate.

    :param ecgData: The ECG Array that is fed into the function.  This should be smoothed with offsets removed.
    :param ecgTime: This is the time array that corresponds to the ECG array.
    :param ecgThreshold: This is the ECG threshold used to find peaks.
    :returns: instant_hr_actual  - the instantaneous heart rate returned by the function.

    """

    import numpy as np
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Info: The instantaneous heart rate average is being calculated')

    counts = np.empty(shape=[0, len(ecgData)], dtype=np.float64)  # Initialize Empty Array of ECG waveform counts.
    beat_time = np.empty(shape=[0, len(ecgData)], dtype=np.float64)  # Initialize Empty Array of times when ECG
    # waveform counts are recorded.

    # The for loop determines the peak and appends the peak ECG Value and the time to arrays.
    for k in range(0, len(ecgData)):
        if ecgData[k] > ecgThreshold and ecgData[k] > ecgData[k - 1] and ecgData[k] > ecgData[k + 1]:
            counts = np.append(counts, ecgData[k])
            beat_time = np.append(beat_time, ecgTime[k])
        elif ecgData[k] > ecgThreshold and ecgData[k] == ecgData[k - 1] and ecgData[k] > ecgData[k + 1]:
            counts = np.append(counts, ecgData[k])
            beat_time = np.append(beat_time, ecgTime[k])

    instant_hr = np.zeros(len(beat_time) - 1)

    for i in range(0, len(beat_time) - 1):
        instant_hr[i] = (1 / (beat_time[i + 1] - beat_time[i])) * 60  # in bpm

    try:
        instant_hr_actual = np.sum(instant_hr) / len(instant_hr)

    except ZeroDivisionError:
        print('Instantaneous Heart Rate is invalid due to division by zero error')

    return instant_hr_actual


def one_minute_avg(ecg_data, threshold, time_counter, interval_sec_one_min= 60):
    """ This function takes in the array of ecg data, a threshold, a time counter value and a 60 second value
    to find the 1 min heart rate average.  The same peak detect algorithm used in the previous function is used.
    The total number of counts (peaks) is divided by 60 and multiplied by 60 to get bpm for a min.  The time counter
    is needed to activate the function.  For time under 60 seconds, the function will not calculate averages (bc there
    is not 1 minutes worth of data yet!). With time counter values over 60 seconds, the function will find the 1 min
    averages.

    :param ecg_data: Array of ECG data to be processed
    :param threshold: Threshold used to find peaks
    :param time_counter: A metric to determine when to start finding 1 min heart rate averages.
    :param interval_sec_one_min: 60 seconds, because there are 60 seconds in a min.
    :return: one_min_avg - a one min average heart rate.

    """

    import numpy as np
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Info: The one minute heart rate average is being calculated')

    if time_counter >= 60:

        hr_counts = np.zeros(1, dtype=float)
        for j in range(0, len(ecg_data)):
            if ecg_data[j] >= threshold and ecg_data[j] > ecg_data[j - 1] and ecg_data[j] > ecg_data[j + 1]:
                hr_counts[0] += 1.0
            elif ecg_data[j] >= threshold and ecg_data[j] == ecg_data[j - 1] and ecg_data[j] > ecg_data[j + 1]:
                hr_counts[0] += 1.0
        one_min_avg = (hr_counts / interval_sec_one_min) * 60  # in bpm

        return one_min_avg

    else:
        return 0.0


def five_minute_avg(ecg_data, threshold, time_counter, interval_sec_five_min=300):
    """ This function is essentially the same as the above function, except the time counter has an activating value
    of 300, not 60, because there's 300 seconds in 5 minutes.

    :param ecg_data: Array of ECG data
    :param threshold: Threshold to find peaks
    :param time_counter: Time counter to activate the function
    :param interval_sec_five_min: 300 seconds
    :return: five_min_avg - a five minute heart rate average.

    """
    import numpy as np
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Info: The five minute heart rate average is being calculated')

    if time_counter >= 300:

        hr_counts = np.zeros(1, dtype=float)

        for r in range(0, len(ecg_data)):
            if ecg_data[r] >= threshold and ecg_data[r] > ecg_data[r - 1] and ecg_data[r] > ecg_data[r + 1]:
                hr_counts += 1.0
            elif ecg_data[r] >= threshold and ecg_data[r] == ecg_data[r - 1] and ecg_data[r] > ecg_data[r + 1]:
                hr_counts += 1.0

        five_min_avg = (hr_counts / interval_sec_five_min) * 60  # in bpm

        return five_min_avg

    else:
        return 0.0


def display_metrics(instant_hr, ecg_time_num, one_min_avg, five_min_avg, bradycardia = 60, tachycardia=100):
    """ This function should take the instantaneous heart rate, the ecg time, the one min and five min heart rate
    average and displays them to the terminal.  If the instantaneous heart rate is less than 60 or over 100 - then
    bradycardia/tachycardia conditions will be alarmed.

    :param instant_hr: Instantaneous heart rate found
    :param ecg_time_num: ecg time (signal time)
    :param one_min_avg: 1 min heart rate average
    :param five_min_avg: 5 min heart rate average
    :param bradycardia: Threshold for bradycardia. Default is 60 bpm.
    :param tachycardia: Threhold for tachycardia. Default is 100 bpm.
    :return: 0 - the function just prints to the terminal so 0 is returned to indicate the end of the function.

    """
    from time import sleep
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')

    if instant_hr < bradycardia:
        logging.warning("Warning: Bradycardia is happening here!")
        sleep(2)
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print('Danger: Bradycardia Detected!!')
        sleep(2)

        print("The Signal Time is", ecg_time_num, "min")
        sleep(2)

        print("The one minute average heart rate is", one_min_avg, "bpm")
        sleep(2)

        print("The five average heart rate is", five_min_avg, "bpm")
        sleep(2)

        return 0

    elif instant_hr > tachycardia:
        logging.warning("Warning: Tachycardia is happening here!")
        sleep(2)
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print('Danger: Tachycardia Detected!!')
        sleep(2)

        print("The Signal Time is", ecg_time_num, "min")
        sleep(2)

        print("The one minute average heart rate is", one_min_avg, "bpm")
        sleep(2)

        print("The five average heart rate is", five_min_avg, "bpm")
        sleep(2)

        return 0

    else:
        sleep(2)
        print("The Instantaneous Heart Rate is", instant_hr, "bpm")
        sleep(1)

        print("The Signal Time is", ecg_time_num, "min")
        sleep(2)

        print("The one minute average heart rate is", one_min_avg, "bpm")
        sleep(2)

        print("The five minute average heart rate is", five_min_avg, "bpm")
        sleep(2)

        return 0


def plot_heart_rate(hr_data, time_data):
    """ This function just takes in an array of heart rate data and plots it versus an array of time data that corresponds
    to the heart rate data.

    :param hr_data: Array of heart rate data to be traced/plotted.
    :param time_data: Time that the heart rate is found at.
    :return: zero. Just plotting.
    """


    import matplotlib.pyplot as plt
    import logging
    logging.basicConfig(filename='log.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info('Info:The Heart Rate Trace is being plotted now')

    x = time_data
    y = hr_data
    plt.plot(x, y)
    plt.xlabel('Time in min')
    plt.ylabel('Heart Rate Trace (bpm)')
    plt.title('Continuous trace log of Heart Rate')
    plt.show()

    return 0


def parse_hr():
    """This function allows the user to run the script in the command window and specify arguments.  The arguments are for
    the data file to be run, one argument to allow for either ecg data or both ecg data and pp data, one argument to
    specify bradycardia, another to specify tachycardia, and finally one to specify the duration of the multi min
    averages.

    :return: args - This is the output for the argparser function.

    """

    import argparse as ap

    par = ap.ArgumentParser(description="Arguments to be passed into the Total Functions.py",
                            formatter_class=ap.ArgumentDefaultsHelpFormatter)

    par.add_argument("--file_name", dest="data_file", help="file that is to be input for reading", type=str,
                     default="ECG_first_long.bin")

    par.add_argument("--input for just ECG or both ECG & PP", dest="data_choice",
                     help="Input string ECG if you just want ECG values, otherwise enter " "", type=str,
                     default=" ")

    par.add_argument("--Bradycardia_Threshold", dest='bradycardia', help='Integer value for Bradycardia Threshold',
                     type=int, default=60)

    par.add_argument("--Tachycardia Threshold", dest='tachycardia', help='Integer value for Tachycardia Threshold',
                     type=int, default=100)

    par.add_argument("--duration of multi min heart rate averages", dest='interval_sec_one_min',
                     help='Specify duration of the multi minute heart rate estimates', type=int, default=60)

    args = par.parse_args()

    return args


if __name__ == '__main__':
     main()



    
    
    
    
    
    
    









    
        
    
    
        
        
    
    
        
    
    
            
    
    


    







    