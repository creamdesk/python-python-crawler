import pandas as pd
import plotly.graph_objects as go

# 读取Excel文件
df = pd.read_excel("豆瓣电影top250数据_年份类型拆分.xlsx")

# 按照评分进行分组统计，计算每个评分对应电影的数量
rating_counts = df["评分"].value_counts().reset_index()
rating_counts.columns = ["评分", "数量"]

# 绘制饼状图
fig = go.Figure(
    data=[go.Pie(labels=rating_counts["评分"], values=rating_counts["数量"])]
)
fig.update_layout(title="豆瓣电影Top 250评分分布")

# 设置悬停文本，显示评分和对应的电影数量
fig.update_traces(hovertemplate="评分: %{label}<br>数量: %{value}")

# 显示图表
fig.show()
output_file = "豆瓣电影评分分布.html"
fig.write_html(output_file)
print(f"图表已成功保存为：{output_file}")
