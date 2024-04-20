import pandas as pd
from sqlalchemy import create_engine

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject2.settings")
django.setup()
engine = create_engine('mysql+pymysql://root:wxx20051128@127.0.0.1:3306/tcm_data')


def write2sql(df, table_name):
    df.to_sql(table_name, engine, if_exists="replace", index=False)


def read_mysql(table_name):
    sql_cmd = f'select * from {table_name}'
    df = pd.read_sql(sql_cmd, engine)
    return df


data = read_mysql('app01_shennongmateriamedical')
data2 = read_mysql('app01_typhoidfeverandmiscellaneousdiseases')


def level_size(level):
    level_data = data[data['level'] == level].count()
    return int(level_data['level'])


def get_classify(name):
    data_tcm_level = data[data['level'] == name]
    data_lei_dict = data_tcm_level.groupby(by='category').size().to_dict()
    return list(data_lei_dict.keys()), list(data_lei_dict.values())


def get_level_name(level, lei=False):
    data_tcm_level = data[data['level'] == level]
    if not lei:
        level_name = data_tcm_level['name']
        return level_name.tolist()
    level_name = data_tcm_level[data_tcm_level['category'] == lei]['name']
    return level_name.tolist()


def generate_taste_dict(xing, m, taste_xing_dict):
    for taste in m:
        if not taste_xing_dict[xing]:
            taste_xing_dict[xing] = {'甘': 0, '酸': 0, '苦': 0, '辛': 0, '咸': 0}
            taste_xing_dict[xing][taste] += 1
        else:
            taste_xing_dict[xing][taste] += 1


def get_taste_data():
    # name_data = data['名称']
    taste_data = (data['wei']).tolist()
    xing_data = data['xing'].tolist()
    # taste_data_dict = {}
    # for k in xing_data:
    #     if k not in taste_data_dict:
    #         taste_data_dict[k] = 1
    #     else:
    #         taste_data_dict[k] += 1
    # print(taste_data_dict)
    taste_xing_dict = {'寒': None, '凉': None, '平': None, '微温': None, '温': None, '热': None}
    for m, n in zip(taste_data, xing_data):
        if '微' not in n:
            for xing in n:
                generate_taste_dict(xing, m, taste_xing_dict)
        else:
            if n == '微寒':
                n = '凉'
            generate_taste_dict(n, m, taste_xing_dict)
    return taste_xing_dict


def get_bar_data():
    data = get_taste_data()
    x_list = []  # 性列表
    w_dict = {}  # 味字典
    for x_name, dt in data.items():
        s = sum(dt.values())
        x_list.append({'name': x_name, 'value': s})
        for w_name, num in dt.items():
            if w_name not in w_dict:
                w_dict[w_name] = num
            else:
                w_dict[w_name] += num
    w_list = [{'name': name, 'value': value} for name, value in w_dict.items()]  # 将字典转换为列表
    return x_list, w_list


def become_dict():
    '''
    将get_taste_data函数返回的数据格式变为旭日图所需的格式
    :return: 列表嵌套字典
    '''
    data = get_taste_data()
    n_list = []
    for name, dt in data.items():
        s = sum(dt.values())
        ch_list = []
        for n, d in dt.items():
            n_dict = {'value': d, 'name': n}
            ch_list.append(n_dict)
        name_dict = {'name': name, 'value': s, 'children': ch_list}
        n_list.append(name_dict)
    return n_list


def get_origin(name):
    """
    获取原文
    :return:
    """
    name_py = data['namepy'][data['name'] == name].values[0]
    lei = data['category'][data['name'] == name].values[0]
    xingwei = data['feature'][data['name'] == name].values[0]
    origin = data['original'][data['name'] == name].values[0]
    return name_py, lei, xingwei, origin


def get_examples(x, w):
    """
    通过性味来获取该性味下有哪些药物
    :param x: 性
    :param w: 味
    :return: 随机抽取的药物字符串
    """
    amount = 5
    l = []
    if x == '凉':
        x = '微寒'
    if w == '辛' or w == '甘':
        l = data['name'][(data['xing'] == x) & (data['wei'] == '甘辛')].tolist()
    name_list = data['name'][(data['xing'] == x) & (data['wei'] == w)].tolist()
    name_list.extend(l)
    name_list_examples = name_list[:amount]
    name_str = '、'.join(name_list_examples)
    return name_str


def calculate_gj():
    """
    统计归经中各个器官的出现次数
    """
    gj_dict = {}
    for i in data["meridian"].tolist():
        if not pd.isnull(i):
            for j in i.split("、"):
                if j not in gj_dict:
                    gj_dict[j] = 1
                else:
                    gj_dict[j] += 1
    gj_list = []
    for name, num in gj_dict.items():
        gj_list.append({'value': num, 'name': name})
    gj_list.sort(key=lambda x: x['value'], reverse=False)
    return gj_list


def count_medicine():
    """统计《伤寒论》药方中每种药出现的次数"""
    md_dict = {}  # 所有的药物
    for name_str in data2["medical"].tolist():
        for name in name_str.split('、'):
            if name not in md_dict:
                md_dict[name] = 1
            else:
                md_dict[name] += 1
    medicine_data = data['name'].tolist()
    used_medicine = {}  # 在《本经》中出现的药物
    for i in md_dict.keys():
        if i in medicine_data:
            used_medicine[i] = md_dict[i]
    return used_medicine


def match():
    """计算《本经》中有多少种药物出现已及《伤寒论》药方中出现了多少种《本经》的药物"""
    used_medicine = count_medicine()
    # 计算每个数量段有多少种药
    amount_dict = {'1': 0, '2': 0, '3~5': 0, '6~10': 0, '11~': 0}
    for i in used_medicine.values():
        if i == 1:
            amount_dict['1'] += 1
        elif i == 2:
            amount_dict['2'] += 1
        elif 3 <= i <= 5:
            amount_dict['3~5'] += 1
        elif 6 <= i <= 10:
            amount_dict['6~10'] += 1
        else:
            amount_dict['11~'] += 1
    return list(amount_dict.keys()), list(amount_dict.values())


def find_amount(amount):
    """返回每个数量段的所以药物名字和出现次数"""
    md_dict = count_medicine()
    if amount == '1':
        count_list_dict = [{'name': name, 'value': md_dict[name]} for name in md_dict if md_dict[name] == 1]
    elif amount == '2':
        count_list_dict = [{'name': name, 'value': md_dict[name]} for name in md_dict if md_dict[name] == 2]
    elif amount == '3~5':
        count_list_dict = [{'name': name, 'value': md_dict[name]} for name in md_dict if 3 <= md_dict[name] <= 5]
    elif amount == '6~10':
        count_list_dict = [{'name': name, 'value': md_dict[name]} for name in md_dict if 6 <= md_dict[name] <= 10]
    else:
        count_list_dict = [{'name': name, 'value': md_dict[name]} for name in md_dict if md_dict[name] >= 11]
    return count_list_dict


def every_medicine_match(name):
    match_medicine_dict = {}  # 搭配药物名字:数量
    md_dict = count_medicine()
    for name_str in data2["medical"].tolist():
        if name in name_str:
            for medicine in name_str.split('、'):
                if medicine != name and medicine not in match_medicine_dict and medicine in md_dict:
                    match_medicine_dict[medicine] = 1
                elif medicine != name and medicine in match_medicine_dict and medicine in md_dict:
                    match_medicine_dict[medicine] += 1
    return list(match_medicine_dict.keys()), list(match_medicine_dict.values())


def get_prescription(params):
    df = data2
    for name in params:
        df = df[df['medical'].str.contains(name)]
    name1 = df['prescriptionName'].tolist()[:6]
    name2 = df['prescription'].tolist()[:6]
    return name1, name2


if __name__ == '__main__':
    # process_pinyin()
    print(len(every_medicine_match('甘草')[0]))
    # df = pd.read_excel(r"D:\PycharmProject\djangoProject2\app01\static\data\伤寒论药方.xlsx")
    # write2sql(df,"app01_typhoidfeverandmiscellaneousdiseases")


