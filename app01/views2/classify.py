from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app01.data_analysis import analysis
from django.views.decorators.csrf import csrf_exempt
import random


def classify_show(request):
    return render(request, '1.html')


def classify_pie(request):
    level_list = ['上药', '中药', '下药']
    level_size_list = []
    for level in level_list:
        level_dict = {'name': level, 'value': analysis.level_size(level)}
        level_size_list.append(level_dict)
    result = {
        "status": True,
        "data": {
            'data_list': level_size_list
        }
    }
    return JsonResponse(result)


def name_list_dict(name='上药'):
    name_data = analysis.get_level_name(name)
    name_dict_list = []
    for i in name_data:
        value = random.randint(20, 40)
        name_dict = {'name': i, 'value': value}
        name_dict_list.append(name_dict)
    return name_dict_list


@csrf_exempt
def classify_bar(request):
    if request.method == 'GET':
        get_data = analysis.get_classify('上药')
        name_dict_list = name_list_dict()
        xaxis_list = get_data[0]
        result = {
            "status": True,
            "data": {
                "xaxis_list": xaxis_list,
                "series_list": get_data[1],
                "word_list": name_dict_list
            }
        }
        return JsonResponse(result)
    else:
        name = request.POST.get('name')
        get_data = analysis.get_classify(name)
        name_dict_list = name_list_dict(name)
        xaxis_list = get_data[0]
        result = {
            "status": True,
            "data": {
                "xaxis_list": xaxis_list,
                "series_list": get_data[1],
                "word_list": name_dict_list
            }
        }
        return JsonResponse(result)


def classify_wordcloud(request):
    lei = request.GET.get('lei')
    level = request.GET.get('level')
    data_name = analysis.get_level_name(level, lei)
    name_dict_list = []
    for i in data_name:
        value = random.randint(20, 40)
        name_dict = {'name': i, 'value': value}
        name_dict_list.append(name_dict)
    result = {
        "status": True,
        "data": name_dict_list
    }
    return JsonResponse(result)


def classify_origin(request):
    """
    点击词云图的词语后展示原文
    :param request:
    :return:
    """
    name = request.GET.get('name')
    name_py, lei, xw, origin = analysis.get_origin(name)
    data_dict = {'name_py': name_py, 'lei': lei, 'xw': xw, 'origin': origin}
    request = {
        "status": True,
        "data": data_dict
    }
    return JsonResponse(request)
