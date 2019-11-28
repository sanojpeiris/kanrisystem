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



def moveToJinkenhi(request):
    return render(request, "jinkenhi.html")

#〜〜〜〜〜〜〜勤怠情報

def moveToKintai(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    # print("nextmonth=",month)
    value_yotei=Kintai.objects.values_list('teiji',flat=True).filter(Date=dateToday,edit_username=username, type="予定", ).reverse()
    value_overtime_yotei=Kintai.objects.values_list('overtime',flat=True).filter(Date=dateToday,edit_username=username, type="予定",  )
    value_jisseki=Kintai.objects.values_list('teiji',flat=True).filter(Date=dateToday,edit_username=username, type="実績",).reverse()
    value_overtime_jisseki=Kintai.objects.values_list('overtime',flat=True).filter(Date=dateToday,edit_username=username, type="実績", )
    value_yotei_kakunin=Kintai.objects.values_list('kakunin',flat=True).filter(Date=dateToday,edit_username=username, type="予定", )
    value_jisseki_kakunin=Kintai.objects.values_list('kakunin',flat=True).filter(Date=dateToday,edit_username=username, type="実績", )
    print("kakunin-",value_yotei_kakunin)

    return render(request, "kintai.html",{"yotei":value_yotei,
                                        "overtime_yotei":value_overtime_yotei,
                                        "jisseki":value_jisseki,
                                        "overtime_jisseki":value_overtime_jisseki,
                                        "yotei_kakunin":value_yotei_kakunin,
                                        "jisseki_kakunin":value_jisseki_kakunin,
                                        })

def saveKintai_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()+datetime.timedelta(31)
    month = dateToday.strftime('%B')
    add_to_kintai = Kintai(
        edit_username=username,
        type=("予定"),
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        done=True,
        Month=month,
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
    add_to_kintai = Kintai(
        edit_username=username,
        type=("実績"),
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        done = True,
        Month=month,
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
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def kintai_sashimodoshi(request,kakunin_id):
    is_kakunin_ok=Kintai.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

#〜〜〜〜〜〜〜出張情報

def moveToshucchou(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    value_yotei=Btrip.objects.values_list('B_money',flat=True).filter(Date=dateToday,edit_username=username, type="予定").reverse()
    value_overtime_yotei=Btrip.objects.values_list('gout',flat=True).filter(Date=dateToday,edit_username=username, type="予定")
    value_jisseki=Btrip.objects.values_list('B_money',flat=True).filter(Date=dateToday,edit_username=username, type="実績").reverse()
    value_overtime_jisseki=Btrip.objects.values_list('gout',flat=True).filter(Date=dateToday,edit_username=username, type="実績")
    value_yotei_kakunin=Btrip.objects.values_list('kakunin',flat=True).filter(Date=dateToday,edit_username=username, type="予定", )
    value_jisseki_kakunin=Btrip.objects.values_list('kakunin',flat=True).filter(Date=dateToday,edit_username=username, type="実績", )

    return render(request, "shucchou.html",{"yotei":value_yotei,
                                        "overtime_yotei":value_overtime_yotei,
                                        "jisseki":value_jisseki,
                                        "overtime_jisseki":value_overtime_jisseki,
                                        "yotei_kakunin":value_yotei_kakunin,
                                        "jisseki_kakunin":value_jisseki_kakunin,
                                        })

def saveshucchou_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()+datetime.timedelta(31)
    month = dateToday.strftime('%B')
    add_to_Btrip = Btrip(
        edit_username=username,
        type=("予定"),
        B_money=(request.POST["teiji"]),
        gout=(request.POST["overtime"]),
        done=True,
        Month=month,
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
    add_to_Btrip = Btrip(
        edit_username=username,
        type=("実績"),
        B_money=(request.POST["teiji"]),
        gout=(request.POST["overtime"]),
        done = True,
        Month=month,
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
    kintai_all = Kintai.objects.all()
    shucchou_all = Btrip.objects.all()
    user_list = User.objects.values_list('username', flat=True).distinct()
    print("userlist-",user_list)


    return render(request, "confirm.html",{"kintai_yotei":kintai_yotei,
                                           "kintai_shucchou":kintai_shucchou,  
                                           "shucchou_yotei":shucchou_yotei,
                                           "shucchou_jisseki":shucchou_jisseki,
                                           "user_list":user_list,
                                           "kintai_all":kintai_all,
                                           "shucchou_all":shucchou_all,
    })

def shucchou_kakunin(request,kakunin_id):
    is_kakunin_ok=Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = True
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def shucchou_sashimodoshi(request,kakunin_id):
    is_kakunin_ok=Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")

def confirm_all(request):
    confirm_cursor=connection.cursor()
    confirm_cursor.execute('UPDATE useractivities_kintai set kakunin=True;')
    return redirect("moveToConfirm")