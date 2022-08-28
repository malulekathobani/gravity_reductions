""" Name    : Thobani
    Surname : Maluleka
    Empl Id : MLLTHO015
    Course  : APG4005F
    Date    : Fri Aug 26 02:25:21 2022
"""
import pandas as pd
import Functions as fn
import statisticas as st
import terrain_corrections as tc

grav_dataset=fn.data.gravity_data()
terrain_corr=tc.terraincorrections
empty_list=[]

for i in grav_dataset.itertuples():
    TC_index=terrain_corr[terrain_corr['gsID']==i.gravity_station_ID].index.values
    TC=terrain_corr._get_value(TC_index[0], 'TC')
    datain=list(i[1:8])
    lat=i.gravity_station_latitude
    long=i.gravity_station_longitude
    h_srtm=i.gravity_station_srtm
    H_srtm=fn.adjust(lat, long, h_srtm, st.sol_srtm)
    Gobs=i.gravity_station_observed_gravity
    
    lat_corr=fn.anomalies.latitude_correction(lat)
    freeair_corr=fn.anomalies.freeair_correction(H_srtm)
    freeair_anomaly=(Gobs - lat_corr) + freeair_corr
    simple_bouguer=freeair_anomaly - fn.anomalies.simple_bouguer_correction(H_srtm)
    complete_bouguer=simple_bouguer + TC
    
    diffFAA=i.gravity_station_freeair_anomaly - freeair_anomaly
    diffSBA=i.gravity_station_simple_bouguer_anomaly - simple_bouguer
    diffCBA=i.gravity_station_simple_bouguer_anomaly - complete_bouguer
    
    dataout=datain + [H_srtm, freeair_anomaly , simple_bouguer, TC, complete_bouguer, diffFAA, diffSBA, diffCBA]
    empty_list.append(dataout)

data_columns=list(grav_dataset.keys())[0:7] + ['gravity_station_srtm_adjusted',
                                            'gravity_station_refined_freeair_anomaly',
                                            'gravity_station_refined_simple_bouguer_anomaly',
                                            'gravity_station_terrain_correction',
                                            'gravity_station__complete_bouguer_anomaly',
                                            'gravity_station_delta_freeair_anomaly',
                                            'gravity_station_delta_simple_bouguer_anomaly',
                                            'gravity_station_delta_complete_bouguer_anomaly']

data_columns=pd.DataFrame(columns=data_columns)

refined_gravity_anomalies=fn.data.new_data(data_columns, empty_list)
fn.excel_writers(refined_gravity_anomalies, 'refined_gravity_anomalies')

#%%Computing Free-air and Simple Bouguer Statistics
all_data=fn.data.all_results('refined_gravity_anomalies')

stat_faa=fn.data_statistics(all_data.gravity_station_delta_freeair_anomaly)
stat_simple_bouguer=fn.data_statistics(all_data.gravity_station_delta_simple_bouguer_anomaly)
stat_complete_bouguer=fn.data_statistics(all_data.gravity_station_delta_complete_bouguer_anomaly)
starts_new=fn.data.new_gravstatistics(stat_faa, stat_simple_bouguer, stat_complete_bouguer)

fn.excel_writers(pd.DataFrame(starts_new), 'gravity_statistics')    
