#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:28:02 2025

@author: hugo
"""

import os
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import mne
import pandas as pd
import seaborn as sns

def plot_sd(pd_dataframe, x_axis, y_axis, hue, order, hue_order, out_path=None):
    
    # # Plot results (similar to Bonaiuto et al., 2018)
    # sns.stripplot(pd_dataframe, x = x_axis, y = y_axis, hue = hue, order = order, hue_order = hue_order, palette='colorblind', size = 8)
    # # Insert border between coils
    # # Not necessary anymore if space is inserted
    # plt.axvline(2.5, 0, 2, color = 'black')
    # plt.axvline(5.5, 0, 2, color = 'black')
    # plt.axvline(8.5, 0, 2, color = 'black')
    # # Define the legend to be placed outside of the plot
    # plt.legend(title='sub_id', loc = 'upper center', fontsize = 8, bbox_to_anchor=(1.2,1))
    # Change the axis ticks
    # # TODO: Insert space after three ticks for clearer visibility
    # plt.xticks(ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 
    #            labels = ['x', 'y', 'z', 'x', 'y', 'z', 'x', 'y', 'z', 'x', 'y', 'z'])
    # plt.xlabel('')
    # plt.ylabel('Standard Deviation (mm)')
    # plt.title('Standard deviation of full recording (3 min)')
    # plt.text(0.5, -0.2, 'Coil 1')
    # plt.text(3.5, -0.2, 'Coil 2')
    # plt.text(6.5, -0.2, 'Coil 3')
    # plt.text(9.5, -0.2, 'Coil 4')
    
    # Alternate version by Perplexity
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.stripplot(
        data=pd_dataframe,
        x=x_axis,
        y=y_axis,
        hue=hue,
        order=order,
        hue_order=hue_order,
        palette='colorblind',
        size=8,          # datapoint size
        jitter=True,     # optional
        ax=ax
    )
    
    # Borders between coil groups
    ax.axvline(2.5, color='black', linewidth = 2)
    ax.axvline(5.5, color='black', linewidth = 2)
    ax.axvline(8.5, color='black', linewidth = 2)
    
    # Tick-label font size
    ax.tick_params(
        axis='both',
        which='major',
        labelsize=20
    )
    
    
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    
    # Keep only the left and bottom borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    
    # Optional: make the remaining borders slightly thicker
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)

    # Axis-label font size
    ax.set_xlabel('', fontsize=20)
    ax.set_ylabel('Standard Deviation (mm)', fontsize=20)
    
    # Title
    ax.set_title(
        'Standard deviation of full recording (3 min)',
        fontsize=20, fontweight = 'bold'
    )
    
    ax.set_xticks(range(12))
    ax.set_xticklabels(
        ['x', 'y', 'z'] * 4,
        fontsize=20, fontweight = 'bold'
    )
    
    # Coil labels
    ax.text(1, -0.2, 'HPI 1', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=20, fontweight = 'bold')
    ax.text(4, -0.2, 'HPI 2', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=20, fontweight = 'bold')
    ax.text(7, -0.2, 'HPI 3', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=20, fontweight = 'bold')
    ax.text(10, -0.2, 'HPI 4', transform=ax.get_xaxis_transform(),
            ha='center', fontsize=20, fontweight = 'bold')
    
    ax.legend(
        title='sub_id',
        loc='upper left',
        bbox_to_anchor=(1.02, 1),
        fontsize=8,
        title_fontsize=9
    )
    
    plt.tight_layout()
    plt.show()

    
    if out_path:
        plt.savefig(os.path.join(out_path, 'movement_sd_patients_within.svg'), dpi = 300, bbox_inches = 'tight', pad_inches = 0.1)
        plt.close()
    
    return plt

def plot_timeseries(pd_dataframe, x, y, out_dir=None, color = 'black',
                    alpha = 1, regplot = True, lowess = True, scatter = False,
                    var_specific = None, cols=2, hue=None, hue_order=None, 
                    share_x = False, share_y = False, ylim = [-5, 5],
                    fontsize = 8, errorbar = 'ci'):
    
    if var_specific != None:
        out_name = y + '_' + var_specific + '_specific'
        
        g_facet = sns.FacetGrid(pd_dataframe, col = var_specific, col_wrap = cols, hue=hue, hue_order = hue_order,
                  sharex=share_x, sharey=share_y, ylim = ylim)
        g_facet.map(sns.lineplot, x, y)
        g_facet.add_legend()
        if out_dir:
            g_facet.savefig(os.path.join(out_dir, f'{out_name}.svg'), dpi = 300, bbox_inches = 'tight', pad_inches = 0.1)
            plt.close()    
    
    else:
        
        out_name = y + '_averaged'
        sns.lineplot(pd_dataframe, x = x, y=y, alpha = alpha, hue=hue, color = 'gray', errorbar=errorbar)
        plt.ylim(ylim[0], ylim[1])
        
        if regplot:
            if lowess:
                label = 'Locally weighted \nscatterplot smoothing'
            else:
                label = 'Linear regression estimation'
            sns.regplot(data=pd_dataframe, x=x, y=y, lowess=lowess, 
                        scatter=scatter, color = color, label = label)
        plt.legend(title='Subject ID', loc = 'upper center', fontsize = 8, bbox_to_anchor=(1.2,1))
        if out_dir:
            plt.savefig(os.path.join(out_dir, f'{out_name}.svg'), dpi = 300, bbox_inches = 'tight', pad_inches = 0.1)
            plt.close()