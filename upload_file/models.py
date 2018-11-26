#coding:utf-8
from django.db import models

# Create your models here.
class File(models.Model):
    """上传文件表
    关联字段:
        permissions(一对多)
    """

    id = models.AutoField(primary_key=True)
    excel_name = models.CharField(max_length=200, verbose_name='文件名称')
    sheet_num = models.IntegerField(verbose_name='包含的sheet数')
    flag = models.BooleanField(max_length=32, default=False, verbose_name='执行状态')
    date = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    txt = models.ForeignKey(to='Txt', to_field='id', verbose_name='对应生成的txt', on_delete=models.CASCADE)

    def __str__(self):
        return self.excel_name

    class Meta:
        verbose_name_plural = '上传EXCEL文件表'


class Txt(models.Model):
    """txt文件表
    """

    id = models.AutoField(primary_key=True)
    txt_name = models.CharField(max_length=200, verbose_name='文件名称',unique=True)
    txt_result = models.CharField(max_length=200, default='', verbose_name='wc -l /data/logs/tmp_log/guantie_everyday_result/crawl_2018-09-02.txt 执行结果')

    def __str__(self):
        return self.txt_name

    class Meta:
        verbose_name_plural = '生成txt文件表'