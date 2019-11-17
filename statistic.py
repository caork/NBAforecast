# 基于非参数统计-决策树对NBA篮球赛的获胜球队预测
# 采用NBA2018-2019年赛季数据
# 整合后数据已上传至github ——> http:


# 首先使用pandas读取csv数据
#%%
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from collections import defaultdict
import pandas as pd
import numpy as np
from backup import *
location = r'/home/jsao/Documents/pycode/dataset.csv'
df = pd.read_csv(location, parse_dates=["Date"])

# len(df) #查看球赛数量
# out： 1312  #1312场球赛

# df.head() #查看数据前五行
# out：
'''
        Date Start (ET)         Visitor/Neutral  ...  Unnamed: 7 Attend.  Notes
0 2019-01-01      7:30p               Utah Jazz  ...         NaN  19,800    NaN
1 2019-01-01      8:00p         Detroit Pistons  ...         NaN  17,534    NaN
2 2019-01-01      9:00p         New York Knicks  ...         NaN  19,520    NaN
3 2019-01-01      9:00p  Portland Trail Blazers  ...          OT  17,583    NaN
4 2019-01-01     10:30p      Philadelphia 76ers  ...         NaN  17,868    NaN

[5 rows x 10 columns]
'''

# 特征值提取

df['homewin'] = df['PTS'] < df['PTS.1']
y_value = df['homewin'].values  # 转化特征值供scikit-learn提取

# 创建字典储存球队比赛结果
'''
提取新特征：
1. 上一场主场是否胜利
2. 上一场客场是否胜利
3. 主场是否是背靠背比赛
4. 是否是连续客场
'''

won_last = defaultdict(int)
df['HomeLastWin'] = None
df['VisitorLastWin'] = None
for index, row in df.iterrows():
    home_team = row['Home/Neutral']
    visitor_team = row['Visitor/Neutral']
    row['HomeLastWin'] = won_last[home_team]
    row['VisitorLastWin'] = won_last[visitor_team]
    df.loc[index] = row
    won_last[home_team] = row['homewin']
    won_last[visitor_team] = not row['homewin']
df['HomeLastWin'][df['HomeLastWin'] == 0] = False
df['VisitorLastWin'][df['VisitorLastWin'] == 0] = False

df['Back_to_Back'] = None
df['ContinuousBack'] = None

back_to_back_home = ''
back_to_back_visitor = ''
ContinuousBack = won_last
for index, row in df.iterrows():
    if index != 0:
        back_to_back_visitor = df.iloc[index-1, 2]
        back_to_back_home = df.iloc[index-1, 4]
    if row['Visitor/Neutral'] not in [back_to_back_home, back_to_back_visitor] or row['Home/Neutral'] not in [back_to_back_home, back_to_back_visitor]:
        row['Back_to_Back'] = True
    else:
        row['Back_to_Back'] = False
    visitor_team = back_to_back_visitor
    home_team = back_to_back_home
    if ContinuousBack[visitor_team] == True:
        row['ContinuousBack'] = True
    else:
        row['ContinuousBack'] = False
    ContinuousBack[home_team] = False
    ContinuousBack[visitor_team] = True
    df.loc[index] = row

#加入进攻效率和防守效率排行
df['defense'] = None
df['attack'] = None
team = pd.read_csv(r'/home/jsao/Documents/pycode/team.csv')
for index, row in df.iterrows():
    HomeTeam = row['Home/Neutral']
    VisitorTeam = row['Visitor/Neutral'] #have not check yet
    HomeAttackScore = team.loc[team['team'] == HomeTeam,'attack']
    VisitorAttackScore = team.loc[team['team'] == VisitorTeam,'attack']
    HomeDefenseScore = team.loc[team['team'] == HomeTeam,'defense']
    VisitorDefenseScore = team.loc[team['team'] == VisitorTeam,'defense']
    row['attack'] = int(HomeAttackScore) < int(VisitorAttackScore)
    row['defense'] = int(HomeDefenseScore) < int(VisitorDefenseScore)
    df.loc[index] = row




#%%
# 建立一个value全部为零的字典
CountWin = ContinuousBack 
for value in CountWin:
    CountWin[value] = 0
#%%
winteam = ''
for index, row in df.iterrows():
    if row['homewin'] == True:
        winteam = row['Home/Neutral']
    else:
        winteam = row['Visitor/Neutral']
    CountWin[winteam] += 1
#%%
df['totalscore'] = None
for index, row in df.iterrows():
    if row['Home/Neutral'] < row['Visitor/Neutral']:
        row['totalscore'] = False
    else:
        row['totalscore'] = True
    df.loc[index] = row
# %%
clf = DecisionTreeClassifier(random_state=14)
#x_previouswins = df[['HomeLastWin','VisitorLastWin','Back_to_Back','ContinuousBack','defense','attack','totalscore']].values
x_previouswins = df[['totalscore','defense','attack']].values
scores = cross_val_score(clf,x_previouswins, y_value,scoring='accuracy')
print('Accuracy: {0:.1f}%'.format(np.mean(scores)*100))


# %%

