import random
import sys
import pandas as pd


def create(amount):
    """
        随机产生几注双色球（6+1）
        :param number:
        :return:
        """
    result = []

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

        # 数据预处理
        reds = nums_pre(reds)
        blue = nums_pre([blue])[0]

        result.append(' '.join(reds) + " + " + blue)
    return '\n'.join(result)

def nums_pre(nums):
    """
    购买数字预处理，如果是个位数，加上0
    :param nums:
    :return:
    """
    if nums:
        if isinstance(nums, list) or isinstance(nums,tuple):
            return ['0{}'.format(int(item)) if int(item) < 10 else str(int(item)) for item in nums]
        else:
            return '0{}'.format(int(nums)) if int(nums) < 10 else str(int(nums))
    else:
        return ''

if __name__=="__main__":
    # print(create(2))
    print("02 06 07 08 17 18 + 07")
    print("03 07 18 22 25 27 + 06")
    print(create(int(sys.argv[1])))