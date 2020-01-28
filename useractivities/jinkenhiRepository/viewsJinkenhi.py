from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import  TaskTable,TaskMessage,Kintai,Btrip
from django.db import connection
from django.utils.timezone import localtime, now
from django.utils import timezone
# from dateutil.relativedelta import relativedelta
import calendar
# from datetime import datetime, date
from time import gmtime, strftime
from datetime import date, timedelta

def moveToJinkenhi(request):
    return render(request, "jinkenhi.html")

#〜〜〜〜〜〜〜勤怠情報

def moveToKintai(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    # print("nextmonth=",month)
    value_yotei=Kintai.objects.values_list('teiji',flat=True).filter(Month=nextmonth, edit_username=username, type="予定", ).reverse()
    value_overtime_yotei=Kintai.objects.values_list('overtime',flat=True).filter(Month=nextmonth, edit_username=username, type="予定",  )

    value_jisseki=Kintai.objects.values_list('teiji',flat=True).filter(Month=previousmonth, edit_username=username, type="実績",).reverse()
    value_overtime_jisseki=Kintai.objects.values_list('overtime',flat=True).filter(Month=previousmonth, edit_username=username, type="実績", )

    value_yotei_kakunin=Kintai.objects.values_list('kakunin',flat=True).filter(Month=nextmonth, edit_username=username, type="予定", )
    value_jisseki_kakunin=Kintai.objects.values_list('kakunin',flat=True).filter(Month=month, edit_username=username, type="実績", )
    
    is_yotei_visible=Kintai.objects.values('is_visible').filter(Month=nextmonth, edit_username=username, type="予定" )
    is_jisseki_visible=Kintai.objects.values('is_visible').filter(Month=month, edit_username=username, type="実績" )
    print("kakunin-",value_yotei_kakunin)
    print("is_visible",is_yotei_visible,is_jisseki_visible)
    today = datetime.date.today()
    # today = 2019-12-29
    lastday_1 = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    firstday = today.replace(day=1)
    lastday = today.replace(day=lastday_1-1)
    return render(request, "kintai.html",{"yotei":value_yotei,
                                        "overtime_yotei":value_overtime_yotei,
                                        "jisseki":value_jisseki,
                                        "overtime_jisseki":value_overtime_jisseki,
                                        "yotei_kakunin":value_yotei_kakunin,
                                        "jisseki_kakunin":value_jisseki_kakunin,
                                        "lastday":lastday,
                                        "today":today,
                                        "firstday":firstday,
                                        "is_yotei_visible":is_yotei_visible,
                                        "is_jisseki_visible":is_jisseki_visible,
                                        })

def saveKintai_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_kintai = Kintai(
        edit_username=username,
        type=("予定"),
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        done=True,
        Month=nextmonth,
     )

    add_to_kintai.save()

    return redirect("moveToKintai")

def deleteKintai_yotei(request):
    username = request.user.username
    type=("予定")
    dateToday = datetime.date.today()
    delete_Kintai=Kintai.objects.all().filter(Date=dateToday,edit_username=username,type=type)
    delete_Kintai.delete()

    return redirect("moveToKintai")

def saveKintai_jisseki(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_kintai = Kintai(
        edit_username=username,
        type=("実績"),
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        done = True,
        Month=previousmonth,
     )

    add_to_kintai.save()

    return redirect("moveToKintai")

def deleteKintai_jisseki(request):
    username = request.user.username
    type=("実績")
    dateToday = datetime.date.today()
    delete_Kintai=Kintai.objects.all().filter(Date=dateToday,edit_username=username,type=type)
    delete_Kintai.delete()

    return redirect("moveToKintai")

def kintai_kakunin(request,kakunin_id):
    is_kakunin_ok=Kintai.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = True
    is_kakunin_ok.done = True
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def kintai_sashimodoshi(request,kakunin_id):
    is_kakunin_ok=Kintai.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.done = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

#〜〜〜〜〜〜〜出張情報

def moveToshucchou(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    
    value_yotei=Btrip.objects.values_list('B_money',flat=True).filter(Month=nextmonth, edit_username=username, type="予定").reverse()
    value_overtime_yotei=Btrip.objects.values_list('gout',flat=True).filter(Month=nextmonth, edit_username=username, type="予定")

    value_jisseki=Btrip.objects.values_list('B_money',flat=True).filter(Month=previousmonth, edit_username=username, type="実績").reverse()
    value_overtime_jisseki=Btrip.objects.values_list('gout',flat=True).filter(Month=previousmonth, edit_username=username, type="実績")
    
    value_yotei_kakunin=Btrip.objects.values_list('kakunin',flat=True).filter(Month=nextmonth, edit_username=username, type="予定", )
    value_jisseki_kakunin=Btrip.objects.values_list('kakunin',flat=True).filter(Month=month, edit_username=username, type="実績", )

    is_yotei_visible=Btrip.objects.values('is_visible').filter(Month=nextmonth, edit_username=username, type="予定" )
    is_jisseki_visible=Btrip.objects.values('is_visible').filter(Month=month, edit_username=username, type="実績" )

    today = datetime.date.today()
    # today = 2019-12-29
    lastday_1 = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    firstday = today.replace(day=1)
    lastday = today.replace(day=lastday_1-1)
    return render(request, "shucchou.html",{"yotei":value_yotei,
                                        "overtime_yotei":value_overtime_yotei,
                                        "jisseki":value_jisseki,
                                        "overtime_jisseki":value_overtime_jisseki,
                                        "yotei_kakunin":value_yotei_kakunin,
                                        "jisseki_kakunin":value_jisseki_kakunin,
                                        "lastday":lastday,
                                        "today":today,
                                        "firstday":firstday,
                                        "is_yotei_visible":is_yotei_visible,
                                        "is_jisseki_visible":is_jisseki_visible,
                                        })

def saveshucchou_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_Btrip = Btrip(
        edit_username=username,
        type=("予定"),
        B_money=(request.POST["teiji"]),
        gout=(request.POST["overtime"]),
        done=True,
        Month=nextmonth,
     )

    add_to_Btrip.save()

    return redirect("moveToshucchou")

def deleteshucchou_yotei(request):
    username = request.user.username
    type=("予定")
    dateToday = datetime.date.today()
    delete_Kintai=Btrip.objects.all().filter(Date=dateToday,edit_username=username,type=type)
    delete_Kintai.delete()

    return redirect("moveToshucchou")

def saveshucchou_jisseki(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_Btrip = Btrip(
        edit_username=username,
        type=("実績"),
        B_money=(request.POST["teiji"]),
        gout=(request.POST["overtime"]),
        done = True,
        Month=previousmonth,
     )

    add_to_Btrip.save()

    return redirect("moveToshucchou")

def deleteshucchou_jisseki(request):
    username = request.user.username
    type=("実績")
    dateToday = datetime.date.today()
    delete_Kintai=Btrip.objects.all().filter(Date=dateToday,edit_username=username,type=type)
    delete_Kintai.delete()

    return redirect("moveToshucchou")


#confirm form

def moveToConfirm(request):
    kintai_yotei=Kintai.objects.all().filter(type="予定")
    kintai_shucchou=Kintai.objects.all().filter(type="実績")
    shucchou_yotei=Btrip.objects.all().filter(type="予定")
    shucchou_jisseki=Btrip.objects.all().filter(type="実績")
    kintai_all = Kintai.objects.all().filter()
    shucchou_all = Btrip.objects.all().filter()
    user_list = User.objects.values_list('username', flat=True).distinct()
    print("userlist-",user_list)
    today = datetime.date.today()
    lastday_1 = calendar.monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1]
    firstday = datetime.date.today().replace(day=1)
    lastday = datetime.date.today().replace(day=lastday_1-1)

    
    print("last day-",lastday)
    print("today-",today)
    print("first day-",firstday)
    # lastDay == today
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday+datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month-1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    
# now = datetime.datetime.now()
# last_month = now.month-1 if now.month > 1 else 12

    print("previousmonth-",previousmonth)
    print("thismonth",month)
    print("nextmonth",nextmonth)

    return render(request, "confirm.html",{"kintai_yotei":kintai_yotei,
                                           "kintai_shucchou":kintai_shucchou,  
                                           "shucchou_yotei":shucchou_yotei,
                                           "shucchou_jisseki":shucchou_jisseki,
                                           "user_list":user_list,
                                           "kintai_all":kintai_all,
                                           "shucchou_all":shucchou_all,
                                           "lastday":lastday,
                                           "today":today,
                                           "firstday":firstday,
    })

def shucchou_kakunin(request,kakunin_id):
    is_kakunin_ok=Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = True
    is_kakunin_ok.done = True
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def shucchou_sashimodoshi(request,kakunin_id):
    is_kakunin_ok=Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.done = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def confirm_all(request):
    confirm_cursor=connection.cursor()
    confirm_cursor.execute('UPDATE useractivities_kintai set kakunin=True;')
    return redirect("moveToConfirm")