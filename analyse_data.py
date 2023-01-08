# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 09:09:24 2022

@author: chris
"""

from matplotlib import pyplot as plt
import statistics as st
import scipy.stats as sp
import pylab

def plot_charts(list_check_in_cash, list_check_in_asset,list_check_total,list_check_benchmark):
    
    for i,x in enumerate(list_check_total[0]):
        
        pathOutput='C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/week plots/'
        date_string=[]
        for j in list_check_benchmark[0][i].index:
            date_string.append(str(j.year) + '-' + str(j.month) + '-' + str(j.day))
        
        fig,ax=plt.subplots(2,figsize=(10,5))
        
        ax[0].plot(date_string,list_check_benchmark[0][i],label='stock',color='blue')
        ax[0].plot(date_string,x,label='selected strategy',color='red')        
        ax[0].set_title('Performance strategy vs stock')
        ax[0].legend()
        
        
        ax[1].plot(date_string,list_check_in_cash[0][i],label='money in cash',color='lime')
        ax[1].plot(date_string,list_check_in_asset[0][i],label='invested money',color='darkgreen')   
        ax[1].set_title('Selected strategy cash flow')
        ax[1].legend()
        
        plt.tight_layout()
        # plt.setp(ax[0].get_xticklabels(), visible=False)
        plt.savefig(pathOutput+'week '+str(i+1)+'.png')
        plt.clf()

    return

def error_type1_testing(list_diff_AUC,alfa):
    
    pathOutput='C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/box plots/'
    
    list_diff_AUC=[list(x) for x in zip(*list_diff_AUC)]
    list_mean=[]
    list_std_dev=[]
    list_t_type1=[]
        
    mi=0
    
    for i,x in enumerate(list_diff_AUC):
        n=len(x)
        list_mean.append(st.mean(x))
        list_std_dev.append(st.stdev(x))
        list_t_type1.append((list_mean[-1]-mi)/(list_std_dev[-1]/(n**0.5)))
    
        plt.figure(1)
        plt.boxplot(x)
        plt.xticks([1],['Chosen strategy Week '+str(i+1)])
        plt.savefig(pathOutput+'Week '+str(i+1))
        plt.close()
    
    DF=len(list_diff_AUC[0])
    
    alfa=alfa/(len(list_diff_AUC[0])) #bonferroni correction
    
    t_inf=(-sp.t.ppf(1-alfa/2,DF)) 
    t_sup=sp.t.ppf(1-alfa/2,DF)

    print('\n % times above t score: '+'{:.2%}'.format(sum(i>t_sup for i in list_t_type1)/len(list_t_type1)))
    print('\n % times below t score: '+'{:.2%}'.format(sum(i<t_inf for i in list_t_type1)/len(list_t_type1)))
    print('\n % times below or above t score: '+'{:.2%}\n'.format((sum(i>t_sup for i in list_t_type1)+sum(i<t_inf for i in list_t_type1))/len(list_t_type1)))
    
    return list_mean,list_std_dev,list_t_type1,list_diff_AUC

def error_type2_testing(list_diff_AUC,list_power,alfa,beta):
    
    list_diff_AUC=[list(x) for x in zip(*list_diff_AUC)]
    mi=0
    
    DF=len(list_diff_AUC[0])
    t_inf=(-sp.t.ppf(1-alfa/2,DF)) 
    t_sup=sp.t.ppf(1-alfa/2,DF)
    
    power=[]
    
    for i in list_power:
        mi_power=i
        power_partial=[]
        for j in list_diff_AUC:         
            x_barra_inf=(t_inf*st.stdev(j)/(len(j)**0.5))+mi
            x_barra_sup=(t_sup*st.stdev(j)/(len(j)**0.5))+mi
            
            pValueInf=sp.t.cdf((x_barra_inf-mi_power)/(st.stdev(j)/(len(j)**0.5)),DF)
            pValueSup=1-sp.t.cdf((x_barra_sup-mi_power)/(st.stdev(j)/(len(j)**0.5)),DF)
            
            power_partial.append(pValueInf+pValueSup)
        
        power.append(power_partial)
    
        print('for supposed mi = '+str(i)+' against mi = 0, % times over limit for type 2 error: '+'{:.2%}\n'.format(sum((1-i)>beta for i in power_partial)/len(power_partial)))
    
    return power


def pooled_test(list_check_total, list_check_benchmark,alfa):
    
    # pathOutput='C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/box plots/'
    
    list_flat_total=[]
    list_flat_benchmark=[]
    
    for i in list_check_total[0]:
        for j in i:
            list_flat_total.append(j)
    
    for i in list_check_benchmark[0]:
        for j in i:
            list_flat_benchmark.append(j)
    
    plt.figure(1)
    plt.boxplot([list_flat_total,list_flat_benchmark])
    plt.xticks([1,2],['Tested Strategy', 'Stock'])
    
    plt.figure(2)
    plt.hist(list_flat_total,bins=int(len(list_flat_total)/20))
    plt.title('Strategy Distribution')
    
    plt.figure(3)
    plt.hist(list_flat_benchmark,bins=int(len(list_flat_benchmark)/20))
    plt.title('Stock Distribution')
    
    plt.figure(4)
    sp.probplot(list_flat_total,dist='norm',plot=pylab)
    plt.title('Quantile - quantile plot chosen Strategy')
    
    plt.figure(5)
    sp.probplot(list_flat_benchmark,dist='norm',plot=pylab)
    plt.title('Quantile - quantile plot benchmark')
    
    n1=len(list_flat_total)
    n2=len(list_flat_benchmark)
    
    std1=st.stdev(list_flat_total)
    std2=st.stdev(list_flat_benchmark)
    
    mean1=st.mean(list_flat_total)
    mean2=st.mean(list_flat_benchmark)
    
    sPooled=(((n1-1)*std1+(n2-1)*std2)/(n1+n2-2))**(0.5)
        
    SE=sPooled*((1/n1+1/n2)**0.5)
    
    DF=n1+n2-2
    
    TAlfaOver2=sp.t.ppf(1-alfa/2,DF)
    
    mean_upper=mean1-mean2+TAlfaOver2*SE
    mean_inferior=mean1-mean2-TAlfaOver2*SE
    
    tScore=(mean1-mean2)/SE
    
    pValue=2*(1 - sp.t.cdf(abs(tScore), DF)) # making times two because it is a double tailed problem
    
    print('\n probability of occuring under H0 : '+'{:.2%}'.format(pValue))
    print('\n the mean range is : '+str(round(mean_inferior))+' to '+str(round(mean_upper))+'\n')
    
    return list_flat_total,list_flat_benchmark,TAlfaOver2,mean_inferior,mean_upper,tScore,pValue

def unpooled_test(list_check_total, list_check_benchmark,alfa):
    
    pathOutput='C:/Users/chris/OneDrive/Documentos/GitHub/tatu-re/Welch test/'
    
    list_flat_total=[]
    list_flat_benchmark=[]
    
    for i in list_check_total[0]:
        for j in i:
            list_flat_total.append(j)
    
    for i in list_check_benchmark[0]:
        for j in i:
            list_flat_benchmark.append(j)
    
    plt.figure(1)
    plt.boxplot([list_flat_total,list_flat_benchmark])
    plt.xticks([1,2],['Tested Strategy', 'Stock'])
    plt.title('Distribution AUC of each week in year')
    plt.savefig(pathOutput+'box plot.png')
    plt.close()
    
    plt.figure(2)
    plt.hist(list_flat_total,bins=int(len(list_flat_total)/20))
    plt.title('Strategy Distribution')
    plt.savefig(pathOutput+'bar chart strategy.png')
    plt.close()
    
    plt.figure(3)
    plt.hist(list_flat_benchmark,bins=int(len(list_flat_benchmark)/20))
    plt.title('Stock Distribution')
    plt.savefig(pathOutput+'bar chart stock.png')
    plt.close()
    
    plt.figure(4)
    sp.probplot(list_flat_total,dist='norm',plot=pylab)
    plt.title('Quantile - quantile plot chosen Strategy')
    plt.savefig(pathOutput+'qq chart strategy.png')
    plt.close()
    
    plt.figure(5)
    sp.probplot(list_flat_benchmark,dist='norm',plot=pylab)
    plt.title('Quantile - quantile plot benchmark')
    plt.savefig(pathOutput+'qq benchmark.png')
    plt.close()
    
    n1=len(list_flat_total)
    n2=len(list_flat_benchmark)
    
    std1=st.stdev(list_flat_total)
    std2=st.stdev(list_flat_benchmark)
    
    mean1=st.mean(list_flat_total)
    mean2=st.mean(list_flat_benchmark)
    
    SE=(((std1**2)/n1)+((std2**2)/n2))**0.5
    
    DF=(((std1**2)/n1 + (std2**2)/n2)**2) / ((1/(n1-1)*((std1**2)/n1)**2) + (1/(n2-1)*((std2**2)/n2)**2))
    
    TAlfaOver2=sp.t.ppf(1-alfa/2,DF)
    
    mean_upper=mean1-mean2+TAlfaOver2*SE
    mean_inferior=mean1-mean2-TAlfaOver2*SE
    
    tScore=(mean1-mean2)/SE
    pValue=2*(1 - sp.t.cdf(abs(tScore), DF))
    
    print('\n probability of occuring under H0 : '+'{:.2%}'.format(pValue))
    print('\n the mean range is : '+str(round(mean_inferior,2))+' to '+str(round(mean_upper,2))+'\n')
    
    return list_flat_total,list_flat_benchmark,TAlfaOver2,mean_inferior,mean_upper,tScore,pValue
