""" Name    : Thobani
    Surname : Maluleka
    Empl Id : MLLTHO015
    Course  : APG4005F
    Date    : Thu Aug 25 19:13:54 2022
"""

"""The python script to compute the minimum, mean, maximum, standard deviation
and root Mean Square Error"""



import Functions as fn
import pandas as pd
#%%Statistic before polynomial application
all_data=fn.data.all_results('outlier_removed')

stat_srtm=fn.data_statistics(all_data.delta_srtm)
stat_topographical_map=fn.data_statistics(all_data.delta_topographical_map)
starts_new=fn.data.new_statistics(stat_srtm, stat_topographical_map)

fn.excel_writers(pd.DataFrame(starts_new), 'stats_before_adjustment')

#Polynomial Application
A=[]
L=[]
print(int(len(all_data) * 0.7))
percent=0
for i in all_data.itertuples():
    lat=i.latitude
    long=i.longitude
    h_srtm=i.srtm
    h_ortho=i.levelling
    while percent<=int(len(all_data) * 0.7):
        A.append([lat, long, h_srtm, 1])
        L.append([h_ortho])
    percent+=1
        
#print(percent)   

corrections=fn.lsm.parametric_lsm(A, L)


#%%Statistic after polynomial application