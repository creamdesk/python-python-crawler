import pandas as pd
import numpy as np
import plotly.express as px
import webbrowser

# 读取Excel数据
df = pd.read_excel(
    "豆瓣电影top250数据_年份类型拆分.xlsx", sheet_name="豆瓣电影top250数据"
)

# 取前150条数据并去重，保留唯一的评分和年份组合
df_unique = df.head(150).drop_duplicates(subset=["评分", "年份"])

# 添加随机扰动模拟散点图抖动
jitter_amount = 4  # 调整这个值以控制抖动程度，数值越小，抖动越小
np.random.seed(42)  # 设置随机种子以确保结果可复现
df_unique["评分"] = df_unique["评分"] + jitter_amount * np.random.normal(
    size=len(df_unique)
)
df_unique["年份"] = df_unique["年份"] + jitter_amount * np.random.normal(
    size=len(df_unique)
)
# 保留评分小数点后一位，年份小数点后零位
df_unique["评分"] = df_unique["评分"].round(1)
df_unique["年份"] = df_unique["年份"].astype(int)
# 创建交互式散点图
fig = px.scatter(
    df_unique,
    x="评分",
    y="年份",
    hover_data=["标题", "类型", "参演人员"],
    text="标题",
    template="plotly",  # 使用plotly模板或不指定模板以获得默认白色背景
)

# 将电影片名转换为可点击链接
for i, (index, row) in enumerate(df_unique.iterrows()):
    fig.data[0].text[i] = f'<a href="{row["链接"]}" target="_blank">{row["标题"]}</a>'

# 自定义图表布局
fig.update_layout(showlegend=False)
fig.update_xaxes(
    range=[df["评分"].min() - 0.1, df["评分"].max() + 0.1],
    automargin=True,
    showgrid=True,
)
fig.update_yaxes(
    range=[df["年份"].min() - 5, df["年份"].max() + 5],
    automargin=True,
    showgrid=True,
)
fig.update_layout(
    title_text="豆瓣电影评分与年份散点图", title_font_size=20
)

# 定位文本标签
fig.update_traces(textposition="top center")

# 保存并打开图表
fig.write_html("interactive_scatterplot_plotly_with_jitter.html")
webbrowser.open("interactive_scatterplot_plotly_with_jitter.html")
