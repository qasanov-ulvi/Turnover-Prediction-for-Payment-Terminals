"""
#it helps me to editing addresses - Cyrillic character problems - line12

dict = grouped_df['Main_Address'].value_counts(normalize=True).to_dict()
print(dict.keys())

"""

main_address_dict = {'xətai':'xətai', 'abşeron':'abşeron', 'binəqədi':'binəqədi',
             'yasamal':'yasamal', 'sabunçu':'sabunçu', 'nəsimi':'nəsimi', 'nərimanov':'nərimanov', 'xəzər':'xəzər', 'nizami':'nizami', 'suraxanı':'suraxanı',
             'sumqayıt':'sumqayıt', 'səbail':'səbail', 'qaradağ':'qaradağ', 'xaçmaz':'xaçmaz', 'quba':'quba', 'sabirabad':'sabirabad', 'siyəzən':'siyəzən', 
             'şirvan':'şirvan', 'i̇mişli':'imişli', 'qusar':'qusar', 'şabran':'şabran', 'hacıqabul':'hacıqabul', 'binagadi':'binəqədi', 'saatlı':'saatlı', 'xacmaz':'xaçmaz',
             'abseron':'abşeron', 'qaradag':'qaradağ', 'nasimi':'nəsimi', 'sumqayit':'sumqayıt', 'biləsuvar':'biləsuvar', 'binaqadi':'binəqədi', 'sabuncu':'sabunçu',
             'sumqаyıt':'sumqayıt', 'xatai':'xətai', 'xızı':'xızı', 'sabail':'səbail', 'salyan':'salyan', 'xazar':'xəzər', 'sabran':'şabran', 'narimanov':'nərimanov',
             'xazar.':'xəzər', 'suraxani':'suraxanı', 'siyazan':'siyəzən', 'xəzər.':'xəzər', 'xаçmаz':'xaçmaz', 'nəsimi.':'nəsimi', 'хızı':'xızı', 'хаçmаz':'xaçmaz'}



""" it helps me to selection of words for creation of dummies
words = []
for address in grouped_df['Address']:
    address_words = ''.join(char if char.isalnum() or char.isspace() else ' ' for char in address).split()
    words.extend(address_words)
word_counts = {}
for word in words:
    word_counts[word] = word_counts.get(word, 0) + 1
sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
top_words = sorted_words[0:200]
for word, count in top_words:
    grouped_df[word] = grouped_df['Address'].str.contains(word)
    correlation = grouped_df['Monthly_Amount'].corr(grouped_df[word])
    if abs(correlation)> 0.02 and len(word)>1:
     print(f"{word}: {count} - Correlation with 'Amount': {correlation}")
     del grouped_df[word]
"""

#some little cities place in some big districts

littlecities = ['xırdalan','xudat']

store = ['bazar ','ticarət','ticarət mərkəzi','sədərək t','binə t','mall','plaza','mağaza',' market',' supermarket', ' hipermarket',' minimarket',' express']

medical = ['aptek','hospital','klinik','xəstəxana','medical']

others = ['universitet','kartomat',' store','beynəlxalq','avtovağzal','dəmiryol',
          'yeni','stansiya','dayanacaq','şəhər','şəhərciyi','filial','park','asan','asan xidmət','asan kommunal','mərkəz','mərkəzi','m/s','bağ','metro','mkr','kəsişməsi']

markets = ['araz','bravo','bazarstore','superstore','rahat','bolmart','al market','neptun','qayalı','bizim','megastore',
           'spar','oba','tamstore']

banks = ['abb bank','afb bank','access bank', 'asb bank', 'atb bank','bank avrasiya','bank btb','bank of baku',	'bank respublika',
         'expressbank','kapital bank', 'naxçıvanbank', 'paşa bank',	'premium bank',	'rabitəbank',	'turanbank', 'unibank', 'vtb bank',
         'xalq bank', 'yapı kredi',	'yelobank',	'ziraat bank']

allwords = littlecities + store + medical + others + markets + banks

"""statistics for regions - https://www.stat.gov.az/source/demoqraphy/"""

regions_data = {
    "bakı": {
        "Region_Area": 2.14,
        "Region_People": 2336.6,
        "Region_Legal_entities": 116702,
        "Region_Physical person": 336950,
        "Region_Employees": 899.9,
        "Region_Avg_Salary": 1080.6,
        "Region_Total_Salary": 40651261.4,
        "Region_Production": 105503183.6,
        "Region_Industry": 75384524,
        "Region_Trade_Turnover": 30288816.8,
        "Region_Investments": 9508358.5,
        "Region_Density_of_population": 1092
    },
    "abşeron-xızı": {
        "Region_Area": 3.73,
        "Region_People": 874.1,
        "Region_Legal_entities": 11983,
        "Region_Physical person": 66647,
        "Region_Employees": 100.5,
        "Region_Avg_Salary": 689.2,
        "Region_Total_Salary": 3665522.2,
        "Region_Production": 7208923.5,
        "Region_Industry": 4762166.3,
        "Region_Trade_Turnover": 2837377.4,
        "Region_Investments": 692056.3,
        "Region_Density_of_population": 234
    },
    "quba-xaçmaz": {
        "Region_Area": 6.96,
        "Region_People": 543.8,
        "Region_Legal_entities": 4847,
        "Region_Physical person": 76702,
        "Region_Employees": 55.5,
        "Region_Avg_Salary": 577.7,
        "Region_Total_Salary": 2197164.6,
        "Region_Production": 2455206.1,
        "Region_Industry": 346209.5,
        "Region_Trade_Turnover": 1673151,
        "Region_Investments": 428623.4,
        "Region_Density_of_population": 78
    }
}

subregions_data = {
    "sumqayıt": {
        "Place": 0.09,
        "People": 426,
        "Avg_Salary": 734.1,
        "Industry_Production_Price": 4043.7884,
        "Trade_Turnover": 1563760.6,
        "Density_of_population": 4733,
    },
    "abşeron": {
        "Place": 1.97,
        "People": 431.5,
        "Avg_Salary": 637.7,
        "Industry_Production_Price": 708.3087,
        "Trade_Turnover": 1245208.2,
        "Density_of_population": 219
    },
    "xızı": {
        "Place": 1.67,
        "People": 16.6,
        "Avg_Salary": 495,
        "Industry_Production_Price": 10.0692,
        "Trade_Turnover": 28408.6,
        "Density_of_population": 10
    },
    "xaçmaz": {
        "Place": 1.06,
        "People": 173.5,
        "Avg_Salary": 560,
        "Industry_Production_Price": 188.0256,
        "Trade_Turnover": 646300.7,
        "Density_of_population": 164
    },
    "quba": {
        "Place": 2.61,
        "People": 169.1,
        "Avg_Salary": 589,
        "Industry_Production_Price": 60.5573,
        "Trade_Turnover": 570996,
        "Density_of_population": 65
    },
    "qusar": {
        "Place": 1.5,
        "People": 101.7,
        "Avg_Salary": 556.4,
        "Industry_Production_Price": 21.4087,
        "Trade_Turnover": 251434.4,
        "Density_of_population": 68
    },
    "siyəzən": {
        "Place": 0.7,
        "People": 41.5,
        "Avg_Salary": 643.6,
        "Industry_Production_Price": 20.7975,
        "Trade_Turnover": 97161.4,
        "Density_of_population": 59
    },
    "şabran": {
        "Place": 1.09,
        "People": 58,
        "Avg_Salary": 564.5,
        "Industry_Production_Price": 55.4204,
        "Trade_Turnover": 107258.5,
        "Density_of_population": 53
    },
    "binəqədi": {
        "Place": 0.17,
        "People": 268,
        "Avg_Salary": 702.5,
        "Industry_Production_Price": 916.5,
        "Trade_Turnover": 2032988,
        "Density_of_population": 1806
    },
    "xətai": {
        "Place": 0.03,
        "People": 290,
        "Avg_Salary": 1131.5,
        "Industry_Production_Price": 651.9,
        "Trade_Turnover": 3020776,
        "Density_of_population": 9167
    },
    "xəzər": {
        "Place": 0.37,
        "People": 168,
        "Avg_Salary": 1118.4,
        "Industry_Production_Price": 666.9,
        "Trade_Turnover": 751129,
        "Density_of_population": 553
    },
    "qaradağ": {
        "Place": 1.08,
        "People": 128,
        "Avg_Salary": 1404.5,
        "Industry_Production_Price": 1328.7,
        "Trade_Turnover": 2315215,
        "Density_of_population": 107
    },
    "nərimanov": {
        "Place": 0.02,
        "People": 179,
        "Avg_Salary": 925.7,
        "Industry_Production_Price": 5610.2,
        "Trade_Turnover": 2553188,
        "Density_of_population": 9005
    },
    "nəsimi": {
        "Place": 0.01,
        "People": 222,
        "Avg_Salary": 1044.6,
        "Industry_Production_Price": 1104.2,
        "Trade_Turnover": 3231079,
        "Density_of_population": 21880
    },
    "nizami": {
        "Place": 0.02,
        "People": 201,
        "Avg_Salary": 931.8,
        "Industry_Production_Price": 893.6,
        "Trade_Turnover": 2870753,
        "Density_of_population": 9235
    },
    "sabunçu": {
        "Place": 0.24,
        "People": 247,
        "Avg_Salary": 768.6,
        "Industry_Production_Price": 720.6,
        "Trade_Turnover": 3329078,
        "Density_of_population": 1373
    },
    "səbail": {
        "Place": 0.03,
        "People": 102,
        "Avg_Salary": 1824.1,
        "Industry_Production_Price": 61670.3,
        "Trade_Turnover": 1871097,
        "Density_of_population": 3387
    },
    "suraxanı": {
        "Place": 0.12,
        "People": 222,
        "Avg_Salary": 823.7,
        "Industry_Production_Price": 497.7,
        "Trade_Turnover": 1295425,
        "Density_of_population": 1728
    },
    "yasamal": {
        "Place": 0.02,
        "People": 249,
        "Avg_Salary": 847.4,
        "Industry_Production_Price": 662.8,
        "Trade_Turnover": 2368103,
        "Density_of_population": 9655
    }
}

#atm counts

kapital = {
    'binəqədi': 73,
    'xətai': 17,
    'xəzər': 31,
    'qaradağ': 22,
    'nərimanov': 33,
    'nəsimi': 59,
    'nizami': 29,
    'sabunçu': 34,
    'səbail': 22,
    'suraxanı': 22,
    'yasamal': 70,
    'sumqayıt': 44,
    'abşeron': 39,
    'xızı': 6,
    'quba': 25,
    'qusar': 19,
    'xaçmaz': 16,
    'siyəzən': 0,
    'şabran': 8
}


for region, data in subregions_data.items():
    if region in kapital:
        data['kapital'] = kapital[region]


# type: ignore