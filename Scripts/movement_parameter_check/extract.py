#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 13:18:52 2025

@author: jan
"""
import mne
import numpy as np
import pandas as pd
import os

center_function = lambda x: x - np.mean(x)
init_pos_function = lambda x: x - x[0]


def set_up_data_environment(path_to_data, t_window, subj_id = ''):
    
    crosstalk_file = '/home/jan/Jan/meg_related/tSSS_config/ct_sparse.fif'
    calibration_file = '/home/jan/Jan/meg_related/tSSS_config/sss_cal.dat'

    try:
        df_mvmt_desc = pd.read_csv(os.path.join(path_to_data, f'HPI_mvmt_desc_{t_window}s.csv'))
    except FileNotFoundError:
        df_mvmt_desc = pd.DataFrame()

    try: 
        df_coil1 = pd.read_csv(os.path.join(path_to_data, f'coil1_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil1 = pd.DataFrame()
        
    try: 
        df_coil2 = pd.read_csv(os.path.join(path_to_data, f'coil2_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil2 = pd.DataFrame()

    try: 
        df_coil3 = pd.read_csv(os.path.join(path_to_data, f'coil3_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil3 = pd.DataFrame()

    try: 
        df_coil4 = pd.read_csv(os.path.join(path_to_data, f'coil4_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil4 = pd.DataFrame()    

    try: 
        df_movement_descriptives = pd.read_csv(os.path.join(path_to_data, f'movement_characteristics_{t_window}s.csv'))
    except FileNotFoundError:
        df_movement_descriptives = pd.DataFrame()    

    try:
        df_head_mvmt_raw = pd.read_csv(os.path.join(path_to_data, f'head_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError: 
        df_head_mvmt_raw = pd.DataFrame()
    try:
        df_metadata_info = pd.read_csv(os.path.join(path_to_data, f'metadata_coils_within_{t_window}s.csv'))
    except FileNotFoundError: 
        df_metadata_info = pd.DataFrame()
        
    return crosstalk_file, calibration_file, df_mvmt_desc, df_coil1, df_coil2, df_coil3, df_coil4, df_movement_descriptives, df_head_mvmt_raw, df_metadata_info


def set_up_data_environment_WP2(path_to_data, t_window, subj_id):
    
    crosstalk_file = '/home/jan/Jan/meg_related/tSSS_config/ct_sparse.fif'
    calibration_file = '/home/jan/Jan/meg_related/tSSS_config/sss_cal.dat'

    try:
        df_mvmt_desc = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_HPI_mvmt_desc_{t_window}s.csv'))
    except FileNotFoundError:
        df_mvmt_desc = pd.DataFrame()

    try: 
        df_coil1 = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_coil1_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil1 = pd.DataFrame()
        
    try: 
        df_coil2 = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_coil2_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil2 = pd.DataFrame()

    try: 
        df_coil3 = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_coil3_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil3 = pd.DataFrame()

    try: 
        df_coil4 = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_coil4_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError:
        df_coil4 = pd.DataFrame()    

    try: 
        df_movement_descriptives = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_movement_characteristics_{t_window}s.csv'))
    except FileNotFoundError:
        df_movement_descriptives = pd.DataFrame()    

    try:
        df_head_mvmt_raw = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_head_mvmt_raw_{t_window}s.csv'))
    except FileNotFoundError: 
        df_head_mvmt_raw = pd.DataFrame()
    try:
        df_metadata_info = pd.read_csv(os.path.join(path_to_data, f'{subj_id}_metadata_coils_within_{t_window}s.csv'))
    except FileNotFoundError: 
        df_metadata_info = pd.DataFrame()
        
    return crosstalk_file, calibration_file, df_mvmt_desc, df_coil1, df_coil2, df_coil3, df_coil4, df_movement_descriptives, df_head_mvmt_raw, df_metadata_info

def extract_metadata(file, id_ident):
    '''

    Parameters
    ----------
    file : str
        Path to raw .fif file
    id_ident : str
        ID indentifier

    Returns
    -------
    extracted_metadata : list
        Summary of metadata. Contains:
            Subject Identification, Coil Identification, active frequency, goodness of fit, usage and if the fit was accepted

    '''
    
    extracted_metadata = []
    raw_metadata = mne.io.read_info(file, verbose = False)
    
    accepted_fit = raw_metadata['hpi_results'][0]['accept']
        
    for coil in raw_metadata['hpi_results'][0]['order']:
        gof = raw_metadata['hpi_results'][0]['goodness'][coil-1]
        freq = raw_metadata['hpi_meas'][0]['hpi_coils'][coil-1]['coil_freq']
        usage = 'Yes' if coil in raw_metadata['hpi_results'][0]['used'] else 'No'
        
        if usage == 'No':
            print(f'\nNot all HPI coils were used!\nCoil {coil} is not used.\n')
        extracted_metadata.append([id_ident, coil, freq, gof, usage, accepted_fit])
        
    return extracted_metadata

def extract_metadata_WP2(file, id_ident):
    '''

    Parameters
    ----------
    file : str
        Path to raw .fif file
    id_ident : str
        ID indentifier

    Returns
    -------
    extracted_metadata : list
        Summary of metadata. Contains:
            Subject Identification, Coil Identification, active frequency, goodness of fit, usage and if the fit was accepted

    '''
    condition, run = extract_condition_idents(file)
    
    extracted_metadata = []
    raw_metadata = mne.io.read_info(file, verbose = False)
    
    accepted_fit = raw_metadata['hpi_results'][0]['accept']
        
    for coil in raw_metadata['hpi_results'][0]['order']:
        gof = raw_metadata['hpi_results'][0]['goodness'][coil-1]
        freq = raw_metadata['hpi_meas'][0]['hpi_coils'][coil-1]['coil_freq']
        usage = 'Yes' if coil in raw_metadata['hpi_results'][0]['used'] else 'No'
        
        if usage == 'No':
            print(f'\nNot all HPI coils were used!\nCoil {coil} is not used.\n')
        extracted_metadata.append([id_ident, coil, freq, gof, usage, accepted_fit, condition, run])
        
    return extracted_metadata
    
def extract_cHPI_elekta(raw_data, t_window, t_step_max, id_ident):
    '''

    Parameters
    ----------
    raw_data : raw object
        raw object, loaded in via. mne.io.read_raw_fif()
    t_window : float
        Time window to use to estimate the amplitudes.
    t_step_max : float
        Maximum time step to use.
    id_ident : str
        ID indentifier.

    Returns
    -------
    head_pos_centered : ndarray
        Contains head position estimation. The [t, q1, q2, q3, x, y, z, gof, err, v] for each fit.
    coil_dict : dict
        Contains for each coil a subfield with its respective x, y, z coordinates plus a time entry

    '''
    print('Calculating HPI amplitudes.\n')
    chpi_amplitudes = mne.chpi.compute_chpi_amplitudes(raw_data, t_window=t_window, verbose=False)

    print('Calculating HPI locations.\n')
    # returns a dict with 4 outputs -> rrs contains the estimated position from the HPI coils
    # 1 estimate per second, with 4 hpi coils and 3 dimensions (x,y,z) in m
    chpi_locs = mne.chpi.compute_chpi_locs(raw_data.info, chpi_amplitudes, t_step_max=t_step_max, too_close='warning', verbose=False)
    
    # Calculate head center movement (mne function)
    print('Calculating head position.\n')
    head_pos = mne.chpi.compute_head_pos(raw_data.info, chpi_locs, verbose = False)
    
    head_pos_centered = head_pos.copy()
    for i in range(0, 9):
        if i == 0:
            head_pos_centered[:, i] = init_pos_function(head_pos[:, i])
        else:
            head_pos_centered[:, i] = center_function(head_pos[:, i] * -1000)
        
    head_pos_centered = np.column_stack((head_pos_centered, np.repeat(id_ident, len(head_pos_centered))))

    # get coils estimates for each axis
    # split 3D array to get a seperate df for each coil
    coil1, coil2, coil3, coil4 = np.split(chpi_locs['rrs'], 4, axis = 1)
    coil_dict = {'time': chpi_locs['times'],
                 'coil1': np.squeeze(coil1, axis = 1),
                 'coil2': np.squeeze(coil2, axis = 1),
                 'coil3': np.squeeze(coil3, axis = 1),
                 'coil4': np.squeeze(coil4, axis = 1)}
    
    return head_pos_centered, coil_dict


def calculate_movement_characteristics(positions, init_pos, delta_t):
   
    displacement = np.linalg.norm(positions-init_pos, axis = 1)
    
    diff = np.diff(positions, axis = 0)
    distances = np.linalg.norm(diff, axis = 1)
    cum_dist = np.insert(np.cumsum(distances), 0, 0)
        
    velocity = distances/delta_t
    velocity = np.insert(velocity, 0, 0)
    
    return displacement, cum_dist, velocity


def get_cHPI_descriptive(coil_dict, id_ident, ID_file, metadata):
    
    '''
    
    Parameters
    ----------
    coil_dict : dict
       should be the output from extract_cHPI_elekta()
    head_pos_centered : ndarray
        should be the output from extract_cHPI_elekta()
    id_ident : str
        Path to raw .fif file
    ID_file : str
        ID indentifier

    Returns
    -------
    ID_coil_desc : TYPE
        DESCRIPTION.
    coil_dict_centered : dict
        DESCRIPTION

    '''
    ID_coil_desc = []
    movement_desc_sub = []
    coil_dict_centered = coil_dict.copy()
    for name, coil in coil_dict_centered.items():
        
        if name == 'time':
            coil_dict_centered[name] = init_pos_function(coil)
            delta_t = np.diff(coil)
            continue
        else:
            
            for axs in range(0, coil.shape[1]):

                coil_dict_centered[name][:, axs] = center_function(coil[:, axs]*-1000) # to bring data from a m to a mm scaling
            
                if axs == 0:
                    ax = 'x'
                elif axs == 1:
                    ax = 'y'
                else:
                    ax = 'z'
                
                ID_c_coil_mean = np.mean(coil_dict_centered[name][:, axs])
                ID_c_coil_sd = np.std(coil_dict_centered[name][:, axs])
                ID_c_coil_range = np.max(coil_dict_centered[name][:, axs]) - np.min(coil_dict_centered[name][:, axs])
                
                temp_data = [id_ident, ax, name, ID_c_coil_mean, ID_c_coil_sd, ID_c_coil_range, ID_file]
                
                ID_coil_desc.append(temp_data)
        
        if metadata[int(name[4])-1][4] != 'No':
            init_pos = np.array([coil_dict_centered[name][0, 0], coil_dict_centered[name][0, 1], coil_dict_centered[name][0, 2]])
            positions = np.column_stack((coil_dict_centered[name][:, 0], coil_dict_centered[name][:, 1], coil_dict_centered[name][:, 2]))
        
            displacement, cum_dist, velocity = calculate_movement_characteristics(positions, init_pos, delta_t)
            
            mean_disp = np.mean(displacement)
            sd_disp = np.std(displacement)
            mean_velocity = np.mean(velocity)
            sd_velocity = np.std(velocity)
            movement_desc_sub.append([id_ident, name, mean_disp, sd_disp, mean_velocity, sd_velocity])
        else:
            displacement = np.repeat(np.nan, len(coil_dict_centered[name]))
            cum_dist = np.repeat(np.nan, len(coil_dict_centered[name]))
            velocity = np.repeat(np.nan, len(coil_dict_centered[name]))
            
        
        coil_dict_centered[name] = np.column_stack((coil_dict_centered[name], coil_dict_centered['time'], displacement, 
                                                   cum_dist, velocity, np.repeat(id_ident, len(coil_dict_centered[name]))))
        
    
    return coil_dict_centered, movement_desc_sub, ID_coil_desc

def get_cHPI_descriptive_WP2(coil_dict, id_ident, ID_file, metadata):
    
    '''
    
    Parameters
    ----------
    coil_dict : dict
       should be the output from extract_cHPI_elekta()
    head_pos_centered : ndarray
        should be the output from extract_cHPI_elekta()
    id_ident : str
        Path to raw .fif file
    ID_file : str
        ID indentifier

    Returns
    -------
    ID_coil_desc : TYPE
        DESCRIPTION.
    coil_dict_centered : dict
        DESCRIPTION

    '''
    
    condition, run = extract_condition_idents(ID_file)
    
    ID_coil_desc = []
    movement_desc_sub = []
    coil_dict_centered = coil_dict.copy()
    for name, coil in coil_dict_centered.items():
        
        if name == 'time':
            coil_dict_centered[name] = init_pos_function(coil)
            delta_t = np.diff(coil)
            continue
        else:
            
            for axs in range(0, coil.shape[1]):

                coil_dict_centered[name][:, axs] = center_function(coil[:, axs]*-1000) # to bring data from a m to a mm scaling
            
                if axs == 0:
                    ax = 'x'
                elif axs == 1:
                    ax = 'y'
                else:
                    ax = 'z'
                
                ID_c_coil_mean = np.mean(coil_dict_centered[name][:, axs])
                ID_c_coil_sd = np.std(coil_dict_centered[name][:, axs])
                ID_c_coil_range = np.max(coil_dict_centered[name][:, axs]) - np.min(coil_dict_centered[name][:, axs])
                
                temp_data = [id_ident, ax, name, ID_c_coil_mean, ID_c_coil_sd, ID_c_coil_range, ID_file, condition, run]
                
                ID_coil_desc.append(temp_data)
        
        if metadata[int(name[4])-1][4] != 'No':
            init_pos = np.array([coil_dict_centered[name][0, 0], coil_dict_centered[name][0, 1], coil_dict_centered[name][0, 2]])
            positions = np.column_stack((coil_dict_centered[name][:, 0], coil_dict_centered[name][:, 1], coil_dict_centered[name][:, 2]))
        
            displacement, cum_dist, velocity = calculate_movement_characteristics(positions, init_pos, delta_t)
            
            mean_disp = np.mean(displacement)
            sd_disp = np.std(displacement)
            mean_velocity = np.mean(velocity)
            sd_velocity = np.std(velocity)
            movement_desc_sub.append([id_ident, name, mean_disp, sd_disp, mean_velocity, sd_velocity, condition, run])
        else:
            displacement = np.repeat(np.nan, len(coil_dict_centered[name]))
            cum_dist = np.repeat(np.nan, len(coil_dict_centered[name]))
            velocity = np.repeat(np.nan, len(coil_dict_centered[name]))
            
        coil_dict_centered[name] = np.column_stack((np.repeat(id_ident, len(coil_dict_centered[name])), coil_dict_centered[name], coil_dict_centered['time'], displacement, 
                                                   cum_dist, velocity, np.repeat(condition, len(coil_dict_centered[name])), np.repeat(run, len(coil_dict_centered[name]))))
        
    
    return coil_dict_centered, movement_desc_sub, ID_coil_desc
        
    
def process_head_center(head_pos_centered, ID_coil_desc, movement_desc_sub, id_ident, ID_file):
    for i in range(4, 7):
        
        if i == 4:
            ax = 'x'
        elif i == 5:
            ax = 'y'
        else:
            ax = 'z'
        
        ID_coil_desc.append([id_ident, 
                             ax, 
                             'head_center', 
                             np.mean(head_pos_centered[:, i].astype(np.float32)), 
                             np.std(head_pos_centered[:, i].astype(np.float32)), 
                             np.max(head_pos_centered[:, i].astype(np.float32)) - np.min(head_pos_centered[:, i].astype(np.float32)), 
                             ID_file])
        
        
    init_pos = np.array([float(head_pos_centered[0, 4]), float(head_pos_centered[0, 5]), float(head_pos_centered[0, 6])])
    positions = np.column_stack((head_pos_centered[:, 4].astype(np.float32), head_pos_centered[:, 5].astype(np.float32), head_pos_centered[:, 6].astype(np.float32)))
    
    displacement, cum_dist, velocity = calculate_movement_characteristics(positions, init_pos, np.diff(head_pos_centered[:, 0].astype(np.float32)))
    
    mean_disp = np.mean(displacement)
    sd_disp = np.std(displacement)
    mean_velocity = np.mean(velocity)
    sd_velocity = np.std(velocity)
    
    head_pos_centered = np.column_stack((head_pos_centered, displacement, cum_dist, velocity))
    
    ID_coil_desc = np.vstack(ID_coil_desc)
    movement_desc_sub.append([id_ident, 'head_center', mean_disp, sd_disp, mean_velocity, sd_velocity])

    return ID_coil_desc, head_pos_centered, movement_desc_sub

def process_head_center_WP2(head_pos_centered, ID_coil_desc, movement_desc_sub, id_ident, ID_file):
    
    condition, run = extract_condition_idents(ID_file)
    
    for i in range(4, 7):
        
        if i == 4:
            ax = 'x'
        elif i == 5:
            ax = 'y'
        else:
            ax = 'z'
        
        ID_coil_desc.append([id_ident, 
                             ax, 
                             'head_center', 
                             np.mean(head_pos_centered[:, i].astype(np.float32)), 
                             np.std(head_pos_centered[:, i].astype(np.float32)), 
                             np.max(head_pos_centered[:, i].astype(np.float32)) - np.min(head_pos_centered[:, i].astype(np.float32)), 
                             ID_file, condition, run])
        
        
    init_pos = np.array([float(head_pos_centered[0, 4]), float(head_pos_centered[0, 5]), float(head_pos_centered[0, 6])])
    positions = np.column_stack((head_pos_centered[:, 4].astype(np.float32), head_pos_centered[:, 5].astype(np.float32), head_pos_centered[:, 6].astype(np.float32)))
    
    displacement, cum_dist, velocity = calculate_movement_characteristics(positions, init_pos, np.diff(head_pos_centered[:, 0].astype(np.float32)))
    
    mean_disp = np.mean(displacement)
    sd_disp = np.std(displacement)
    mean_velocity = np.mean(velocity)
    sd_velocity = np.std(velocity)
    
    head_pos_centered = np.column_stack((head_pos_centered, displacement, cum_dist, velocity, np.repeat(condition, len(displacement)), np.repeat(run, len(displacement))))
    
    ID_coil_desc = np.vstack(ID_coil_desc)
    movement_desc_sub.append([id_ident, 'head_center', mean_disp, sd_disp, mean_velocity, sd_velocity, condition, run])

    return ID_coil_desc, head_pos_centered, movement_desc_sub

def convert_to_numeric(pd_dataframe):
    
    variables = list(pd_dataframe)
    
    for col in variables:
        if col in ['gof', 'time', 'q1', 'q2', 'q3', 'x', 'y', 'z', 'err', 'v', 'mean', 'sd', 'range', 'displacement', 'cummulative_path_length', 'velocity']:
            pd_dataframe[col] = pd.to_numeric(pd_dataframe[col], errors='coerce')
    
    return pd_dataframe

# def extract_condition_idents(file):
#     filename = file.split(os.sep)[-1]
#     fileparts = filename.split('_')
#     medState = fileparts[[i for i, s in enumerate(fileparts) if 'med'.lower() in s.lower()][0]]
#     stimState = fileparts[[i for i, s in enumerate(fileparts) if 'stim'.lower() in s.lower()][0]]
#     run = fileparts[[i for i, s in enumerate(fileparts) if 'run'.lower() in s.lower()][0]]
#     condition = medState + '_' + stimState
    
#     return condition, run

def extract_condition_idents(file):
    filename = file.split(os.sep)[-1]
    fileparts = filename.split('_')

    med_idx = next((i for i, s in enumerate(fileparts)
                    if 'med' in s.lower()), None)
    stim_idx = next((i for i, s in enumerate(fileparts)
                     if 'stim' in s.lower()), None)
    run_idx = next((i for i, s in enumerate(fileparts)
                    if 'run' in s.lower()), None)

    medState  = fileparts[med_idx]  if med_idx  is not None else ''
    stimState = fileparts[stim_idx] if stim_idx is not None else ''
    run       = fileparts[run_idx]  if run_idx  is not None else ''

    # only add underscore if both parts exist
    if medState and stimState:
        condition = f"{medState}_{stimState}"
    else:
        condition = ''

    return condition, run


# def extract_condition_idents_HC(file):
#     filename = file.split(os.sep)[-1]
#     fileparts = filename.split('_')
#     run = fileparts[[i for i, s in enumerate(fileparts) if 'run'.lower() in s.lower()][0]]
    
#     return run