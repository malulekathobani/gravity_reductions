""" Name    : Thobani
    Surname : Maluleka
    Empl Id : MLLTHO015
    Course  : APG4005F
    Date    : Thu Aug 25 14:00:22 2022
"""

import Functions as fn

trig_data=fn.data.trigonometrical_data()

lower_srtm, upper_srtm=fn.stat_analysis.outliers(trig_data.delta_srtm)
lower_topomap, upper_topomap=fn.stat_analysis.outliers(trig_data.delta_topographical_map)

empty_list=[];  outlier_names=[]

for i in trig_data.itertuples():
    if (i.delta_srtm<lower_srtm or i.delta_srtm>upper_srtm) and (i.delta_topographical_map<lower_topomap or i.delta_topographical_map>upper_topomap):
        outlier_names.append(i.Name)       
    else:
        empty_list.append(list(i[1:]))
                 
trigonometrical_data_outlier_removed=fn.data.new_data(trig_data, empty_list)
fn.excel_writers(trigonometrical_data_outlier_removed, 'outlier_removed')
