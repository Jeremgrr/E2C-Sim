#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 02:47:48 2022

@author: c00424072
"""

import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats
import numpy as np

    
workload_name = 'heterogeneous'
scenario = 'sc-1'

schedulers = ['MM','MECT','FCFS']
#schedulers = ['MECT']

cut = 100
objective = 'totalCompletion%'
#objective = 'consumed_energy%'


df_summary = pd.DataFrame(data=None, columns = ['sample','het-idx','scheduler' ,'totalCompletion%'])
df = pd.DataFrame(data=None, columns = ['sample','het-idx','scheduler' ,'totalCompletion%'])

path_h_indices = f'../../workload/etcs/{workload_name}/hindices.csv'

df_h = pd.read_csv(path_h_indices)
#df_h = df_h.sort_values(by='H_index')
het_indices = df_h['h_index'].values
df['het-idx'] = het_indices
df['sample'] = df_h['etc_id'].values
#df['speedup'] = df_h['speedup'].values





for scheduler in schedulers:        
    for etc_id in range(cut):
        if not etc_id in [1000]:
            path = f'../../output/data/{workload_name}/{scenario}/etc-{etc_id}/{scheduler}/results-summary.csv'
            d = pd.read_csv(path, usecols= [objective])              
            df.loc[df['sample']==etc_id, ['scheduler', objective]] = [ scheduler, d.mean().loc[[objective]].values]
            #df_summary.loc[df_summary['sample']==h, ['scheduler', objective]] = [ scheduler, df.mean().loc[[objective]].values]
    df_summary = df_summary.append(df, ignore_index = True)
        
df_summary = df_summary.dropna()
   
#exit()
colors = ['navy','darkred','orange', 'purple','darkgreen', 'red', 'blue']
markers = ['o','p','<','s','p','*', 's']


fig, ax1 = plt.subplots(figsize=(8,4))
#ax2 = ax1.twinx()

i=0

for scheduler in schedulers:
    
    results = df_summary[df_summary['scheduler']==scheduler]
    results = results.sort_values('het-idx')
    results = results.iloc[:cut,:]
    
    if scheduler == 'EE':
        label = 'ELARE'
    elif scheduler == 'FEE':
        label = 'FELARE'
    else:
        label = scheduler    
    
    objective_data = results[objective].values   
    #objective_data *= 50
    het_ids = results['het-idx'].values
    if objective =='totalCompletion%':
        objective_data = 100 - objective_data
    
    ax1.plot(het_ids, objective_data, 
             marker = markers[i],
             color= colors[i],
             #linestyle='-',
             markersize = 5,
            label = label)
    i+=1


if objective == 'totalCompletion%':
    ylabel = '%unsuccessful tasks' 
else:
    ylabel = '%consumed energy'
ax1.set_ylabel(ylabel, fontsize = 14)
ax1.set_xlabel('H-index', fontsize = 14)


    

ax1.legend()
#ax1.tight_layout()
#plt.savefig(f'../../output/figures/missrate_vs_h_index_1.pdf',dpi=300)

# fig, ax3 = plt.subplots()
    
# for scheduler in schedulers:
    
#     results = df_summary[df_summary['scheduler']==scheduler]
#     results = results.sort_values('speedup')
#     results = results.iloc[:cut,:]
    
#     if scheduler == 'EE':
#         label = 'ELARE'
#     elif scheduler == 'FEE':
#         label = 'FELARE'
#     else:
#         label = scheduler    
    
#     objective_data = results[objective].values   
#     #objective_data *= 50
#     speedup = results['speedup'].values
#     if objective =='totalCompletion%':
#         objective_data = 100 - objective_data
    
#     ax3.plot(speedup, objective_data, 
#              marker = markers[i],
#              color= colors[i],
#              #linestyle='-',
#              markersize = 5,
#             label = label)
#     i+=1    

# if objective == 'totalCompletion%':
#     ylabel = '%unsuccessful tasks' 
# else:
#     ylabel = '%consumed energy'
# ax3.set_ylabel(ylabel, fontsize = 14)
# ax3.set_xlabel('speedup', fontsize = 14)


    

# ax3.legend()
#ax3.tight_layout()
#plt.savefig(f'../../output/figures/missrate_vs_h_index_1.pdf',dpi=300)


no_schedulers = len(schedulers)

#plt.savefig(f'../../output/figures/{ylabel}_hindex_{scenario}_0-{cut}_{no_schedulers}_schedulers.jpg',dpi=300)



# plt.figure()

# scheduler = schedulers[0]
    
# results = df_summary[df_summary['scheduler']==scheduler]
# results = results.sort_values('het-idx')
# results = results.iloc[:cut,:]



# het_ids = results['het-idx'].values   
# speedup = results['speedup'].values 
# ax2.plot(het_ids, speedup, 
#          marker = '*',
#           color= 'k',
#           linestyle='--',
#         label = 'speedup')

# ax2.set_ylabel('speedup', fontsize = 14)



# plt.xlabel('H-index', fontsize= 14)
# plt.ylabel('%unsuccessful tasks', fontsize= 14)
# #plt.xlim(0,100)
# #plt.ylim(0,100)
# # plt.legend(loc=(0.78,0.1))
# plt.legend()
# plt.tight_layout()
#plt.savefig(f'../../output/figures/missrate_vs_h_index_1.pdf',dpi=300)
   


