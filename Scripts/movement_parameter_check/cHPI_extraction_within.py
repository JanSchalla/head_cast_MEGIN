# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:27:54 2024

@author: Jan Schalla
"""

import os, sys
from datetime import datetime
import glob
import matplotlib.pyplot as plt
import numpy as np
import mne
import pandas as pd
import seaborn as sns
from mne.preprocessing import find_bad_channels_maxwell
import json
sys.path.append('/home/jan/Jan/001_scripts/head_cast_movement_verification/')
import extract
# %% Prepare environment 
extracted_data_dir = '/home/jan/Jan/002_script_outputs/head_cast_movement_verification/data/'
t_window = 1

# Get all subjects from the SFB project
data_path = '/home/jan/Jan/00_Retune/01_WP1/data/RSSFB*'
out_dir = os.path.join("/home/jan/Jan/002_script_outputs/head_cast_movement_verification/data/", datetime.now().strftime('%Y-%m-%d'))

try: 
    os.makedirs(out_dir)
except FileExistsError as e:
        print("Directory exists already.\nNo new directory is created, files will be overwritten!")

ID_List = glob.glob(data_path)

crosstalk_file, calibration_file, df_mvmt_desc, df_coil1, df_coil2, df_coil3, df_coil4, df_movement_descriptives, df_head_mvmt_raw, df_metadata_info = extract.set_up_data_environment(extracted_data_dir, t_window)

head_mvmt_raw = []
coil1_pos_data = []
coil2_pos_data = []
coil3_pos_data = []
coil4_pos_data = []
coil_position_desc = []
metadata_info = []
movement_descriptives = []
# %% Define time resolution of cHPI localisation!
t_step_max = t_window
tmin = 5
# %% run subject loop
processed_IDs = 0
for ID in ID_List:
    
    ID_file = glob.glob(os.path.join(ID, 'meg/*cHPI*'))
    
    
    
    id_ident = ID.split('/')[7]
    
    print(f'\n#####################\nNow working on {id_ident}\n#####################\n')
    
    if len(ID_file) == 0:
        print(f'{ID} is skipped, due to no cHPI files!')
        continue
    
    if id_ident in df_mvmt_desc.values:
        
        print(f'{ID} already present. Skipping computation')
        
    else:
        
        processed_IDs += 1
        if id_ident == 'RSSFB011PD' or id_ident == 'RSSFB012PD':
            filepath = ID_file[1]
        else:
            filepath = ID_file[0]
            
        raw = mne.io.read_raw_fif(filepath, allow_maxshield = "yes", verbose=False).load_data(verbose=False)
        raw.crop(tmin = tmin, tmax = 180)
        
        # extract metadata from raw .fif file
        metadata_info_sub = extract.extract_metadata(filepath, id_ident)
        
        print('Running automatic bad segment detection.\n')
        raw.info["bads"] = []
        raw_check = raw.copy()
        auto_noisy_chs, auto_flat_chs, auto_scores = find_bad_channels_maxwell(
            raw_check,
            cross_talk=crosstalk_file,
            calibration=calibration_file,
            return_scores=True,
            verbose=False
            )

        bads = raw.info["bads"] + auto_noisy_chs + auto_flat_chs
        raw.info["bads"] = bads
        
        # calculate head position estimation, separately for each coil
        head_pos_centered, coil_dict = extract.extract_cHPI_elekta(raw, t_window, t_step_max, id_ident)
        
        # Here the calculation of descriptive happens under the hood!
        coil_dict_centered, movement_desc_sub, ID_coil_desc = extract.get_cHPI_descriptive(coil_dict, id_ident, filepath, metadata_info_sub)
        ID_coil_desc, head_pos_centered, movement_desc_sub = extract.process_head_center(head_pos_centered, ID_coil_desc, movement_desc_sub, id_ident, filepath)
        
        # ID_coil_desc = np.vstack(ID_coil_desc)
        coil1_pos_data.append(coil_dict_centered['coil1'])
        coil2_pos_data.append(coil_dict_centered['coil2'])
        coil3_pos_data.append(coil_dict_centered['coil3'])
        coil4_pos_data.append(coil_dict_centered['coil4'])        
        
        # join subject estimates
        metadata_info.append(metadata_info_sub)
        coil_position_desc.append(ID_coil_desc)
        head_mvmt_raw.append(head_pos_centered)
        movement_descriptives.append(movement_desc_sub)
        
        #del head_pos_centered, metadata_info_sub, ID_coil_desc, chpi_amplitudes, chpi_locs, raw, raw_check, coil_dict, auto_flat_chs, auto_noisy_chs, auto_scores
        
        print(f'Finished processing {id_ident}.\n')
        
if processed_IDs != 0:
    # %% metadata 
    metadata_info = np.vstack(metadata_info)
    
    if not df_metadata_info.empty:
        metadata_info = np.vstack([df_metadata_info, metadata_info])

    df_metadata_info = pd.DataFrame(metadata_info)
    df_metadata_info = df_metadata_info.rename(columns={0: 'sub_id', 1: 'coil_nr', 2: 'coil_freq', 3: 'gof', 4: 'used', 5: 'accepted_fit'})

    df_metadata_info = extract.convert_to_numeric(df_metadata_info)
    
    df_metadata_info.to_csv(os.path.join(extracted_data_dir, f'metadata_coils_within_{t_window}s.csv'), index = False)
    # %% head center movement data
    head_mvmt_raw = np.vstack(head_mvmt_raw)  

    if not df_head_mvmt_raw.empty:
        head_mvmt_raw = np.vstack([df_head_mvmt_raw, head_mvmt_raw])

    df_head_mvmt_raw = pd.DataFrame(head_mvmt_raw)
    df_head_mvmt_raw = df_head_mvmt_raw.rename(columns={0: 'time', 1: 'q1', 2: 'q2', 3: 'q3', 4: 'x', 5: 'y', 6: 'z', 7: 'gof', 8: 'err', 9: 'v', 10: 'sub_id', 11: 'displacement', 12: 'cummulative_path_length', 13: 'velocity'})

    df_head_mvmt_raw = extract.convert_to_numeric(df_head_mvmt_raw)

    df_head_mvmt_raw.to_csv(os.path.join(extracted_data_dir, f'head_mvmt_raw_{t_window}s.csv'), index = False)
    # %% Descriptives of movement data 
    coil_position_desc = np.vstack(coil_position_desc)

    if not df_mvmt_desc.empty:
        coil_position_desc = np.vstack([df_mvmt_desc, coil_position_desc])

    df_coil_position_desc = pd.DataFrame(coil_position_desc)
    df_coil_position_desc = df_coil_position_desc.rename(columns = {0: 'sub_id', 1:'axis', 2: 'coil_nr', 3: 'mean', 4: 'sd', 5: 'range', 6: 'file'})
    
    df_coil_position_desc = extract.convert_to_numeric(df_coil_position_desc)
    
    df_coil_position_desc.to_csv(os.path.join(extracted_data_dir, f'HPI_mvmt_desc_{t_window}s.csv'), index = False)
    # %% Raw coil movement traces
    coil1_data = np.vstack(coil1_pos_data)
    coil2_data = np.vstack(coil2_pos_data)
    coil3_data = np.vstack(coil3_pos_data)
    coil4_data = np.vstack(coil4_pos_data)
    
    if not df_coil1.empty:
        coil1_data = np.vstack([df_coil1, coil1_data])
    if not df_coil2.empty:
        coil2_data = np.vstack([df_coil2, coil2_data])
    if not df_coil3.empty:
        coil3_data = np.vstack([df_coil3, coil3_data])
    if not df_coil4.empty:
        coil4_data = np.vstack([df_coil4, coil4_data])

    df_coil1 = pd.DataFrame(coil1_data)
    df_coil2 = pd.DataFrame(coil2_data)
    df_coil3 = pd.DataFrame(coil3_data)
    df_coil4 = pd.DataFrame(coil4_data)
    df_coil1 = df_coil1.rename(columns = {0: 'x', 1:'y', 2: 'z', 3: 'time', 4: 'displacement', 5: 'cummulative_path_length', 6: 'velocity', 7: 'sub_id'})
    df_coil2 = df_coil2.rename(columns = {0: 'x', 1:'y', 2: 'z', 3: 'time', 4: 'displacement', 5: 'cummulative_path_length', 6: 'velocity', 7: 'sub_id'})
    df_coil3 = df_coil3.rename(columns = {0: 'x', 1:'y', 2: 'z', 3: 'time', 4: 'displacement', 5: 'cummulative_path_length', 6: 'velocity', 7: 'sub_id'})
    df_coil4 = df_coil4.rename(columns = {0: 'x', 1:'y', 2: 'z', 3: 'time', 4: 'displacement', 5: 'cummulative_path_length', 6: 'velocity', 7: 'sub_id'})
    
    # Transform relevant data to numeric
    df_coil1 = extract.convert_to_numeric(df_coil1)
    df_coil2 = extract.convert_to_numeric(df_coil2)
    df_coil3 = extract.convert_to_numeric(df_coil3)
    df_coil4 = extract.convert_to_numeric(df_coil4)

    df_coil1.to_csv(os.path.join(extracted_data_dir, f'coil1_mvmt_raw_{t_window}s.csv'), index = False)
    df_coil2.to_csv(os.path.join(extracted_data_dir, f'coil2_mvmt_raw_{t_window}s.csv'), index = False)
    df_coil3.to_csv(os.path.join(extracted_data_dir, f'coil3_mvmt_raw_{t_window}s.csv'), index = False)
    df_coil4.to_csv(os.path.join(extracted_data_dir, f'coil4_mvmt_raw_{t_window}s.csv'), index = False)
    
    # %% Movement descritives
    movement_descriptives = np.vstack(movement_descriptives)
    
    if not df_movement_descriptives.empty:
        movement_descriptives = np.vstack([df_movement_descriptives, movement_descriptives])
        
    df_movement_descriptives = pd.DataFrame(movement_descriptives)
    df_movement_descriptives = df_movement_descriptives.rename(columns = {0: 'sub_id', 1: 'position', 2: 'mean_disp', 3: 'sd_disp', 4: 'mean_velocity', 5: 'sd_velocity'})        

    df_movement_descriptives = extract.convert_to_numeric(df_movement_descriptives)

    df_movement_descriptives.to_csv(os.path.join(extracted_data_dir, f'movement_characteristics_{t_window}s.csv'), index = False)
    
    print('cHPI computation finished.')
else:
    print('No subjects analyzed. Not appending any data ...')