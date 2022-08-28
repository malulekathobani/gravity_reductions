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
Asrtm,Lsrtm=fn.lsm.make_equations(all_data, 'srtm')
sol_srtm=fn.lsm.parametric_lsm(Asrtm, Lsrtm)

Atopomap,Ltopomap=fn.lsm.make_equations(all_data, 'topographical_map')
sol_topomap=fn.lsm.parametric_lsm(Atopomap, Ltopomap)

empty_list=[]


for i in all_data.itertuples():
    datain=list(i[1:9])
    lat=i.latitude
    long=i.longitude
    
    level=i.levelling
    srtm=i.srtm
    topo=i.topographical_map
    
    srtm_adj=(sol_srtm[0] * lat) + (sol_srtm[1] * long) + (sol_srtm[2] * srtm) + (sol_srtm[3])
    topo_adj=(sol_topomap[0] * lat) + (sol_topomap[1] * long) + (sol_topomap[2] * topo) + (sol_topomap[3])
    delt_srtm=level - srtm_adj
    delt_topomap=level - topo_adj
    
    empty_list.append(datain + [srtm_adj, topo_adj, delt_srtm, delt_topomap])

polynomial_adjusted=fn.data.new_data(all_data, empty_list)
fn.excel_writers(polynomial_adjusted, 'polynomial_adjusted')


all_data=fn.data.all_results('polynomial_adjusted')

stat_srtm=fn.data_statistics(all_data.delta_srtm)
stat_topographical_map=fn.data_statistics(all_data.delta_topographical_map)
starts_new=fn.data.new_statistics(stat_srtm, stat_topographical_map)

fn.excel_writers(pd.DataFrame(starts_new), 'stats_after_adjustment')



#%%Statistic after polynomial application