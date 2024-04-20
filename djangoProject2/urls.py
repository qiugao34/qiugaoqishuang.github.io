"""
URL configuration for djangoProject2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01.views2 import index, classify, taste, usage

urlpatterns = [
    path('index/', index.index),
    # 第一页分类
    path('classify/show/', classify.classify_show),
    # 饼图
    path('classify/pie/', classify.classify_pie),
    # 柱状图
    path('classify/bar/', classify.classify_bar),
    # 词云
    path('classify/wordcloud/', classify.classify_wordcloud),
    # 显示原文
    path('classify/origin/', classify.classify_origin),
    # 第二页性味
    path('taste/show/', taste.taste_show),
    # 重叠柱状图
    path('stacked/bar/', taste.stacked_orizontal_bar),
    # formatter回调函数
    path('deyial/get/', taste.detail_get),
    # 南丁格尔图
    path('taste/pie/', taste.get_pie_data),
    # 第三页用法
    path('usage/show/', usage.usage_show),
    # 每个数量段柱状图
    path('usage/amount/', usage.amount_bar),
    # 饼图
    path('amount/pie/', usage.amount_pie),
    # 每个药物搭配使用的药物数量柱状图
    path('match/bar/', usage.match_bar),
    # 获取每个药的药方
    path('prescription/get/', usage.prescription_get),
    # 药方表单
    path('prescription/table/', usage.prescription_table),


]
