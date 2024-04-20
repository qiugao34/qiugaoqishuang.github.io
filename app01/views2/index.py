from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app01.data_analysis import analysis
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')


def test(request):
    return render(request, 'test.html')
