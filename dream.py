import json
import random
import sys
import pandas as pd
from datetime import date
import requests


LUCK_NUMBER_1 = "02,06,07,08,17,18 + 07"
LUCK_NUMBER_2 = "03,07,18,22,25,27 + 06"

def create(amount):
    """
        随机产生几注双色球（6+1）
        :param amount: 生成的注数
        :return:
        """
    result = []

    # 随机生成几（amount）注双色球
    for item in range(amount):
        reds = []
        # 产生6个红球
        while len(reds) < 6:
            # 从1-33中随机取一个数字
            temp_red_num = random.randint(1, 33)
            if temp_red_num not in reds:
                reds.append(temp_red_num)

        # 蓝球
        blue = random.randint(1, 16)

        # 红球排序
        reds.sort()

        # 数据美化
        reds = nums_pre(reds)
        blue = nums_pre([blue])[0]

        result.append(','.join(reds) + " + " + blue)
    # return '\n'.join(result)
    return result


def nums_pre(nums):
    """
    生成数字美化，如果是个位数，加上0
    :param nums:
    :return:
    """
    if nums:
        if isinstance(nums, list) or isinstance(nums, tuple):
            return ['0{}'.format(int(item)) if int(item) < 10 else str(int(item)) for item in nums]
        else:
            return '0{}'.format(int(nums)) if int(nums) < 10 else str(int(nums))
    else:
        return ''


def write_to_excel(amount):
    """
    写入excel做记录
    可以使用excel/csv 目前使用csv  excel会有一定格式问题，需要处理 我懒的处理了，直接用csv
    :param amount: 彩票注数
    :return:
    """
    # df = pd.read_excel("./file/Five-Million.xlsx", sheet_name='Sheet1')
    df = pd.read_csv("./file/Five-Million.csv")

    # 显示所有列
    pd.set_option('display.max_columns', 1000000)  # 可以在大数据量下，没有省略号
    # 显示所有行
    pd.set_option('display.max_rows', 1000000)
    # 设置value的显示长度为1000000，默认为50
    pd.set_option('display.max_colwidth', 1000000)

    pd.set_option('display.width', 1000000)

    # 获取原有记录数量
    df_length = len(df)
    # 创建本期的号码
    luck_result = create(amount)
    # 获取运行当前日期
    today = date.today().strftime("%Y-%m-%d")
    # 把本期号码加到记录数据里
    for i in range(len(luck_result)):
        df.loc[df_length + i, 'Date'] = today
        df.loc[df_length + i, 'Number'] = luck_result[i]

    df.loc[len(df) + 1] = {'Date': today, 'Number': LUCK_NUMBER_1}
    df.loc[len(df) + 2] = {'Date': today, 'Number': LUCK_NUMBER_2}

    # 回写记录
    # df.to_excel("./file/Five-Million.xlsx", sheet_name='Sheet1', index=False, header=True)
    df.to_csv("./file/Five-Million.csv", index=False, header=True)

    print("===File All Data===")
    print(df)
    print("==========")
    print(LUCK_NUMBER_1)
    print(LUCK_NUMBER_2)
    print('\n'.join(luck_result))


def redeem():
    """
    兑奖
    :return:
    """
    # 发送请求的url地址
    url = 'http://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice'

    params = {
        'name': 'ssq',
        'issueCount': 30,
        'issueStart': '',
        'issueEnd': '',
        'dayStart': '',
        'dayEnd': '',
    }
    headers = {
        'Referer': 'http://www.cwl.gov.cn/ygkj/wqkjgg/ssq/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }
    response = requests.get(url=url, params=params, headers=headers)
    response.encoding = 'utf-8'
    loads = json.loads(response.text)
    result = loads['result']

    result_dict = {}
    # 处理历史中奖号码，方便兑奖判断
    for i in range(len(result)):
        key = result[i]['date'][0:10]
        result_dict.setdefault(key, result[i]['red'] + " + " + result[i]['blue'])

    # df = pd.read_excel("./file/Five-Million.xlsx", sheet_name='Sheet1')
    df = pd.read_csv("./file/Five-Million.csv")

    # 所有已出奖期数据补全
    df2 = df[df["WinNumber"].isnull()]
    for index, row in df2.iterrows():
        date_ = row["Date"]
        if date_ not in result_dict.keys():
            # 把各期中奖号转为df
            result_df = pd.DataFrame.from_dict(result_dict, orient='index').reset_index()
            for ind, row in result_df.iterrows():
                if int(date_.replace("-", "")) < int(row["index"].replace("-", "")) and int(
                        date_.replace("-", "")) > int(result_df.iloc[ind + 1, 0].replace("-", "")):
                    date_ = row["index"]

        # df.iloc[index, 2] = result_dict[date_]
        df.iloc[index, 2] = result_dict.get(date_)

    # 还没验奖的数据
    df3 = df[df["Premium"].isnull()]
    for index, row in df3.iterrows():
        df.iloc[index, 3] = get_premium(row["Number"], row["WinNumber"])

    df.to_csv("./file/Five-Million.csv", index=False, header=True)


def get_premium(number, win_number):
    """
    获取奖金数量
    :param number: 自选号码
    :param win_number: 当期中奖号码
    :return: 奖金额
    """
    if win_number is None:
        return
    # 红球中奖数
    red_count = 0
    # 篮球中奖数
    blue_count = 0

    number_split = number.split(" + ")
    red = number_split[0].split(",")
    blue = number_split[1]

    win_number_split = win_number.split(" + ")
    win_red = win_number_split[0].split(",")
    win_blue = win_number_split[1]

    # 红球中奖数量
    for item in red:
        if item in win_red:
            red_count = red_count + 1

    # 篮球中奖数量
    if blue == win_blue:
        blue_count = 1

    # 判断中奖金额
    if red_count == 6 and blue_count == 1:
        premium = 5000000  # 一等奖（6+1）
    elif red_count == 6 and blue_count == 0:
        premium = 100000  # 二等奖（6+0）
    elif red_count == 5 and blue_count == 1:
        premium = 3000  # 三等奖（5+1)
    elif red_count == 5 and blue_count == 0:
        premium = 200  # 四等奖(5+0)
    elif red_count == 4 and blue_count == 1:
        premium = 200  # 四等奖(4+1)
    elif red_count == 4 and blue_count == 0:
        premium = 10  # 五等奖(4+0)
    elif red_count == 3 and blue_count == 1:
        premium = 10  # 五等奖(3+1)
    elif red_count == 0 and blue_count == 1:
        premium = 5  # 六等奖(0+1)
    elif red_count == 1 and blue_count == 1:
        premium = 5  # 六等奖(1+1)
    elif red_count == 2 and blue_count == 1:
        premium = 5  # 六等奖(2+1)
    else:
        premium = 0

    return premium


# write_to_excel(3)
# redeem()
# get_premium("01,03,11,22,26,31 + 10","01,03,11,22,26,31 + 10")

if __name__ == "__main__":
    redeem()
    write_to_excel(int(sys.argv[1]))
