from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import  TaskTable,TaskMessage,Kintai
from django.db import connection
from django.utils.timezone import localtime, now
from django.utils import timezone

def moveToJinkenhi(request):
    return render(request, "jinkenhi.html")

def moveToKintai(request):
    dateToday = datetime.date.today()
    value_yotei=Kintai.objects.values_list('teiji',flat=True).filter(Date=dateToday).reverse()
    value_overtime=Kintai.objects.values_list('overtime',flat=True).filter(Date=dateToday)
    value_result=Kintai.objects.values_list('result',flat=True).filter(Date=dateToday)

    return render(request, "kintai.html",{"yotei":value_yotei,
                                        "overtime":value_overtime,
                                        "result":value_result,
                                        })

def saveKintai(request):
    username = request.user.username

    add_to_kintai = Kintai(
        edit_username=username,
        type=("予定"),
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
     )

    add_to_kintai.save()

    return redirect("moveToKintai")