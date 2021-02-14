# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:34:58 2019

@author: Yannick
"""

import gc
import pandas as pd
import numpy as np
import pandas as pd
#import lightgbm as lgb
#import xgboost as xgb
from scipy.sparse import vstack, csr_matrix, save_npz, load_npz
import gc
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('C:/Users/Yannick/Documents/Business Analytics/Data Mining/Assignment2')

gc.enable()
#%%
# variable types & measurement level (boolean, nominal, ordinal, interval/ratio), missing values, comments
# VALUES ARE BASED ON TRAINING SET!!
dtypes = {'srch_id': 'int32' # id variable, 0% missing
        , 'site_id':'int32' # nominal, 0% missing
        , 'visitor_location_country_id' : 'int32' # nominal, 0% missing
        , 'visitor_hist_starrating' :'float16' # interval/ratio, 94.9% missing
        , 'visitor_hist_adr_usd' : 'float16' # interval/ratio, 94.9% missing
        , 'prop_country_id' : 'int32' # nominal, 0% missing
        , 'prop_id' : 'int32' # nominal, 0% missing, TARGET
        , 'prop_starrating' : 'int8' # ordinal, 0% missing, 0 no stars due to unknown so maybe recode
        , 'prop_review_score' : 'float16' # ordinal, 0.15% missing, 0 means no reviews/unavaillable so maybe recode
        , 'prop_brand_bool': 'int8' # boolean, 0% missing
        ,'prop_location_score1' :'float16' # interval/ratio, 0% missing
        , 'prop_location_score2' : 'float16' #interval/ratio, 22% missing
        ,'prop_log_historical_price' : 'float16' #interval/ratio (scaled by log), 0% missing
        , 'position': 'int16' # interval (discrete), 0% missing, (not availlable in test)
        , 'price_usd' : 'float32' # interval/ratio, 0% missing
        , 'promotion_flag': 'int8' # boolean, 0% missing
        ,'srch_destination_id' : 'int32' #nominal, 0% missing, maybe compare with prop_country_id?
        , 'srch_length_of_stay' : 'int16' # interval (discrete), 0% missing
        , 'srch_booking_window': 'int16' # interval (discrete), 0% missing
        ,'srch_adults_count': 'int16' # interval (discrete), 0% missing
        , 'srch_children_count': 'int16' # interval (discrete), 0% missing
        , 'srch_room_count': 'int16' # interval (discrete), 0% missing
        ,'srch_saturday_night_bool':'int8' #boolean, 0% missing
        , 'srch_query_affinity_score' : 'float32' # interval/ratio, 93.6% missing
        ,'orig_destination_distance' : 'float32' # interval/ratio ,32.4%
        , 'random_bool':'int8' # boolean, 0% missing
        , 'comp1_rate': 'float16' # ordinal (kind of),97.6% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp1_inv' : 'float16' # ordinal (kind of), 97.4% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp1_rate_percent_diff' : 'float64' # ratio, 98% missing
        , 'comp2_rate' : 'float16' # ordinal (kind of),59.2% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp2_inv' : 'float16'  # ordinal (kind of),57.0% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp2_rate_percent_diff' : 'float64' # ratio, 88.8% missing
        , 'comp3_rate' : 'float16'  # ordinal (kind of),69.1% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp3_inv' : 'float16'  # ordinal (kind of),66.7% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp3_rate_percent_diff' : 'float64' # ratio, 90.5% missing
        , 'comp4_rate' : 'float16'  # ordinal (kind of),93.8% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp4_inv' : 'float16'  # ordinal (kind of),93.1% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp4_rate_percent_diff' : 'float64' # ratio, 97.4% missing,
        , 'comp5_rate' : 'float16'  # ordinal (kind of),97.6% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp5_inv' : 'float16'  # ordinal (kind of),97.6% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp5_rate_percent_diff' : 'float64' # ratio, 83.0% missing
        , 'comp6_rate' : 'float16'  # ordinal (kind of),95.2% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp6_inv' : 'float16'  # ordinal (kind of),94.7% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp6_rate_percent_diff' : 'float64' #ratio, 98.1% missing
        , 'comp7_rate': 'float16'  # ordinal (kind of),93.6% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp7_inv': 'float16'  # ordinal (kind of),92.8% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp7_rate_percent_diff' : 'float64' # ratio, 97.2% missing
        , 'comp8_rate' : 'float16'  # ordinal (kind of),61.3% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'comp8_inv' : 'float16'  # ordinal (kind of),59.9% missing, 0 means no data availlable & is an int with nan values so convert later
        ,'comp8_rate_percent_diff' : 'float64'  # ordinal (kind of),87.6% missing, 0 means no data availlable & is an int with nan values so convert later
        , 'click_bool' : 'int8' #boolean, 0% missing, TARGET
        , 'gross_bookings_usd' : 'float32' #interval/ratio, 0% missing TARGET
        ,'booking_bool' : 'int8', #boolean, 0% missing, TARGET
}

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
parse_dates = ['date_time']
#print('Download Train and Test Data.\n')
train = pd.read_csv('training_set_VU_DM.csv', dtype=dtypes,parse_dates=parse_dates, low_memory=True)
test =pd.read_csv('test_set_VU_DM.csv', dtype=dtypes,parse_dates=parse_dates, low_memory=True)
gc.collect()

train.to_pickle("./train_pickle.pkl")
test.to_pickle("./test_pickle.pkl")

#%%
train = pd.read_pickle("./train_pickle.pkl")
test =  pd.read_pickle("./test_pickle.pkl")

#%%
def markBoolean(x,value):
    if x == 1:
        return value
    return 0

def substitute_y_for_z(x,y,z):
    if x == y:
        return z
    return x

train['booking_bool_help'] = train['booking_bool'].apply(lambda x: markBoolean(x,5))
train['relevance_grades']= train['booking_bool_help'] + train['click_bool'] 
train['relevance_grades'] = train['relevance_grades'].apply(lambda x: substitute_y_for_z(x,6,5))

def aboveFiveToZero(x, points = False):
    k = 5
    if x > k:
        return 0
    else:
        if points:
            return 2*x
        else:
            return x
        
train['position_rank'] = train.groupby("srch_id")["position"].rank("first", ascending=True)
train['position_rank'] = train['position_rank'].apply(lambda x:aboveFiveToZero(x))
train['position_rank'] = train.groupby("srch_id")["position_rank"].rank("first", ascending=False)
train['position_rank'] = train['position_rank'].apply(lambda x:aboveFiveToZero(x, True))

train['month'] = train['date_time'].dt.month
test['month'] = test['date_time'].dt.month

train['weekday'] = train['date_time'].dt.weekday
test['weekday'] = test['date_time'].dt.weekday

train['comptotal_rate'] = train[['comp1_rate', 'comp2_rate', 'comp3_rate', 'comp4_rate', 'comp5_rate', 'comp6_rate', 'comp7_rate', 'comp8_rate']].mean(axis=1) 
test['comptotal_rate'] = test[['comp1_rate', 'comp2_rate', 'comp3_rate', 'comp4_rate', 'comp5_rate', 'comp6_rate', 'comp7_rate', 'comp8_rate']].mean(axis=1) 

train['price_usd_position'] = train.groupby("srch_id")["price_usd"].rank("first", ascending=False)
train['price/prop_starrating'] = train['price_usd'] / train['prop_starrating']

test['price_usd_position'] = test.groupby("srch_id")["price_usd"].rank("first", ascending=False)
test['price/prop_starrating'] = test['price_usd'] / test['prop_starrating']

import holidays

#avgprice_propID = pd.DataFrame(train.groupby('prop_id')['price_usd'].mean(), index=train['prop_id'].unique())
#avgprice_propID = avgprice_propID[~avgprice_propID.index.duplicated(keep='first')]
#avgprice_propID = avgprice_propID['price_usd'].rename('Avg_price_propID')
#
#train = pd.merge(train, avgprice_propID, left_on = 'prop_id', right_on = avgprice_propID.index)

train['Avg_price_propID'] = train['price_usd'].groupby(train['prop_id']).transform('mean')
train['Std_price_propID'] = train['price_usd'].groupby(train['prop_id']).transform('std')
train['diff_price_with_avg'] = train['Avg_price_propID'] - train['price_usd']

test['Avg_price_propID'] = test['price_usd'].groupby(test['prop_id']).transform('mean')
test['Std_price_propID'] = test['price_usd'].groupby(test['prop_id']).transform('std')
test['diff_price_with_avg'] = test['Avg_price_propID'] - test['price_usd']

train['Avg_price_srchID'] = train['price_usd'].groupby(train['srch_id']).transform('mean')
train['Avg_price_srch_destinationID'] = train['price_usd'].groupby(train['srch_destination_id']).transform('mean')

test['Avg_price_srchID'] = test['price_usd'].groupby(test['srch_id']).transform('mean')
test['Avg_price_srch_destinationID'] = test['price_usd'].groupby(test['srch_destination_id']).transform('mean')



#train['diff_with_avg_relgrade'] = train['relevance_grades'] - train['Avg_relgrade_propID']


#train['relevance_grades_y'].rename('Avg_rel_grade_propID')



del train['booking_bool_help']


#%%
def correlationplot(df):
    import seaborn as sns
    corr = df.corr(method='pearson')
    sns.heatmap(corr, 
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values, annot = True, fmt = '.2f')  
    
def frequencyplot(df, x, y):
    pd.crosstab(df[x], df[y]).plot(kind='bar')
    plt.title('{0} Frequency for {1}'.format(y.title(), x.title()))
    plt.xlabel('{0}'.format(x.title()))
    plt.xticks(rotation=45)
    plt.ylabel('Frequency of {0}'.format(y.title()))  
    plt.show()
    
def densityplot(df, x, y):
    for i in sample_train[y].unique():
        # Subset to the airline
        subset = sample_train[sample_train[y] == i]
    
        # Draw the density plot
        sns.distplot(subset[x], hist = False, kde = True,
                     kde_kws = {'linewidth': 3},
                     label = i)
    
        # Plot formatting
        plt.legend(prop={'size': 16}, title = y.title())
        plt.title('Density Plot with %s'%y.title())
        plt.xlabel('%s'%x.title())
        plt.ylabel('Density')
        
#%%
#Descriptive statistics    
cols = test.columns.tolist()
missing_values_df = pd.DataFrame(columns=['column','number of missing values (train)','percentage (train)'
                                         ,'number of missing values (test)','percentage (test)'])
for col in cols:
    row = {'column':col
            ,'number of missing values (train)':train[col].isnull().sum()
            ,'percentage (train)':train[col].isnull().sum()*100 / len(train)
            ,'number of missing values (test)':test[col].isnull().sum()
            ,'percentage (test)':test[col].isnull().sum()*100 / len(test)}
    missing_values_df = missing_values_df.append(row,ignore_index=True)
print(missing_values_df)
del row, col
gc.collect()


from scipy import stats

skipcols= ['site_id','srch_id','date_time','visitor_location_country_id','prop_country_id','prop_id','srch_destination_id']
summary_df = pd.DataFrame(index=['count','mean','std','min','25%','50%','75%','max','median','kurtosis','skewness','missing_values','percentage_missing_values'])
for usecol in train.columns.tolist():
    if usecol in skipcols:
        continue
    train_filtered = train[usecol].dropna(axis=0)
    desc = stats.describe(train_filtered)
    add_descriptives = train_filtered.describe(include ='all').to_frame()
    add_descriptives.loc['mean'] = np.mean(train_filtered.tolist())
    add_descriptives.loc['median'] = train_filtered.median()
    add_descriptives.loc['kurtosis'] = desc.kurtosis
    add_descriptives.loc['skewness'] = desc.skewness
    add_descriptives.loc['missing_values'] = train[usecol].isna().sum()
    add_descriptives.loc['percentage_missing_values'] = (train[usecol].isna().sum()*100) /len(train[usecol])
    summary_df =summary_df.merge(add_descriptives,left_index=True,right_index=True)

print(np.round(summary_df, decimals=2))

del skipcols,add_descriptives,desc,train_filtered
gc.collect()

#%%
print(pd.crosstab(train['booking_bool'] ,train['click_bool']))
print(pd.crosstab(train['random_bool'] ,train['click_bool']))


sns.set(rc={'figure.figsize':(3,3)})

sns.set(style="whitegrid")
ax = sns.boxplot(x= train['booking_bool'], y=train['position'])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax.axes.set_title("booking bool vs. position",fontsize=35)
ax.set_xlabel("booking bool",fontsize=30)
ax.set_ylabel("position",fontsize=20)
plt.show()

plt.clf()
plt.close()

sns.set(rc={'figure.figsize':(5,4)})

sns.set(style="whitegrid")
ax = sns.boxplot(x= train['click_bool'], y=train['position'])
ax.set_xticklabels(ax.get_xticklabels(),rotation=45)
ax.axes.set_title("click bool vs. position",fontsize=35)
ax.set_xlabel("click bool",fontsize=30)
ax.set_ylabel("position",fontsize=20)

plt.show()

plt.clf()
plt.close()


import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (24,12)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

cols = ['visitor_hist_starrating','visitor_hist_adr_usd', 'prop_starrating','prop_review_score','prop_location_score1'
,'prop_location_score2','prop_log_historical_price','position','price_usd','srch_length_of_stay','srch_booking_window'
,'srch_adults_count','srch_children_count','srch_room_count','srch_query_affinity_score','orig_destination_distance'
,'comp1_rate_percent_diff','comp2_rate_percent_diff'
,'comp3_rate_percent_diff','comp4_rate_percent_diff'
,'comp5_rate_percent_diff','comp6_rate_percent_diff'
,'comp7_rate_percent_diff','comp8_rate_percent_diff','gross_bookings_usd']


corr = train[cols].corr(method='pearson')

fig, ax = plt.subplots()
sns.set(font_scale=1.5)
ax.set_xticklabels(labels = corr.columns.values,rotation=90)
sns.heatmap(corr, 
            yticklabels=corr.columns.values, ax=ax,annot = True, fmt = '.2f'
           , vmin=-1, vmax=1)
ax.tick_params(labelsize=25)




plt.rcParams['figure.figsize'] = (11,6)
sns.set(style="white")
sns.set(style="whitegrid", color_codes=True)

cols = [
'comp1_rate_percent_diff','comp2_rate_percent_diff'
,'comp3_rate_percent_diff','comp4_rate_percent_diff'
,'comp5_rate_percent_diff','comp6_rate_percent_diff'
,'comp7_rate_percent_diff','comp8_rate_percent_diff','gross_bookings_usd']
corr = train[cols].corr(method='pearson')

fig, ax = plt.subplots()
ax.set_xticklabels(labels = corr.columns.values,rotation=90)
sns.set(font_scale=1.8)
sns.heatmap(corr,     
            yticklabels=corr.columns.values, ax=ax,annot = True, fmt = '.2f'
           , vmin=-1, vmax=1)
ax.tick_params(labelsize=25)


#Correlations with relevance_grades:
#correlationplot(sample_train.iloc[:,np.r_[0:10, -1]])
# Position -0.16
# random_bool -0.07
# promotion_flag 0.04
# prop_location_score2 0.07
# srch_query_affinity_score 0.03
# prop_review_score 0.03
# comp8_rate 0.03


#Correlations with position (look only at random_bool == 0)
#correlationplot(train.iloc[:,np.r_[0:10, 14]])
# prop_starrating -0.13
# prop_location_score2 -0.20
# promotion_flag -0.14
# srch_query_affinity_score -0.10
# prop_review_score -0.08
# comptotal_rate -0.04
# srch_room_count -0.03
# site_id = -0.03
# prop_country_id 0.03


gc.collect()

#%%
#CHOOSE FEATURES AND CONSTRUCT X_TRAIN, Y_TRAIN AND X_TEST
from random import sample 
import random
random.seed(1)

user_list = list(train['srch_id'].unique())
sample_list = sample(user_list,round(len(user_list) * 1))
sample_train = train[train['srch_id'].isin(sample_list)]
sample_train
#sample_train = train.sample(n=300000)
#print(sample_train)

del user_list,sample_list
           
idlist = ['srch_id','prop_id']
catvars = ['random_bool', 'promotion_flag', 'site_id', 'prop_country_id', 'visitor_location_country_id',
           'prop_brand_bool', 'srch_destination_id', 'srch_saturday_night_bool']
numvars = ['prop_location_score2', 'srch_query_affinity_score', 'prop_review_score',
           'prop_log_historical_price', 'srch_length_of_stay', 'srch_booking_window', 'price_usd',
           'price_usd_position', 'price/prop_starrating',
           'comp1_rate', 'comp2_rate', 'comp3_rate', 'comp4_rate', 'comp5_rate', 'comp6_rate',
           'comp7_rate', 'comp8_rate', 'comp1_rate_percent_diff', 'comp2_rate_percent_diff',
           'comp3_rate_percent_diff', 'comp4_rate_percent_diff', 'comp5_rate_percent_diff',
           'comp6_rate_percent_diff', 'comp7_rate_percent_diff', 'comp8_rate_percent_diff',
           'Avg_price_propID', 'Avg_price_srchID', 'Avg_price_srch_destinationID', 'Std_price_propID', 'srch_adults_count',
           'position_rank_est', 'srch_children_count','srch_room_count']

targetlist = ['relevance_grades']

sample_train_XY = sample_train[idlist + catvars  + numvars + targetlist]

test_processed = test[idlist + catvars]

test_processed[numvars] = test[numvars]

max_prop_starrating_train = sample_train.loc[sample_train['price/prop_starrating'] != np.inf, 'price/prop_starrating'].max()
max_prop_starrating_test = test.loc[test['price/prop_starrating'] != np.inf, 'price/prop_starrating'].max()

#For now, mark all missing values with an apparent different value
for f in numvars:
    if f == 'price/prop_starrating':
        from math import inf
        sample_train_XY[f]=sample_train_XY[f].fillna(0)
        sample_train_XY[sample_train_XY[f] == inf][f] = max_prop_starrating_train
        
        test_processed[f]=test_processed[f].fillna(0)
        test_processed[test_processed[f] == inf][f] = max_prop_starrating_test
        
    sample_train_XY[f]=sample_train_XY[f].fillna(-1)
    test_processed[f]=test_processed[f].fillna(-1)
    

#from sklearn import preprocessing
#scaler = preprocessing.StandardScaler()
#sample_train_XY[numvars] = scaler.fit_transform(sample_train_XY[numvars])  
#test_processed[numvars] = scaler.fit_transform(test_processed[numvars])  

sample_train_XY[targetlist] = sample_train[targetlist]

test_processed = test_processed.reset_index()

X_train = sample_train_XY[idlist + catvars + numvars]
#X_train = X_train.set_index(idlist)
Y_train = sample_train_XY[idlist + targetlist]
#Y_train = Y_train.set_index(idlist)
X_test = test_processed[idlist + catvars + numvars]
#X_test = X_test.set_index(idlist)
del test_processed, sample_train_XY


#%%

#Split training and validation from prior splitted training data, default is at 70%
def splitTrainToTrainAndVal(training_data_X,training_data_Y,perc = 0.7):
    user_list = list(training_data_X['srch_id'].unique())
    user_list_train = user_list[0:round(len(user_list)*perc)]
    user_list_val = user_list[round(len(user_list)*perc):len(user_list)]
    
    X_train = training_data_X[training_data_X['srch_id'].isin(user_list_train)]
    Y_train = training_data_Y[training_data_Y['srch_id'].isin(user_list_train)]
    X_val = training_data_X[training_data_X['srch_id'].isin(user_list_val)]       
    Y_val = training_data_Y[training_data_Y['srch_id'].isin(user_list_val)]
    
    return X_train,Y_train,X_val,Y_val

X_train,Y_train,X_val,Y_val = splitTrainToTrainAndVal(X_train,Y_train)
gc.collect()


#%%

def getGroupCounts(training_data,testing_data):    
    srch_id_count = training_data[['srch_id']]
    srch_id_count['count'] = 1
    groups_count_train = np.array(srch_id_count.groupby(['srch_id'],axis=0).count()['count'])
    
    srch_id_count = testing_data[['srch_id']]
    srch_id_count['count'] = 1
    groups_count_test = np.array(srch_id_count.groupby(['srch_id'],axis=0).count()['count'])
    
    return groups_count_train,groups_count_test
    #del X_test['prop_id']
groups_count_train,groups_count_val = getGroupCounts(X_train,X_val)

del Y_train['srch_id'],Y_train['prop_id']
del Y_val['srch_id'],Y_val['prop_id']

#%%
#BASE MODEL, TRAINING AND VALIDATION
import xgboost as xgb
params = {'objective': 'rank:ndcg',
        'eval_metric':'ndcg@5-',
        'max_depth': 6,
        #'max_delta_step':5,
        #'gamma':3,
        #'min_child_weight':5
        #'eta': 0.2
    #    'min_child_weight':3
        #'reg_alpha':[0,3,5],

        }

dtrain = xgb.DMatrix(data=X_train, label=Y_train)
dtrain.set_group(group=groups_count_train)

dval = xgb.DMatrix(data=X_val, label=Y_val)
dval.set_group(group=groups_count_val)
#dtrain.set_group(np.array(group_sizes))
evals_result = {}
watchlist = [(dval,'test'),(dtrain, 'train')]
model_XGB = xgb.train(params=params,dtrain=dtrain,early_stopping_rounds=5,num_boost_round=250,evals=watchlist,evals_result=evals_result)

import pickle
filename = 'XGB.sav'
pickle.dump(model_XGB, open(filename, 'wb'))


#pred = model_XGB.predict(dval)
#model = xgb.train(params={'objective': 'rank:ndcg'}, dtrain=dtrain, num_boost_round=10)
#XGB.fit(X_train, Y_train)
#pred_XGB = XGB.predict_proba(X_test)
#ROC_XGB = roc_auc_score(np.array(X_test), np.array(pred_XGB.T[1]))

#%%
#AFTER FITTING THE BASE MODEL, RETRAIN ON ALL TRAINING DATA IF WANTED (NOT NEEDED)

X_train = pd.concat([X_train,X_val])
Y_train = pd.concat([Y_train,Y_val])

def getGroupCounts(training_data):    
    srch_id_count = training_data[['srch_id']]
    srch_id_count['count'] = 1
    groups_count_train = np.array(srch_id_count.groupby(['srch_id'],axis=0).count()['count'])
    
    return groups_count_train
    #del X_test['prop_id']
groups_count_train = getGroupCounts(X_train)
del X_train,Y_train
import xgboost as xgb
params = {'objective': 'rank:ndcg',
        'eval_metric':'ndcg@5-',
        'max_depth': 4,
        #'max_delta_step':5,
        #'gamma':3,
        #'min_child_weight':5
        #'eta': 0.2
    #    'min_child_weight':3
        #'reg_alpha':[0,3,5],

        }

dtrain = xgb.DMatrix(data=X_train, label=Y_train)
dtrain.set_group(group=groups_count_train)

#dtrain.set_group(np.array(group_sizes))
evals_result = {}
#watchlist = [(dval,'test'),(dtrain, 'train')]
watchlist = [(dtrain, 'train')]
model_XGB = xgb.train(params=params,dtrain=dtrain,early_stopping_rounds=5,num_boost_round=500,evals=watchlist,evals_result=evals_result)




#%%
import pickle
filename = 'XGB.sav'
model_XGB = pickle.load(open(filename, 'rb'))


#pred = model_XGB.predict(dval)
#model = xgb.train(params={'objective': 'rank:ndcg'}, dtrain=dtrain, num_boost_round=10)
#XGB.fit(X_train, Y_train)
#pred_XGB = XGB.predict_proba(X_test)
#ROC_XGB = roc_auc_score(np.array(X_test), np.array(pred_XGB.T[1]))


#%%
#PREDICTING AND STORE IN FORMAT
dtest = xgb.DMatrix(data=X_test)

pred = model_XGB.predict(dtest)

def toint(x):
    return int(x)

def orderAndPrepareDF(pred_df):
    #outcome is such that it can be submitted at kaggle right away.
    #Preprocessing of testdata should be done beforehand, srch_id and prop_id should be set as index
    
    pred_df['prop_id'] = pred_df['prop_id'].apply(lambda x:toint(x))
    pred_df['srch_id'] = pred_df['srch_id'].apply(lambda x:toint(x))
    
    final_pred_df = pred_df.sort_values(by=['srch_id','prediction'], ascending=[True,False])
    #print(final_pred_df) #for those who don't believe the df is not sorted per search_id by the prediction
    final_pred_df = final_pred_df.reset_index()
    final_pred_df = final_pred_df.set_index(['srch_id'])
    del final_pred_df['prediction'],final_pred_df['index']
    
    return final_pred_df

def predToDF(pred,X_test):
    preddict = {}
    cols = X_test[['srch_id','prop_id']]
    preddict['srch_id']=cols['srch_id']
    preddict['prop_id']=cols['prop_id']
    preddict['prediction']= pred
    pred_df = pd.DataFrame(preddict)
      
    return pred_df

pred_df = predToDF(pred,X_test)

#%%
pred_df_final = orderAndPrepareDF(pred_df)

pred_df_final.to_csv('pred13.csv')

#%%

#RF TO PREDICT RELEVANCE_GRADE
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import ParameterSampler
from sklearn.metrics import roc_curve, roc_auc_score,precision_score

n_estimators = [i for i in range(1,1000,5)]
max_depth = [i for i in range(1,99,2)]
min_samples_split = [i for i in range(5,50,5)]
min_samples_leaf = [i for i in range(5,100,5)]
params_RF ={
            'n_estimators' : [3,4,5,6,7]
            ,'max_features' : [3]
            ,'max_depth' : [5,10]
            ,'min_samples_split': [5]
            ,'min_samples_leaf' : [1,3]
            ,'class_weight'  : [{0:.5,1:.5}]
         }


folds = 5
param_comb = 2

model_RF = RandomForestClassifier() 
skf_RF = StratifiedKFold(n_splits=folds)

grid_search_RF = RandomizedSearchCV(model_RF, n_iter=param_comb,param_distributions=params_RF,scoring='recall', n_jobs=10, cv=skf_RF)
grid_search_RF.fit(X_train, Y_train)

print('\n All results:')
print(grid_search_RF.cv_results_)
print('\n Best estimator:')
print(grid_search_RF.best_estimator_)
print('\n Best normalized gini score for %d-fold search with %d parameter combinations:' % (folds, param_comb))
print(grid_search_RF.best_score_ * 2 - 1)
print('\n Best hyperparameters:')
print(grid_search_RF.best_params_)
results = pd.DataFrame(grid_search_RF.cv_results_)

del n_estimators,max_depth,min_samples_split,min_samples_leaf,params_RF,folds,param_comb,model_RF,skf_RF

#results.to_csv('RF-grid-search-results-15-filtered.csv', index=False)

def toint(x):
    return int(x)



#%%
#Output to specific csv for Kaggle
def predictTest(testdata,model):
    #outcome is such that it can be submitted at kaggle right away.
    #Preprocessing of testdata should be done beforehand, srch_id and prop_id should be set as index
    pred = model.predict_proba(X_test).T[1]
    testdata = testdata.reset_index()
    m = np.matrix([testdata['srch_id'].to_list(),pred,test['prop_id'].to_list()]).T
    pred_df = pd.DataFrame(m,columns=['srch_id','prediction','prop_id'])
    pred_df['prop_id'] = pred_df['prop_id'].apply(lambda x:toint(x))
    pred_df['srch_id'] = pred_df['srch_id'].apply(lambda x:toint(x))
    
    final_pred_df = pred_df.sort_values(by=['srch_id','prediction'], ascending=[True,False])
    #print(final_pred_df) #for those who don't believe the df is not sorted per search_id by the prediction
    final_pred_df = final_pred_df.reset_index()
    final_pred_df = final_pred_df.set_index(['srch_id'])
    del final_pred_df['prediction'],final_pred_df['index']
    
    return final_pred_df

#Get prediction seperatly
#pred = grid_search_RF.best_estimator_.predict_proba(X_test).T[1]

model = grid_search_RF.best_estimator_
pred = predictTest(X_test,model)

pred.to_csv('pred2.csv')



#%%
#EVALUATION WITH NDCG

def ndcg(pred,train,k=5): 
    #pred has columns [srch_id,prop_id,prediction]
    #train has all srch ids prop ids, features and Y variable 'relevance_grades'
    #Dont put srch_id and prop_id in index!

    pred['rank'] = pred.groupby("srch_id")["prediction"].rank("first", ascending=False)
    pred = pred.loc[pred['rank'].isin([i for i in range(1,k+1)])]
    pred = pred.sort_values(['srch_id','rank'])

    def changeranktolog(x):
        if x != 1:
            return np.log2(x)
        else:
            return x
    pred['rank'] = pred['rank'] +1
    pred['rank'] = pred['rank'].apply(lambda x: changeranktolog(x))
    data = pred.merge(train[['srch_id','prop_id','relevance_grades']],left_on=['srch_id','prop_id'],right_on=['srch_id','prop_id'],how= 'left')
    rel_grades_sorted = data[['srch_id','relevance_grades']].sort_values(['srch_id','relevance_grades'],ascending = [True,False])
    
    rel_grades_sorted = rel_grades_sorted.reset_index()

    del rel_grades_sorted['srch_id'],rel_grades_sorted['index']

    data = data.merge(rel_grades_sorted,left_index = True,right_index=True)

    #print(data[['relevance_grades_x','relevance_grades_y']])
    data['user'] = data['relevance_grades_x'] / data['rank']
    
    data['best'] = data['relevance_grades_y'] / data['rank']
    
    score = data[['srch_id','user','best']].groupby(['srch_id']).sum()
    
    score = score['user'] / score['best']
    
    score = score.fillna(0)
    #print(user)
    totalscore= sum(score)
    #print(usersum)
    count = len(score.index)
    
    return totalscore/count

ndcg(pred_df, sample_train)

#%%

#%%
#PREDICT POSITION
from random import sample 
import random
random.seed(1)

user_list = list(train['srch_id'].unique())
sample_list = sample(user_list,round(len(user_list) * 1))
sample_train = train[train['srch_id'].isin(sample_list)]
sample_train = sample_train.query('random_bool == 0')
sample_train
#sample_train = train.sample(n=300000)
#print(sample_train)

del user_list,sample_list

idlist = ['srch_id','prop_id']
catvars = ['promotion_flag', 'site_id', 'prop_country_id']
numvars = ['prop_location_score2', 'srch_query_affinity_score', 'prop_starrating', 'prop_review_score', 
           'comp1_rate', 'comp2_rate', 'comp3_rate', 'comp4_rate', 'comp5_rate', 'comp6_rate', 'comp7_rate',
           'comp8_rate', 'srch_room_count', 'price_usd', 'Avg_price_propID', 'price_usd_position']

featurelist = ['prop_location_score2','promotion_flag', 'srch_query_affinity_score', 'prop_starrating']

targetlist = ['position_rank']

test_processed = test[idlist + catvars]
train_processed = sample_train[idlist + catvars]

test_processed[numvars] = test[numvars]
train_processed[numvars] = sample_train[numvars]

#For now, mark all missing values with an apparent different value
for f in numvars:
    test_processed[f]=test_processed[f].fillna(-1)
    train_processed[f]=train_processed[f].fillna(-1) 

train_processed[targetlist] = sample_train[targetlist]

X_train = train_processed[idlist + catvars + numvars]
#X_train = X_train.set_index(idlist)
Y_train = train_processed[idlist + targetlist]
#Y_train = Y_train.set_index(idlist)
X_test = test_processed[idlist + catvars + numvars]
#X_test = X_test.set_index(idlist)
del test_processed, train_processed
gc.collect()

#%%

#Split training and validation from prior splitted training data, default is at 70%
def splitTrainToTrainAndVal(training_data_X,training_data_Y,perc = 0.7):
    user_list = list(training_data_X['srch_id'].unique())
    user_list_train = user_list[0:round(len(user_list)*perc)]
    user_list_val = user_list[round(len(user_list)*perc):len(user_list)]
    
    X_train = training_data_X[training_data_X['srch_id'].isin(user_list_train)]
    Y_train = training_data_Y[training_data_Y['srch_id'].isin(user_list_train)]
    X_val = training_data_X[training_data_X['srch_id'].isin(user_list_val)]       
    Y_val = training_data_Y[training_data_Y['srch_id'].isin(user_list_val)]
    
    return X_train,Y_train,X_val,Y_val

X_train,Y_train,X_val,Y_val = splitTrainToTrainAndVal(X_train,Y_train)
gc.collect()


#%%

def getGroupCounts(training_data,testing_data):    
    srch_id_count = training_data[['srch_id']]
    srch_id_count['count'] = 1
    groups_count_train = np.array(srch_id_count.groupby(['srch_id'],axis=0).count()['count'])
    
    srch_id_count = testing_data[['srch_id']]
    srch_id_count['count'] = 1
    groups_count_test = np.array(srch_id_count.groupby(['srch_id'],axis=0).count()['count'])
    
    return groups_count_train,groups_count_test
    #del X_test['prop_id']
groups_count_train,groups_count_val = getGroupCounts(X_train,X_val)

del Y_train['srch_id'],Y_train['prop_id']
del Y_val['srch_id'],Y_val['prop_id']
#%%
  
import xgboost as xgb
params = {'objective': 'rank:ndcg',
        'eval_metric':'ndcg@5-',
        'max_depth': 7
        #'max_delta_step':5,
        #'gamma':3,
        #'min_child_weight':5
        #'eta': 0.2
    #    'min_child_weight':3
        #'reg_alpha':[0,3,5],

        }

dtrain = xgb.DMatrix(data=X_train, label=Y_train)
dtrain.set_group(group=groups_count_train)

dval = xgb.DMatrix(data=X_val, label=Y_val)
dval.set_group(group=groups_count_val)
#dtrain.set_group(np.array(group_sizes))
evals_result = {}
watchlist = [(dval,'test'),(dtrain, 'train')]
model_XGB_position = xgb.train(params=params,dtrain=dtrain,early_stopping_rounds=5,num_boost_round=300,evals=watchlist,evals_result=evals_result)

import pickle
filename = 'XGB_position.sav'
pickle.dump(model_XGB_position, open(filename, 'wb'))

#%%
#test2 = test[idlist + catvars + numvars]
dtrain = xgb.DMatrix(data=train[idlist + catvars + numvars])
position_rank_est = model_XGB.predict(dtrain)
train['position_rank_est'] = position_rank_est
train['position_rank_est'] = train.groupby("srch_id")["position_rank_est"].rank("first", ascending=True)
train.to_pickle("./train_pickle.pkl")

dtest = xgb.DMatrix(data=test[idlist + catvars + numvars])
position_rank_est = model_XGB.predict(dtest)
test['position_rank_est'] = position_rank_est
test['position_rank_est'] = test.groupby("srch_id")["position_rank_est"].rank("first", ascending=True)
test.to_pickle("./test_pickle.pkl")


#X_test['position_rank'] = round(X_test['position_rank'], 0).astype(int)

#test.to_pickle("./test_pickle.pkl")

#pred = model_XGB.predict(dval)
#model = xgb.train(params={'objective': 'rank:ndcg'}, dtrain=dtrain, num_boost_round=10)
#XGB.fit(X_train, Y_train)
#pred_XGB = XGB.predict_proba(X_test)
#ROC_XGB = roc_auc_score(np.array(X_test), np.array(pred_XGB.T[1]))

#%%
#RF MODEL
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV

np.random.seed(12)
rf = RandomForestRegressor(min_samples_leaf = 5, max_features = len(X_train.columns), n_estimators=10)

import time 
startTime = time.time()

rf.fit(X_train, Y_train)  
y_pred = rf.predict(X_train)  

print('Mean Squared Error:', metrics.mean_squared_error(sample_train['position'], y_pred))
print('Mean Absolute Error:', metrics.mean_absolute_error(sample_train['position'], y_pred))

fi = pd.DataFrame({'feature': list(X_train.columns),
                   'importance': rf.feature_importances_}).\
                    sort_values('importance', ascending = False)

#add position to testset



#%%query = '(srch_id == 1) & (prop_id == 1)'
train.query(query)

for i in train['srch_id'].unique()[0:4]:
    train[train['srch_id'] == i].sort_values(by=['srch_id', 'booking_bool', 'click_bool'], ascending=False)['prop_id']
    