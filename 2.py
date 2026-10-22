"""
项目名称：Steam 游戏数据探索性分析 (EDA)
作者：你的名字
日期：2026年10月

【业务问题 A 分析结论：价格与口碑的关系】
- 整体趋势：价格与好评率并非线性关系。
- 最佳性价比区间：10-30 美元区间的游戏平均好评率最高，达到 80.61%。
- 极端价格表现：免费游戏（76.19%）和 30 美元以上的高价游戏（76.15%）好评率均相对较低。
- 原因推测：免费游戏可能受限于内购模式和外挂；高价 3A 大作则面临玩家极高的预期，首发 Bug 容易引发差评。
"""


import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("D:\\数据分析\\first\\games.csv")

df = df.drop(columns=['Movies'])

# 数据错位的调整
df['real_price'] = df['Required age']
df['real_name'] = df['AppID']

# 计算评论量，且保留评论量>=50的游戏
df['total_reviews'] = df['Positive'] + df['Negative']
df_clean = df[df['total_reviews'] >= 50]
df_clean['positive_rate'] = df_clean['Positive'] / df_clean['total_reviews']

# 价格分档
bins = [-1,0,10,30,999999]
labels = ['免费','0-10美元','10-30美元','30美元以上']
df_clean['price_group'] = pd.cut(df_clean['real_price'], bins=bins, labels=labels)

# print("价格转换后的前5个样本：", df['Price'].head().tolist())
# print(df[['AppID', 'Name', 'Price']].head(10))
print(df.info())
# print(df[['real_name', 'real_price', 'Positive', 'Negative']].head(10))
# print(f"过滤前：{len(df)} 款游戏，过滤后（有效样本）：{len(df_clean)} 款游戏")
# print(df_clean.head())\
# print("\n各个价格区间的游戏数量分布：",df_clean['price_group'].value_counts())


# 画图
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# price_analysis = df_clean.groupby('price_group',observed=True)['positive_rate'].mean()
#
# plt.figure(figsize = (10,6))
# price_analysis.plot(kind='bar',color=['#4C72B0', '#55A868', '#C44E52', '#8172B2'],edgecolor='black')
#
# plt.title('Steam 游戏价格与平均好评率的关系',fontsize = 16)
# plt.xlabel('价格区间',fontsize = 12)
# plt.ylabel('平均好评率',fontsize = 12)
# plt.xticks(rotation = 0)
# plt.ylim(0,1)
#
# for i,v in enumerate(price_analysis):
#     plt.text(i , v + 0.02 , f'{v:.2%}' , ha = 'center')
#
# plt.show()
#
#
#
#
# # 游戏的价格区间占比
# price_counts = df_clean['price_group'].value_counts()
#
# # 画图
# plt.figure(figsize = (8,8))
# colors= ['#4C72B0', '#55A868', '#C44E52', '#8172B2']
# plt.pie(price_counts, labels=price_counts.index, autopct='%1.1f%%', startangle=90, colors=colors, explode=(0.05, 0, 0, 0))
# plt.title('Steam 游戏价格区间分布占比（样本量>=50）', fontsize = 16)
# plt.show()
#
#
#
# 按主类型分组，计算游戏数量和平均好评率
df_clean['main_genre'] = df_clean['Genres'].astype(str).str.split(',').str[0]
genre_stats = df_clean.groupby('main_genre').agg(游戏数量=('positive_rate', 'count'),平均好评率=('positive_rate', 'mean')).reset_index()
genre_stats = genre_stats[genre_stats['游戏数量'] >= 100]
genre_stats = genre_stats.sort_values('平均好评率', ascending=True)
#
# # 画图
# plt.figure(figsize=(12, 8))
# plt.barh(genre_stats['main_genre'], genre_stats['平均好评率'], color='#55A868', edgecolor='black')
#
# plt.title('不同游戏类型的平均好评率对比 (样本量≥100)', fontsize=16)
# plt.xlabel('平均好评率', fontsize=12)
# plt.ylabel('游戏类型', fontsize=12)
# plt.xlim(0, 1)
# for i, v in enumerate(genre_stats['平均好评率']):
#     plt.text(v + 0.01, i, f"{v:.2%}", va='center')
#
# plt.show()