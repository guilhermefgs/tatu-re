# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 09:09:24 2022

@author: chris
"""

from matplotlib import pyplot as plt
import statistics as st
import scipy.stats as sp


def plot_charts(list_all_results,number_of_experiments):
    for i in list(range(0,number_of_experiments)):
        
        pathOutput='C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/'+str(i)+'/'
        
        list_of_results=list_all_results[i][0]
        list_of_benchmark=list_all_results[i][1]
        list_asset_cash=list_all_results[i][2]
        
        difference=[]
        bar_label=[]
        for j,x in enumerate(list_of_results):
            
            fig,ax=plt.subplots(2,figsize=(15,7.5))
            ax[0].plot(list_of_benchmark[j].index,x,label='random strategy',color='blue')
            ax[0].plot(list_of_benchmark[j].index,list_of_benchmark[j],label='S&P',color='red')
            ax[0].set_title('Timeseries Tatu RE vs S&P')
            ax[0].legend()
            
            ax[1].plot(list_of_benchmark[j].index,list_asset_cash[j][0],color='darkblue',label='cash')
            ax[1].plot(list_of_benchmark[j].index,list_asset_cash[j][1],color='royalblue',label='asset')
            ax[1].set_title('Cash flow strategy')
            ax[1].legend()
            
            plt.tight_layout()
            plt.setp(ax[0].get_xticklabels(), visible=False)
            plt.savefig(pathOutput+'Fig '+str(j)+'.png')
            plt.clf()
            
            difference.append((x.sum()/len(x))-(list_of_benchmark[j].sum()/len(list_of_benchmark[j])))
            bar_label.append('Period '+str(list_of_benchmark[j].index[0].date()))
    
        fig,ax=plt.subplots()
        ax.bar(bar_label,difference)
        ax.set_ylabel('Differenece (Tatu RE - S&P)')
        ax.set_title('Performance comparison Tatu RE vs S&P')
        plt.tight_layout()
        plt.savefig(pathOutput+'bar chart.png')
        plt.clf()
    
    return 

def error_type1_testing(list_diff_AUC):
    list_diff_AUC=[list(x) for x in zip(*list_diff_AUC)]
    list_mean=[]
    list_std_dev=[]
    list_z_type1=[]
    
    mi=0
    
    for i in list_diff_AUC:
        n=len(i)
        list_mean.append(st.mean(i))
        list_std_dev.append(st.stdev(i))
        list_z_type1.append((list_mean[-1]-mi)/(list_std_dev[-1]/(n**0.5)))
        
    return list_mean,list_std_dev,list_z_type1,list_diff_AUC