import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from statistics import *
import matplotlib.pyplot as plt

#the purpose of the project is predicting monthly collection amount for a payment kiosk (for those under the responsibility of the central office)
    
df = pd.read_excel('final.xlsx')


df['Address'] = df['Address'].str.lower()
df['Address'] = df['Address'].str.replace(',','.')

df_no_duplicates = df.drop_duplicates(subset=['Terminal', 'Address'])
df_no_duplicates_dict = df_no_duplicates['Address'].value_counts()

def currency_convert(a):
    if a['Currency']=='USD':
        return a['Amount'] * 1.7
    elif a['Currency']=='EUR':
        return a['Amount'] * 1.85
    else:
        return a['Amount']

df['Amount_AZN'] = df.apply(currency_convert, axis=1)

del df['Currency']
del df['Terminal']

#finding Monthly encashment amount for each terminal location = (total amount - first encashment amount)/working days)*30

grouped_df = df.groupby('Address').agg({'Amount_AZN': ['sum', 'first'], 'Date_encashment': lambda x: (x.max() - x.min()).days}).reset_index()
grouped_df.columns = ['Address', 'Total_Amount', 'First_encashment_amount', 'Date_diff']
grouped_df = grouped_df[(grouped_df['Total_Amount'] > 0) & (grouped_df['Date_diff'] > 0)]
grouped_df['Turnover_Amount'] = grouped_df['Total_Amount'] - grouped_df['First_encashment_amount']
grouped_df['Monthly_Amount_Per_Address'] = (grouped_df['Turnover_Amount'] / grouped_df['Date_diff'])*30

#how many terminal are in the same place?
grouped_df['Terminal_Count'] = grouped_df['Address'].map(df_no_duplicates_dict)

#monthly
grouped_df['Monthly_Amount'] = grouped_df['Monthly_Amount_Per_Address'] / grouped_df['Terminal_Count']

plt.hist(grouped_df['Date_diff'], bins= 30, color='skyblue', edgecolor='black', alpha = 0.5)
plt.xlabel('Working days')
plt.ylabel('Count')
plt.title('Working days of terminals')
plt.show()
plt.cla()

def findOutliers( series ) -> dict:
    output = {}

    output['mean'] = series.mean()
    output['std'] = series.std()
    output['q3'] = series.quantile(0.75) # q0.75
    output['q1'] = series.quantile(0.25) # q0.25

    output['upper'] = output['mean'] + 3 * output['std']
    output['lower'] = output['mean'] - 3 * output['std']

    output['iqr'] = output['q3'] - output['q1']
    output['upper2'] = output['q3'] + 1.5 * output['iqr']
    output['lower2'] = output['q1'] - 1.5 * output['iqr']

    for o in output:
        output[o] = round( output[o], 2 )

    return output

out = findOutliers(grouped_df['Monthly_Amount'])

grouped_df = grouped_df[ ~(grouped_df['Monthly_Amount'] > out['upper'])]

grouped_df = grouped_df[ ~(grouped_df['Monthly_Amount'] < 15000)]

#max 6 terminals are in same place
grouped_df = grouped_df[ grouped_df['Terminal_Count'] < 7 ]

del grouped_df['Monthly_Amount_Per_Address']
del grouped_df['Total_Amount']
del grouped_df['First_encashment_amount']
del grouped_df['Turnover_Amount']
del grouped_df['Date_diff']

#some addresses were incorrectly written - example: Qusar and qusar or şəh, şəh.
#grouped_df['Address'] = grouped_df['Address'].str.lower()
#grouped_df['Address'] = grouped_df['Address'].str.replace(',','.')

#some characters were written in Cyrillic fonts
for old_text, new_text in main_address_dict.items():
    grouped_df['Address'] = grouped_df['Address'].str.replace(old_text, new_text)


#extracting main addresses districts of Baku + Sumqayıt, Abşeron, Xızı, Quba, Qusar, Xaçmaz, Şabran, Siyəzən, Xızı
grouped_df['Main_Address'] = grouped_df['Address'].apply(lambda x: x.split()[0])

#I deleted the terminals that were placed in stock. Mainly, terminals are sent here if they have technical problems and don't work to their full potential
grouped_df = grouped_df[~grouped_df['Address'].str.contains('anbar')]
grouped_df = grouped_df[~grouped_df['Address'].str.contains('test')]

#The company has established new regional centers and has delegated control of the terminals with addresses containing [excluded_values] to these new centers
excluded_values = ['salyan', 'sabirabad', 'şirvan', 'imişli', 'hacıqabul', 'saatlı', 'biləsuvar']
mask = grouped_df['Main_Address'].isin(excluded_values)
grouped_df = grouped_df[~mask]

#extracting districts, streets, highways etc
separatorwords = ['şəh.', 'küç','qəs','yolu','massivi','şos', 'pr']
for word in separatorwords:
    grouped_df[word] = grouped_df['Address'].apply(lambda x, word=word: x.split(word)[0].strip().split('. ')[-1] if word in x else None)

#creation of regions
def assign_region(row):
    if row['Main_Address'] in ['sumqayıt', 'abşeron', 'xızı']:
        return 'abşeron-xızı'
    elif row['Main_Address'] in ['quba', 'siyəzən', 'qusar', 'xaçmaz', 'şabran']:
        return 'quba-xaçmaz'
    elif row['Main_Address'] in ['binəqədi', 'nəsimi', 'yasamal', 'xətai', 'sabunçu', 'nərimanov', 'xəzər', 'nizami', 'suraxanı', 'səbail', 'qaradağ']:
        return 'bakı'
    else:
        return 'Other'

grouped_df['Region'] = grouped_df.apply(assign_region, axis=1)

#encoding for separatorwords
for x in separatorwords:
    new_dict = grouped_df[x].value_counts(normalize=True).to_dict()
    grouped_df[x+'fr'] = grouped_df[x].map(new_dict)
    del grouped_df[x]
    new_dict = {}

market_type_dict = {
    ' express': 1,
    ' minimarket': 1,
    ' market': 2,
    ' supermarket': 3,
    ' hipermarket': 4
}

grouped_df['market_type'] = grouped_df['Address'].apply(lambda x: next((market_type_dict[key] for key in market_type_dict if key in x), None))

#creation of new columns with some words that have high correllation with monthly amount
for x in allwords:
    grouped_df[x] = grouped_df['Address'].apply(lambda t: 1 if x in t else 0)


grouped_df.fillna(0,inplace=True)

#some terminals are outside, thats mean is they work 24hours. Sales team said that working time for other terminals avg 15 hours
terminal24h = ['çöl','tumba','divararası','london','col']
grouped_df['working_time'] = grouped_df['Address'].apply(lambda x: 1 if any(keyword in x for keyword in terminal24h) else 0.625)

#adding subregion statistics to df

def get_region_data(row):
    return regions_data.get(row['Region'], {})
grouped_df = pd.concat([grouped_df, grouped_df['Region'].apply(lambda x: pd.Series(get_region_data({'Region': x})))], axis=1)

scaler = MinMaxScaler()
columns_to_normalize = [
    "Region_Area",
    "Region_People",
    "Region_Legal_entities",
    "Region_Physical person",
    "Region_Employees",
    "Region_Avg_Salary",
    "Region_Total_Salary",
    "Region_Production",
    "Region_Industry",
    "Region_Trade_Turnover",
    "Region_Investments",
    "Region_Density_of_population"
]
grouped_df[columns_to_normalize] = scaler.fit_transform(grouped_df[columns_to_normalize])

#adding subregion statistics to df

def get_subregion_data(row):
    return subregions_data.get(row['Main_Address'], {})
grouped_df = pd.concat([grouped_df, grouped_df['Main_Address'].apply(lambda x: pd.Series(get_subregion_data({'Main_Address': x})))], axis=1)
columns_to_normalize2 = ["Place","People","Avg_Salary","Industry_Production_Price","Trade_Turnover","Density_of_population","kapital"]
grouped_df[columns_to_normalize2] = scaler.fit_transform(grouped_df[columns_to_normalize2])

for c in grouped_df:
    if grouped_df[c].nunique() == 1:
        del grouped_df[c]

main_address_unique = grouped_df['Main_Address'].value_counts(normalize=True).to_dict()
grouped_df['Main_Address'] = grouped_df['Main_Address'].map(main_address_unique)

region_unique = grouped_df['Region'].value_counts(normalize=True).to_dict()
grouped_df['Region'] = grouped_df['Region'].map(region_unique)

del grouped_df['Address']


columns_list = grouped_df.columns
for x in columns_list:
    y = grouped_df['Monthly_Amount'].corr(grouped_df[x])
    if y < 0:
        print(x,grouped_df['Monthly_Amount'].corr(grouped_df[x]))


plt.hist(grouped_df['Monthly_Amount'],alpha = 0.5)
plt.show()
plt.cla()

#grouped_df.to_excel('final-excel7777.xlsx')

from sklearn.ensemble import AdaBoostRegressor
from sklearn import datasets, ensemble

from sklearn.ensemble import RandomForestRegressor
from sklearn import datasets, linear_model

import xgboost as xgb
from sklearn.linear_model import Ridge, Lasso

#clf = RandomForestRegressor(max_depth=11, random_state=0)

#clf = ensemble.GradientBoostingRegressor()

#clf = linear_model.LinearRegression()

clf = xgb.XGBRegressor()

#clf = Lasso()

#clf = Ridge()

import numpy as np

target = "Monthly_Amount"

grouped_df = grouped_df.sample(frac= 1.0)

limit = 0.85
limit = int(len(grouped_df) * limit)

train = grouped_df[:limit]
test = grouped_df[limit:]

train = train.sample(frac = 1.0)

print(train.shape)

#Split

train_X = train.drop( columns = [target])
train_y = train[target]

test_X = test.drop( columns = [target])
test_y = test[target]

clf.fit(train_X, train_y)

print("Score:",clf.score( test_X, test_y ))

test_X['prediction'] = clf.predict( test_X )# + MEAN
test_X['true'] = test_y #+ MEAN

mean_value = np.mean(test_X[['prediction', 'true']])

test_X['prediction'] += mean_value
test_X['true'] += mean_value

test_X['error'] = test_X['true'] - test_X['prediction']
test_X['direction'] = np.sign(test_X['error'])
test_X['abserror'] = np.abs(test_X['error'])
test_X['percentage'] = test_X['error'] / test_X['true']
test_X['abspercentage'] = test_X['abserror'] / test_X['true']

test_X['bigerror'] = test_X['abspercentage'] > 0.28
test_X['bigerror'] = test_X['bigerror'].astype(int)

small = test_X[test_X['bigerror'] == 0]
big = test_X[test_X['bigerror'] == 1]
Accuracy = len(small)/(len(small)+len(big))
Total = len(small)+len(big)

print(len(small), len(big), 'Total test: ', Total, 'Accuracy: ', Accuracy)

plt.hist(test_X['true'], alpha = 0.3, bins=30, color='Yellow', edgecolor='black')
plt.hist(test_X['prediction'], alpha= 0.3, bins=30, color='Red', edgecolor='black')
plt.xlabel('Monthly Encashment Amount')
plt.ylabel('Count')
plt.title('Monthly Turnover of Terminals')
plt.legend(labels=['True', 'Prediction'])
plt.show()


print(grouped_df['Monthly_Amount'].corr(grouped_df['Terminal_Count']))