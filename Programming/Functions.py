""" Name    : Thobani
    Surname : Maluleka
    Empl Id : MLLTHO015
    Course  : APG4005F
    Date    : Thu Aug 25 14:21:19 2022
"""

"""The python function essential for dem analysis and gravity reduction"""
import os
import math as mt
import numpy as np
import sympy as sp
import pandas as pd
import statistics as st

class data:
    """Class used to create pandas data structures in python for accessing data"""
    
    def trigonometrical_data():
        return pd.read_excel((os.getcwd())+"\\Data\\"+'trigonometrical_data.xlsx', 
                             sheet_name='Trigonometrical_Elevations')
    
    def fishnet_grid_data():
        return pd.read_excel((os.getcwd())+"\\Data\\"+'fishnet_grid_data.xlsx', 
                             sheet_name='Fishnet_Grid')
        
    def gravity_data():
        return pd.read_excel((os.getcwd())+"\\Data\\"+'gravity_data.xlsx', 
                             sheet_name='gravity_data')
    def new_data(dataset, datas):
        return pd.DataFrame(data=datas, columns=list(dataset.keys()))
    
    def all_results(sheetname):
        return pd.read_excel('all_results.xlsx', sheet_name=sheetname)
    
    def new_statistics(data1, data2):
        return {" ":["Min", "Median", "Maximum", "Mean", "Range", "Standard Dev", "RMSE"], 
                 "SRTM Statistic": list(data1),
                 "Interpolated Statistic": list(data2)}
    
    def new_gravstatistics(data1, data2, data3):
        return {" ":["Min", "Median", "Maximum", "Mean", "Range", "Standard Dev", "RMSE"], 
                 "Free-air Statistic": list(data1),
                 "Simple Bouguer Statistic": list(data2),
                 "Complete - Simple Bouguer Statistic": list(data3)}
        
class stat_analysis:
    def minimum(dataset):
        return min(dataset)
    
    def maximum(dataset):
        return max(dataset)
        
    def mean(dataset):
        return sum(dataset) / len(dataset)
    
    def rangee(dataset):
        return max(dataset) - min(dataset)
    
    def median(dataset):
        return st.median(dataset)
    
    def standard_deviation(dataset):
        return st.stdev(dataset)
    
    def root_mean_square(dataset):
        summer=0
        for i in dataset:
            summer+=(i**2)
        return mt.sqrt(summer / len(dataset))
            
    def outliers(dataset):
        upperout=dataset.quantile(q=0.5) + (6 * (dataset.quantile(q=0.75) - dataset.quantile(q=0.5))) 
        lowerout=dataset.quantile(q=0.5) - (6 * (dataset.quantile(q=0.5) - dataset.quantile(q=0.25)))
        return lowerout, upperout

  
def excel_writers(dataset, sheetname):
    try:
        with pd.ExcelWriter("all_results.xlsx", mode='a', engine='openpyxl') as writer: 
            try:
                dataset.to_excel(writer, sheet_name=sheetname, index=False, header=True)
            except:
                ""
    except:
        dataset.to_excel("all_results.xlsx", sheet_name=sheetname, index=False, header=True)


def data_statistics(dataset):
    return (stat_analysis.minimum(dataset), stat_analysis.median(dataset),
            stat_analysis.maximum(dataset), stat_analysis.mean(dataset),
            stat_analysis.rangee(dataset), stat_analysis.standard_deviation(dataset),
            stat_analysis.root_mean_square(dataset))

class anomalies:
    def latitude_correction(latitude):
        latitude=mt.radians(latitude)
        return 978031.84558 * (1 + (0.0053024*(mt.sin(latitude)**2)) - (0.0000058*(mt.sin(2 * latitude)**2)))

    def freeair_correction(elevation): 
        return 0.3086 * elevation

    def simple_bouguer_correction(elevation):
        return 0.04193 * 2.67 * elevation


def adjust(latitude, longitude, height, parameters):
    para=parameters
    H=(para[0] * latitude) + (para[1] * longitude) + (para[2] * height) + (para[3])
    return H

class lsm:
    def make_equations(dataset, sources):
        A=[]
        L=[]
        percent=1
        for i in dataset.itertuples():
            lat=i.latitude
            long=i.longitude
            if sources=='srtm':
                h_srtm=i.srtm
            elif sources=='topographical_map':
                h_srtm=i.topographical_map
            else:
                break
            h_ortho=i.levelling
            if percent<=int(len(dataset) * 0.7):
                A.append([lat, long, h_srtm, 1])
                L.append([h_ortho])
                percent+=1
        
        return A, L
                
    def parametric_lsm(A=None, L=None):
        if True:
            #%%Least Squares Mathematical function (Design, Discrepancy and Weight matrix)
            _A=sp.Matrix(np.matrix(A))
            _W=sp.Matrix(np.matrix(L))
            _P=sp.Matrix(np.eye(_A.shape[0]))
            
            #%%Parametric Least Squares Adjustment to compute correction and residual vectors
            X=(_A.T * _P * _A).inv() * _A.T * _P * _W #corrections
            V=(_A*X)-_W #residuals
        return X  

