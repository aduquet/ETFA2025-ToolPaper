from scipy.signal import find_peaks
from signal_metrics import SignalMetrics
from pathlib import Path
import warnings
import numpy as np
import os
import pandas as pd
import glob as gl


def getting_metrics(df):
    df_aux = []

    for index, row in df.iterrows():

        time = np.array(row['time'])
        pressureR =  np.array(row['pressureR'])
        pressureT =  np.array(row['pressureT'])
        speedR =  np.array(row['speedR'])
        speedT =  np.array(row['speedT'])

        pressure_peaks, _ = find_peaks(pressureR, height=0)
        pressure_amplitudes = pressureR[pressure_peaks]

        pressure_max_peak_idx_T = np.argmax(pressureT)
        pressure_target_value = pressureT[pressure_max_peak_idx_T]

        # Find the max peak pressure
        pressure_max_peak_idx = np.argmax(pressure_amplitudes)
        pressure_max_peak_time = time[pressure_peaks[pressure_max_peak_idx]]
        pressure_max_peak_value = pressure_amplitudes[pressure_max_peak_idx]

        pressureT_max_peak_value = pressureT[pressure_max_peak_idx]
        currentPressure_ratio = round(float(pressure_max_peak_value/pressure_target_value),3)
        pressure_metrics = SignalMetrics(signal=pressureR, time=time, max_peak_time=pressure_max_peak_time)
        
        num_oscillations_before_peak = pressure_metrics.oscillation_frequency()
        avg_oscillation_amplitude = pressure_metrics.average_oscillation_amplitude()

        pressure_metrics = SignalMetrics(signal=pressureR, time=time, max_peak_time=pressure_max_peak_time)
        
        num_oscillations_before_peak = pressure_metrics.oscillation_frequency()
        avg_oscillation_amplitude = pressure_metrics.average_oscillation_amplitude()

        # Calculate the first derivative (rate of change) to detect perturbations
        pressure_derivative = np.gradient(pressureR, time)
        # Define threshold for detecting significant perturbations
        threshold = np.percentile(pressureR, 95)  # Using 95th percentile as threshold

        # Identify perturbations based on the threshold
        perturbations_new = np.where(pressureR > threshold, pressure_derivative, 0)

        pressure_energy = pressure_metrics.total_energy(pressure_derivative)
        pressure_energy_before_peak = pressure_metrics.energy_before_peak(pressure_derivative)
        pressure_energy_after_peak = pressure_metrics.energy_after_peak(pressure_derivative)
 
        '''SPEED'''

        # Find peaks in the speed data
        speed_peaks, _ = find_peaks(speedT, height=0)
        speed_amplitudes = speedT[speed_peaks]  # Get the amplitudes at the peaks

        # Find the max peak speed
        # speed_max_peak_idx = np.argmax(speed_amplitudes)
        # speed_max_peak_time = time[speed_peaks[speed_max_peak_idx]]
        # speed_max_peak_value = speed_amplitudes[speed_max_peak_idx]

        speed_metrics = SignalMetrics(signal=speedR, time=time, max_peak_time=pressure_max_peak_time)

        speed_num_oscillations_before_peak = speed_metrics.oscillation_frequency()
        speed_avg_oscillation_amplitude = speed_metrics.average_oscillation_amplitude()

        # Growing factor, R², and fitted values
        # try:
        #     speed_k, speed_r_squared, speed_fitted_values = speed_metrics.growing_factor() # type: ignore
        # except:
        #     speed_k = None
        #     speed_r_squared = None
        #     speed_fitted_values = None

        # Calculate the first derivative (rate of change) to detect perturbations
        speed_derivative = np.gradient(speedR, time)
        # Define threshold for detecting significant perturbations
        speed_threshold = np.percentile(speedR, 95)  # Using 95th percentile as threshold
        # print('============================================')

        # Identify perturbations based on the threshold
        speed_perturbations_new = np.where(speedR > speed_threshold, speed_derivative, 0)

        speed_energy = speed_metrics.total_energy(speed_derivative)
        speed_energy_before_peak = speed_metrics.energy_before_peak(speed_derivative)
        speed_energy_after_peak = speed_metrics.energy_after_peak(speed_derivative)
        
        # pressure_tt, tt_flag = transient_time(time=time, signal=pressureR, signalT=pressureT)
        # Prepare the dataframe with all metrics

        final_score = currentPressure_ratio

        gr_p = pressure_metrics.growing_rate()
        rising_time, rise_index, overshoot_detected = pressure_metrics.get_rising_time(pressureT)
        gr_s = abs(speed_metrics.growing_rate_speed(rise_index))
        gr_prt = pressure_metrics.get_gr_before_rising_time(rise_index=rise_index)
        Eng_p_s = speed_energy/pressure_energy

        df1 = {
            'test_id': row['test_id'],
            'tc': row['tc'],
            'test #': row['id'],
            'Kr': row['Kr'],
            'Tn': row['Tn'],
            'Tv': row['Tv'],
            'PR':currentPressure_ratio,
            'RT': rising_time,
            'P-Eng': pressure_energy,
            'S-Eng': speed_energy,
            'Eng_p-s':  Eng_p_s,
            'gr_p': gr_p,
            'gr_prt':gr_prt,
            'gr_s': gr_s,
            'gr_ratio':gr_prt/gr_s ,
            'speed': speedR,
            'time': time,
            'nobp': num_oscillations_before_peak,
            'nobp_s':speed_num_oscillations_before_peak,
            'avo': speed_avg_oscillation_amplitude,
            'avg_oscillation_amplitude': avg_oscillation_amplitude,
            'speed_energy_before_peak': speed_energy_before_peak,
            'speed_energy_after_peak': speed_energy_after_peak,
            'pressure_max_peak_time': round(float(pressure_max_peak_time),3),
            'pressure_max_peak_value': round(float(pressure_max_peak_value),3),
            'pressure': pressureR,
            'pressureT': pressureT,
            'speedT': speedT,
            'pressure_max_peak_idx': pressure_max_peak_idx,
            # 'speed_peaks': speed_peaks
        }

        df_aux.append(df1)

    df = pd.DataFrame(df_aux)
    return df
