from django.db import models


# Create your models here.
class ShennongMateriaMedical(models.Model):
    name = models.CharField(verbose_name='名称', max_length=64)
    namepy = models.CharField(verbose_name='名称(含拼音)', max_length=64)
    level = models.CharField(verbose_name='品级', max_length=32)
    category = models.CharField(verbose_name='类别', max_length=32)
    feature = models.CharField(verbose_name='性味', max_length=32)
    wei = models.CharField(verbose_name='味', max_length=32)
    xing = models.CharField(verbose_name='性', max_length=32)
    meridian = models.CharField(verbose_name='归经', max_length=32)
    original = models.CharField(verbose_name='原文', max_length=128)




class TyphoidFeverAndMiscellaneousDiseases(models.Model):
    prescriptionName = models.CharField(verbose_name='药名', max_length=32)
    prescription = models.CharField(verbose_name='药方', max_length=64)
    medical = models.CharField(verbose_name='药物', max_length=64)


