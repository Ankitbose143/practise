#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.pipeline import Pipeline
from numpy import sum as arraysum
from numpy import sqrt,pi
from scipy import stats
import matplotlib.pyplot as plt
import datetime as datetime
from pandas import ExcelWriter
from datetime import date
from statistics import mean
import math
from datetime import timedelta


# In[2]:


def poly_regression(x_train,y_train,x_test,degree,get_plot=False):
    """
    This function returns predicted values based on nth degree polynomial eqn

    Parameters
    ----------
    x_train : TYPE
        DESCRIPTION.
    y_train : TYPE
        DESCRIPTION.
    degree : TYPE, optional
        DESCRIPTION. The default is 4.
    get_plot : TYPE, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    poly_pred : TYPE
        DESCRIPTION.

    """
    Input=[('polynomial',PolynomialFeatures(degree=degree)),('modal',LinearRegression())]
    pipe=Pipeline(Input)
    #pipe.fit(x_train,y_train)
    pipe.fit(x_train,y_train)

    poly_pred=pipe.predict(x_test)
    all_pred=pipe.predict(x_train)

    if get_plot:
        #plot
        plt.scatter(x_train,y_train)
        plt.plot(x_train,pipe.predict(x_train),color='red')
        plt.xlabel('Days')
        plt.ylabel('Cases')
        plt.title('degree '+str(4))
        plt.grid()
        plt.show()

    poly_pred=[round(x) for pr in poly_pred for x in pr]
    return poly_pred,all_pred


def get_predictionInterval(predicted_data,actual_data):
    """

    Parameters
    ----------
    predicted_data : TYPE
        DESCRIPTION.
    test_data : TYPE
        DESCRIPTION.
    ci : TYPE, optional
        DESCRIPTION. The default is 0.95.

    Returns
    -------
    interval : TYPE
        DESCRIPTION.

    """
    actual_data=[round(x) for td in actual_data for x in td]
    predicted_data=[round(x) for td in predicted_data for x in td]

    actual_data=actual_data[-7:]
    predicted_data=predicted_data[-7:]

    sum_errs = arraysum((np.array(actual_data) - np.array(predicted_data))**2)
    stdev = int(sqrt(1/(len(actual_data)-1) * sum_errs))


    return round(stdev)

def get_prediction_interval(all_p1,y_new_train,xtest,list_flag=True):
	"""
	Get prediction interval for future predictions

	Parameters
	----------
	xtest : TYPE
		DESCRIPTION.

	Returns
	-------
	None.

	"""
	if list_flag:
		actual_data=[round(x) for td in y_new_train for x in td]
		predicted_data=[round(x) for td in all_p1 for x in td]
	else:
		actual_data=y_new_train
		predicted_data=all_p1
	
	days_count=len(actual_data)
	days=list(range(1,days_count+1))
	
	SSE_line = arraysum((np.array(actual_data) - np.array(predicted_data))**2)
	MSE = SSE_line/(len(actual_data)-2)
	
	t_quantiles=stats.t.ppf(1-0.025, len(actual_data)-2)
	
	SE_predict=sqrt(MSE)*sqrt(1+1/days_count+(mean(days)-xtest)**2/arraysum((np.array(days) - mean(days))**2))
	return(round(SE_predict))



def prepare_train_test(cases_data,n):
    #n=7
    #training data of all days excluding last n days
    x_train=np.array(cases_data['Index'].iloc[:-n]).reshape(-1,1)
    y_train=np.array(cases_data['Total Positive Cases'].iloc[:-n]).reshape(-1,1)

    # last n days as test data
    x_test=np.array(cases_data['Index'].iloc[-n:]).reshape(-1,1)
    y_test=np.array(cases_data['Total Positive Cases'].iloc[-n:]).reshape(-1,1)
    return x_train,y_train,x_test,y_test

def Check_degree(x_train,y_train,x_test,y_test):
    total1=[]
    for degree in (2,3,4,5):
        pred,all_p=poly_regression(x_train,y_train,x_test,degree,False)
        #interval=get_predictionInterval(pred,y_test)
        #lower_limit=list(pred-interval)
        #upper_limit=list(pred+interval)
        pred = [int(x) for x in pred]
        y_test1=y_test.tolist()
        y1=[y for x in y_test1 for y in x]
        y3=[]
        for i in range(0,7):
            if(y1[i]!=0):
                y2=(pred[i]-y1[i])/y1[i]
                y3.append(round(y2,2))
            else:
                y2=0
                y3.append(y2)
        y3[4:7]=[x * 0.2 for x in y3[4:7]]
        y3[0:4]=[x * 0.1 for x in y3[0:4]]
        total=0
        for ele in range(0, len(y3)):
            total = total + abs(y3[ele]) 
        #print(total)
        total1.append(total)
        indx=total1.index(min(total1))
        degree=indx+2
    # if(total1[0]<total1[1]):
    #     #print('Degree 3 is selected')
    #     degree=3
    # else:
    #     #print('Degree 4')
    #     degree=4
    return(degree)


def prepare_new_train_test(cases_data1):
    x_train1=np.array(cases_data1['Index']).reshape(-1,1)
    y_train1=np.array(cases_data1['Total Positive Cases']).reshape(-1,1)
    x_test1=np.array(range(len(cases_data1['Index'])+1,len(cases_data1['Index'])+15)).reshape(-1,1)
    return(x_train1,y_train1,x_test1)



def get_std(arr1,arr2):
    sum_errs = arraysum((np.array(arr1) - np.array(arr2))**2)
    stdev = int(sqrt(1/(len(arr1)-1) * sum_errs))

    return(stdev)

def cumulative(cases_data_df):
    cumulative_data_df = []
    for cd in cases_data_df:
        cd['Cumulative'] = cd['Predicted'].cumsum()
        #cd = cd[['Date', 'District', 'Cum_Positive_Cases','Composite_Predicted','Cumulative']]
        #print(cd['District'])
        actual_state=[l.tolist() for l in cd['Actuals - Deceased'].iloc[:-14].astype(int).values]
        pred_state=[l.tolist() for l in cd['Cumulative'].iloc[:-14].values]

        cd['lower_bound_1_cumulative_deceased'] = ''
        cd['upper_bound_1_cumulative_deceased'] = ''
        cd['lower_bound_2_cumulative_deceased'] = ''
        cd['upper_bound_2_cumulative_deceased'] = ''

        for i in range(len(cd['Actuals - Deceased'])):
            day_number=i+1
            std=get_prediction_interval(pred_state,actual_state,day_number,False)
            cd['lower_bound_1_cumulative_deceased'].iloc[i]=max(0,cd['Cumulative'].iloc[i]-std)
            cd['upper_bound_1_cumulative_deceased'].iloc[i]=max(0,cd['Cumulative'].iloc[i]+std)
            cd['lower_bound_2_cumulative_deceased'].iloc[i]=max(0,cd['Cumulative'].iloc[i]-2*std)
            cd['upper_bound_2_cumulative_deceased'].iloc[i]=max(0,cd['Cumulative'].iloc[i]+2*std)

        cumulative_data_df.append(cd)
        
    return cumulative_data_df


# In[3]:

def read_rawdata_inp():
    Raw_Data= pd.read_excel('District Wise data_31_July.xlsx',sheet_name='District wise Cases')
    state_data=pd.read_excel('District Wise data_31_July.xlsx',sheet_name='State wise')

    Districts=['Mumbai','Thane','Pune','Nashik','Nagpur','Ahmednagar','Solapur','Jalgaon',
        'Aurangabad','Satara','Raigad','Palghar','Akola','Amravati','Beed','Bhandara',
        'Buldhana','Chandrapur','Dhule','Gadchiroli','Gondia','Hingoli','Jalna',
        'Kolhapur','Latur','Nanded','Nandurbar','Osmanabad','Parbhani','Ratnagiri','Sangli',
        'Sindhudurg','Wardha','Washim','Yavatmal'] # 'Maharashtra'

    Raw_Data = Raw_Data.rename(columns = {'Total Positive Cases':'Positive Cases'})
    num_test_records=7
    cases_data_df=[]
    for district in Districts:
        cases_data=Raw_Data[Raw_Data['District']==district]
        cases_data.reset_index(drop=True,inplace=True)
        cases_data.sort_values(by='Date',inplace=True)
        cases_data1=pd.DataFrame(cases_data[['Deceased','Positive Cases']])
        cases_data1.rename(columns={'Deceased':'Total Positive Cases'},inplace=True)
        cases_data['Actuals - Deceased'] = cases_data['Deceased']
        cases_data.rename(columns={'Deceased':'Total Positive Cases'},inplace=True)
        
        ##daily cases part
        cases_data['Daily']=''
        cases_data['Daily'].iloc[0]=0

        for n in range(1,len(cases_data)):
            cases_data['Daily'].iloc[n]=cases_data['Total Positive Cases'].iloc[n]-cases_data['Total Positive Cases'].iloc[n-1]

        cases_data=cases_data.drop('Total Positive Cases',1)
        #print(cases_data)
        cases_data.rename(columns={'Daily':'Total Positive Cases'},inplace=True)
        ##
        cases_data1=pd.DataFrame(cases_data['Total Positive Cases'])

        cases_data1['Index']=range(1,len(cases_data1)+1)
        x_train,y_train,x_test,y_test=prepare_train_test(cases_data1,num_test_records)
        Final_degree=Check_degree(x_train,y_train,x_test,y_test)
        # print('Final_degree_Selected ' +str(Final_degree) + ' for the district ' + district)

        x_new_train,y_new_train,x_new_test=prepare_new_train_test(cases_data1)
        pred1,all_p1=poly_regression(x_new_train,y_new_train,x_new_test,Final_degree,False)

        # while sum([1 for x in pred1 if x < 0]):
        #     Final_degree -= 1
        #     pred1,all_p1=poly_regression(x_new_train,y_new_train,x_new_test,Final_degree,False)
        # print('Final_degree_Selected ' +str(Final_degree) + ' for the district ' + district)
            

        sd=get_predictionInterval(all_p1,y_new_train)
        cases_data=cases_data[['Date','District','Actuals - Deceased','Total Positive Cases']]
        cases_data.reset_index(inplace=True,drop=True)
        cases_data['Predicted']=all_p1

        cases_data['Predicted'].values[cases_data['Predicted']<0]=0
        cases_data['Predicted']=round(cases_data['Predicted'])

        cases_data['lower_bound_1_daily_deceased']=''
        cases_data['upper_bound_1_daily_deceased']=''
        cases_data['lower_bound_2_daily_deceased']=''
        cases_data['upper_bound_2_daily_deceased']=''
        
        ## sd for predicted till date
        i=0
        for i in range(7,len(cases_data['Actuals - Deceased'])):
            act1=cases_data['Total Positive Cases'].iloc[i-7:i]
            prd1=cases_data['Predicted'].iloc[i-7:i]
            std=get_std(act1,prd1)
            cases_data['lower_bound_1_daily_deceased'].iloc[i]=max(0,cases_data['Predicted'].iloc[i]-std)
            cases_data['upper_bound_1_daily_deceased'].iloc[i]=max(0,cases_data['Predicted'].iloc[i]+std)
            cases_data['lower_bound_2_daily_deceased'].iloc[i]=max(0,cases_data['Predicted'].iloc[i]-2*std)
            cases_data['upper_bound_2_daily_deceased'].iloc[i]=max(0,cases_data['Predicted'].iloc[i]+2*std)

        i=0
        for i in range(1,len(x_new_test)+1):
            Date1=cases_data['Date'].iloc[-1]+datetime.timedelta(days=1)
            pred2=pred1[i-1]
            new_row = {'Date':Date1,'District':district, 'Predicted':int(pred2), 'lower_bound_1_daily_deceased':int(pred2)-sd,'upper_bound_1_daily_deceased':int(pred2)+sd, 'lower_bound_2_daily_deceased':int(pred2)-2*sd,'upper_bound_2_daily_deceased':int(pred2)+2*sd}
            cases_data = cases_data.append(new_row, ignore_index=True)
            cases_data['Predicted']=cases_data['Predicted'].astype('int')
            
        cases_data_df.append(cases_data)

    state_data['District']='Maharashtra'
    state_data.rename(columns={'Row Labels':'Date'},inplace=True)
    state_data['Cum_Positive_Cases'] = state_data['Sum of Deceased']
    state_data.rename(columns={'Sum of Deceased':'Total Positive Cases'},inplace=True)
    state_data=state_data[['Date','District','Total Positive Cases','Cum_Positive_Cases']]
    state_data['Daily']=0
    state_data['Sum_dist_cases']=0
    state_data['lower_bound_1_daily_deceased']=''
    state_data['upper_bound_1_daily_deceased']=''
    state_data['lower_bound_2_daily_deceased']=''
    state_data['upper_bound_2_daily_deceased']=''
    state_data['Sum_dist_cases']=0

    state_data['Daily']=''
    state_data['Daily'].iloc[0]=0

    for n in range(1,len(state_data)):
        state_data['Daily'].iloc[n]=state_data['Total Positive Cases'].iloc[n]-state_data['Total Positive Cases'].iloc[n-1]

    state_data=state_data.drop('Total Positive Cases',1)
    state_data.rename(columns={'Daily':'Total Positive Cases'},inplace=True)


    def add_years(d, years):
            return d.replace(year = d.year + years)

    for i in range(0,len(state_data)):
        try:
            a=datetime.datetime.strptime(state_data['Date'].iloc[i], '%d-%b')
            a=add_years(a,120)
            state_data['Date'].iloc[i]=a
        except:
            pass

    i=0
    for i in range(1,len(x_new_test)+1):
        Date1=state_data['Date'].iloc[-1]+datetime.timedelta(days=1)
        new_row = {'Date':Date1}
        state_data = state_data.append(new_row, ignore_index=True)
            #state_data['Predicted']=state_data['Predicted'].astype('int')


    state_dates=state_data['Date'].values
    type(state_dates)
    state_dates1=state_dates[-14:]


    # sdate=state_dates[0]
    # print(sdate)
    # ts = pd.DatetimeIndex([sdate])[0] 
    # dt64 = np.datetime64(sdate) 
    # print(dt64)
    # print(type(dt64))
    k=0
    sum_cases=[]
    for sdate in state_dates:
        sdate1 = np.datetime64(sdate)
        forecast=0
        for data in cases_data_df[0:]:
            if sdate1 in data['Date'].values:
                pred_val=data[data['Date']==sdate1]['Predicted'].iloc[0]
                forecast=forecast+pred_val
        sum_cases.append(forecast)

    state_data['Sum_dist_cases']=sum_cases

    state_data['District']='Maharashtra'


    state_data.loc[state_data['Total Positive Cases']==0,'Sum_dist_cases']=0

    # actual_state=[l.tolist() for l in state_data['Total Positive Cases'].iloc[:-14].astype(int).values]
    # pred_state=[l.tolist() for l in state_data['Sum_dist_cases'].iloc[:-14].values]

    act1=state_data['Total Positive Cases'].iloc[i-7:i]
    prd1=state_data['Sum_dist_cases'].iloc[i-7:i]

    for i in range(len(state_data['Total Positive Cases'])):
        day_number=i+1
        #std=get_prediction_interval(pred_state,actual_state,day_number)
        std=get_std(act1,prd1)
        state_data['lower_bound_1_daily_deceased'].iloc[i]=max(0,state_data['Sum_dist_cases'].iloc[i]-std)
        state_data['upper_bound_1_daily_deceased'].iloc[i]=max(0,state_data['Sum_dist_cases'].iloc[i]+std)
        state_data['lower_bound_2_daily_deceased'].iloc[i]=max(0,state_data['Sum_dist_cases'].iloc[i]-2*std)
        state_data['upper_bound_2_daily_deceased'].iloc[i]=max(0,state_data['Sum_dist_cases'].iloc[i]+2*std)

    state_data = state_data.rename(columns={'Sum_dist_cases':'Predicted','Cum_Positive_Cases':'Actuals - Deceased'})
    state_data['District'] = 'Maharashtra'

    cases_data_df.append(state_data)

    cumulative_data_df = []
    output = cumulative(cases_data_df=cases_data_df)

    with ExcelWriter('Output/Districts_forecast_Deceased_'+str(date.today())+'.xlsx') as writer:
            for cd in cases_data_df:
                cd.to_excel(writer,cd.District[0],index=False)
            writer.save()
    return cases_data_df

# read_rawdata_inp()
