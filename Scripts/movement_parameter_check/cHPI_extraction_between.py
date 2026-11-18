# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:27:54 2024

@author: Jan Schalla
"""

import os
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
import mne
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns
from mne.preprocessing import find_bad_channels_maxwell

center_function = lambda x: x - x[0]

# %% Prepare environment

# Get all subjects from the SFB project
data_path = '/home/jan/Jan/00_Retune/01_WP1/data/RSSFB010*'

ID_dirs = glob.glob(data_path)

crosstalk_file = '/home/jan/Jan/meg_related/tSSS_config/ct_sparse.fif'
calibration_file = '/home/jan/Jan/meg_related/tSSS_config/sss_cal.dat'

coil_position_between_raw = []
# %% run subject loop
for ID in ID_dirs:
    print(f'\n#####################\nWorking on {ID}\n')

    ID_files = glob.glob(os.path.join(ID, 'meg/RSSFB*'))
    
    ID_files = [f for f in ID_files if not re.search(r'-\d+\.fif$', os.path.basename(f))]
    ID_files = [f for f in ID_files if "cHPI" not in f]

    
    for file in ID_files:
        metadata = mne.io.read_info(file, verbose = False)
            
        filename = os.path.split(file)[1]    
        filename = os.path.splitext(filename)[0]
        filename_part = filename.split('_')
        ID = filename_part[0]
        medIdx = next(i for i, item in enumerate(filename_part) if item.startswith('med'))
        stimIdx = next(i for i, item in enumerate(filename_part) if item.startswith('stim'))
        medState = 'On' if filename_part[medIdx] == 'medOn' or filename_part[medIdx]=='medON' else 'Off' if filename_part[medIdx] == 'medOFF' or filename_part[medIdx] == 'medOff' else None
        stimState = 'On' if filename_part[stimIdx] == 'stimOn' or filename_part[stimIdx]=='stimON' else 'Off' if filename_part[stimIdx] == 'stimOFF' or filename_part[stimIdx] == 'stimOff' else None
        run = filename_part[-1]
        
        if run.startswith('run'):
            run = int(run[3:])
            
        
        fit_accepted = metadata['hpi_results'][0]['accept']
        
        # if fit_accepted != 1:
        #     print(f'\nHPI fit of file {file} not accepted.\nSkipping file completely!\n')
        #     tmp_sub_data = [ID, medState, stimState, run, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, file, fit_accepted]
        #     coil_position_between_raw.append(tmp_sub_data)
        #     continue
        
        coil_order = metadata['hpi_results'][0]['order']
        
        for coil in coil_order:
                
            gof = metadata['hpi_results'][0]['goodness'][coil-1]
            x, y, z = np.split(metadata['hpi_results'][0]['dig_points'][coil-1]['r'], 3, axis = 0)
            dig_hpi_x, dig_hpi_y, dig_hpi_z = np.split(metadata['dig'][coil + 2]['r'], 3, axis = 0)
                
            # if  coil not in metadata['hpi_results'][0]['used'] or gof < 0.98:
            #     print(f'\nCoil {coil} ommited!\nGOF is {gof}.')
            #     tmp_sub_data = [ID, medState, stimState, run, gof, np.nan, np.nan, np.nan, coil, dig_hpi_x[0]*1000, dig_hpi_y[0]*1000, dig_hpi_z[0]*1000, file, fit_accepted]
            # else:
            tmp_sub_data = [ID, medState, stimState, run, gof, x[0] * 1000, y[0] *1000, z[0] * 1000, coil, dig_hpi_x[0]*1000, dig_hpi_y[0]*1000, dig_hpi_z[0]*1000, file, fit_accepted]
                
            coil_position_between_raw.append(tmp_sub_data)
                
# %% Descriptives of movement data 
coil_position_between_raw = np.vstack(coil_position_between_raw)

df_coil_position_between_raw = pd.DataFrame(coil_position_between_raw)

df_coil_position_between_raw = df_coil_position_between_raw.rename(columns = {0: 'sub_id', 1:'medState', 2: 'stimState', 3: 'run',
                                                                4: 'gof', 5: 'x', 6: 'y', 7: 'z', 8: 'coil_nr',
                                                                9: 'dig_hpi_x', 10: 'dig_hpi_y', 11: 'dig_hpi_z', 12: 'file', 13: 'accepted_fit'})

# Transform relevant data to numeric
df_coil_position_between_raw['run'] = pd.to_numeric(df_coil_position_between_raw['run'], errors='coerce')
df_coil_position_between_raw['gof'] = pd.to_numeric(df_coil_position_between_raw['gof'], errors='coerce')
df_coil_position_between_raw['x'] = pd.to_numeric(df_coil_position_between_raw['x'], errors='coerce')
df_coil_position_between_raw['y'] = pd.to_numeric(df_coil_position_between_raw['y'], errors='coerce')
df_coil_position_between_raw['z'] = pd.to_numeric(df_coil_position_between_raw['z'], errors='coerce')
df_coil_position_between_raw['coil_nr'] = pd.to_numeric(df_coil_position_between_raw['coil_nr'], errors='coerce')
df_coil_position_between_raw['dig_hpi_x'] = pd.to_numeric(df_coil_position_between_raw['dig_hpi_x'], errors='coerce')
df_coil_position_between_raw['dig_hpi_y'] = pd.to_numeric(df_coil_position_between_raw['dig_hpi_y'], errors='coerce')
df_coil_position_between_raw['dig_hpi_z'] = pd.to_numeric(df_coil_position_between_raw['dig_hpi_z'], errors='coerce')

df_coil_position_between_raw.to_csv('/home/jan/Jan/002_script_outputs/head_cast_movement_verification/HPI_coil_position_between.csv', index = False)
