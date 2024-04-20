from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app01.data_analysis import analysis
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json as js
from app01.utils.pagination import Pagination
from app01 import models


def usage_show(request):

    return render(request, '3.html')


def amount_bar(request):
    data1, data2 = analysis.match()
    result = {
        "status": True,
        "data1": data1,
        "data2": data2,
    }
    return JsonResponse(result)


def amount_pie(request):
    amount = request.GET.get('amount')
    data = analysis.find_amount(amount)
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result)


def match_bar(request):
    name = request.GET.get('medicine')
    data1, data2 = analysis.every_medicine_match(name)
    result = {
        "status": True,
        "data1": data1,
        "data2": data2,
    }
    return JsonResponse(result)


def prescription_get(request):
    datalist = request.GET.get("datalist")
    datalist = eval(datalist)
    name, prescription = analysis.get_prescription(datalist)
    result = {
        "status": True,
        "data1": name,
        "data2": prescription,
    }
    return JsonResponse(result)


def prescription_table(request):
    datalist = request.GET.get("datalist")
    if datalist:
        datalist = eval(datalist)
        queryset = models.TyphoidFeverAndMiscellaneousDiseases.objects.all()
        for i in datalist:
            queryset = queryset.filter(medical__contains=i)
        page_object = Pagination(request, queryset)
        pre_list = page_object.page_queryset
        page_string = page_object.html()
        context = {
            "status": True,
            'data': list(pre_list.values()),
            'pageString': page_string,
        }
        return JsonResponse(context)