# 导入所需的库
import requests  # 用于发送HTTP请求
from lxml import etree  # 用于解析HTML文档
import pandas as pd  # 用于数据处理与分析，创建及操作DataFrame对象
import re

# 定义请求头信息
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"
    )
}


# 定义辅助函数：获取列表首个元素并去除其两端空格
def get_first_text(text_list: list[str]) -> str:
    """
    返回列表首个字符串并去除两端空格，若列表为空或出错则返回空字符串

    参数:
    text_list (list[str]): 包含多个字符串的列表

    返回:
    str: 列表首个字符串（已去两端空格），或空字符串（在列表为空或出错时）
    """
    try:
        return text_list[0].strip()
    except IndexError:
        return ""


# 初始化数据存储结构
COLUMNS = ["序号", "标题", "链接", "评分", "年份和类型", "参演人员"]  # 定义DataFrame的列名
df = pd.DataFrame(columns=COLUMNS)  # 创建一个空的DataFrame，列名为上述定义的COLUMNS

# 计算并生成豆瓣电影Top 250分页URL列表
START_OFFSETS = range(
    0, 250, 25
)  # 从0开始，每25个记录为一页，共10页（0, 25, 50, ..., 225）
URLS = [
    "https://movie.douban.com/top250?start={}&filter=".format(offset)
    for offset in START_OFFSETS
]  # 根据偏移量生成URL列表

# 遍历每个分页URL，抓取并解析电影信息
for index, url in enumerate(
    URLS, start=1
):  # 使用enumerate为每个URL赋予一个递增序号（从1开始）
    try:
        # 发起网络请求
        response = requests.get(url=url, headers=HEADERS)

        # 检查请求是否成功（HTTP状态码为200）
        response.raise_for_status()  # 若状态码非200，抛出HTTPError异常

        # 解析响应的HTML文本为ElementTree对象
        html = etree.HTML(response.text)

        # 查找页面上的所有电影li元素
        movie_lis = html.xpath(
            '//*[@id="content"]/div/div[1]/ol/li'
        )  # 使用XPath定位li标签

        # 遍历每个电影li元素，提取并处理电影信息
        for li in movie_lis:
            # 解析电影标题、链接、评分、年份和类型、参演人员
            title = get_first_text(
                li.xpath("./div/div[2]/div[1]/a/span[1]/text()")
            )  # 标题
            link = get_first_text(li.xpath("./div/div[2]/div[1]/a/@href"))  # 链接
            score = get_first_text(
                li.xpath("./div/div[2]/div[2]/div/span[2]/text()")
            )  # 评分
            yearandtype = get_first_text(
                li.xpath("./div/div[2]/div[2]/p[1]/text()[2]")
            )  # 年份和类型
            actor = get_first_text(li.xpath("./div/div[2]/div[2]/p[1]/text()"))
            # 参演人员
            # 可选：打印当前电影信息（调试用）
            print(index, title, link, score, yearandtype, actor)

            # 将当前电影信息添加到DataFrame中
            df.loc[len(df.index)] = [index, title, link, score, yearandtype, actor]

    except requests.RequestException as e:  # 捕获网络请求相关异常
        print(f"请求失败：{e}")

    except Exception as e:  # 捕获其他未知异常
        print(f"解析或处理数据时发生错误：{e}")

# 将DataFrame中的数据保存为Excel文件
df.to_excel("豆瓣电影top250数据.xlsx", sheet_name="豆瓣电影top250数据", na_rep="")


# 读取已生成的Excel文件
df = pd.read_excel("豆瓣电影top250数据.xlsx", sheet_name="豆瓣电影top250数据")

# 使用 split() 函数拆分年份和类型
df["年份"] = df["年份和类型"].apply(
    lambda x: re.sub(r"\D", "", x.split("/")[0]).lstrip()
)  # 提取年份并清理非数字字符
df["类型"] = df["年份和类型"].apply(
    lambda x: " ".join(x.split("/")[1:]).replace("/", "")
)  # 提取类型并去除斜线，保留空格分隔

# 删除旧的“年份和类型”列
df.drop("年份和类型", axis=1, inplace=True)

# 保存更新后的DataFrame到Excel文件
df.to_excel(
    "豆瓣电影top250数据_年份类型拆分.xlsx", sheet_name="豆瓣电影top250数据", index=False
)

print(
    "年份和类型已拆分为独立列,并分别进行了清理,保存到新文件:豆瓣电影top250数据_年份类型拆分.xlsx"
)
print("Excel文件已经生成!")
