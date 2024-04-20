from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app01.data_analysis import analysis
from django.views.decorators.csrf import csrf_exempt


def taste_show(request):
    return render(request, '2.html')


@csrf_exempt
def stacked_orizontal_bar(request):
    xing_list = list(analysis.get_taste_data().keys())
    taste_data = []
    for xing in xing_list:
        taste_data.append(list(analysis.get_taste_data()[xing].values()))
    data1 = list(zip(xing_list, taste_data))
    data2, data3 = analysis.get_bar_data()
    result = {
        "status": True,
        "data1": data1,
        "data2": data2,
        "data3": data3,
    }
    return JsonResponse(result)


def detail_get(request):
    xing = request.GET.get('x')
    wei = request.GET.get('wei')
    name_str = analysis.get_examples(xing, wei)
    result = {
        "data": name_str,
        "status": True
    }
    return JsonResponse(result)


def get_pie_data(request):
    gj = analysis.calculate_gj()
    result = {
        "status": True,
        "data": gj
    }
    return JsonResponse(result)
