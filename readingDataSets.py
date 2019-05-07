# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 12:51:54 2016

@author: ringoyen
""
"""
def main():

    pass

def reading_data(data_file):
    """
    Read in a data file (16 bit) and obtain the entire data set that is 
    multiplexed between ECG and Pulse data.  The data is then extracted and appended
    to separate arrays
    
    :param data_file: The binary data file to be loaded into the function
    :return data: The ECG data in array
    """

    try:
        import numpy as np
        from scipy.io import loadmat

        m = loadmat(data_file)
        x = dict(m)

        fs = x.get('f_s')
        fs = np.array(fs)
        fs = fs.flatten()

        pp = x.get('pulse_P')
        pp = np.array(pp)
        pp = pp.flatten()

        ecg = x.get('ECG')
        ecg = np.array(ecg)
        ecg = ecg.flatten()

        print(fs)
        return fs, pp, ecg

    except ValueError:
        try:
            import numpy as np
            import h5py

        # for h5py

            with h5py.File(data_file, 'r') as hf:
                fs = hf.get('f_s')
                fs = np.array(fs)
                fs = fs.flatten()

                pp = hf.get('pp')
                pp = np.array(pp)
                pp = pp.flatten()

                ecg = hf.get('ECG')
                ecg = np.array(ecg)
                ecg = ecg.flatten()

                print(fs)

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

            print(ecg)
            return fs, pp, ecg



def ecg_time(ecg_data, f_s):
    """
    Takes in the sampling frequency and the ECG data array found above 
    and determines an array for the ECG Time
    
    :param f_s: is the sampling frequency
    :param ecg_data: is the ECG data array
    :returns: ecg_time_values is the ECG Time array.
    
    """
    
    from numpy import linspace
    
    n_ecg = len(ecg_data)  # total number of points for ecg data array
    ecg_time_total = n_ecg/f_s  # total time elapsed for ecg data array

    ecg_time_values = linspace(0, ecg_time_total, n_ecg)  # time array for ecg values.

    return ecg_time_values



    




    
        
    
        
        
    
    
    

if __name__ == '__main__':
     main()






