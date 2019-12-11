from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import TaskTable, TaskMessage, Kintai, Btrip
from django.db import connection
from django.utils.timezone import localtime, now
from django.utils import timezone
import calendar
from time import gmtime, strftime
from datetime import date, timedelta


# import datetime as DT

def moveToJinkenhi(request):
    return render(request, "jinkenhi.html")


# 〜〜〜〜〜〜〜勤怠情報

def moveToKintai(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    value_yotei = Kintai.objects.values_list('teiji', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                        type="予定", ).reverse()
    value_overtime_yotei = Kintai.objects.values_list('overtime', flat=True).filter(Month=nextmonth,
                                                                                    edit_username=username, type="予定", )

    value_jisseki = Kintai.objects.values_list('teiji', flat=True).filter(Month=previousmonth, edit_username=username,
                                                                          type="実績", ).reverse()
    value_overtime_jisseki = Kintai.objects.values_list('overtime', flat=True).filter(Month=previousmonth,
                                                                                      edit_username=username,
                                                                                      type="実績", )

    value_yotei_kakunin = Kintai.objects.values_list('kakunin', flat=True).filter(Month=nextmonth,
                                                                                  edit_username=username, type="予定", )
    value_jisseki_kakunin = Kintai.objects.values_list('kakunin', flat=True).filter(Month=previousmonth,
                                                                                    edit_username=username, type="実績", )

    is_yotei_visible = Kintai.objects.values('is_visible').filter(Month=nextmonth, edit_username=username, type="予定")
    is_jisseki_visible = Kintai.objects.values('is_visible').filter(Month=month, edit_username=username, type="実績")
    print("kakunin-", value_yotei_kakunin)
    print("is_visible", is_yotei_visible, is_jisseki_visible)
    today = datetime.date.today()

    def last_day_of_month(date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

    firstday = today.replace(day=1)
    secondday = today.replace(day=2)
    thirdday = today.replace(day=3)

    lastday = last_day_of_month(dateToday)
    lastday_sec = (last_day_of_month(lastday) - datetime.timedelta(days=1))
    lastday_third = (last_day_of_month(lastday) - datetime.timedelta(days=2))
    # print("today",day)
    # print("firstday",days)
    kintai_yotei = Kintai.objects.all().filter(edit_username=username, created_month=month, type="予定")
    kintai_jisseki = Kintai.objects.all().filter(edit_username=username, created_month=month, type="実績")
    return render(request, "kintai.html", {"yotei": value_yotei,
                                           "overtime_yotei": value_overtime_yotei,
                                           "jisseki": value_jisseki,
                                           "overtime_jisseki": value_overtime_jisseki,
                                           "yotei_kakunin": value_yotei_kakunin,
                                           "jisseki_kakunin": value_jisseki_kakunin,
                                           "lastday": lastday,
                                           "lastday_sec": lastday_sec,
                                           "lastday_third": lastday_third,
                                           "today": today,
                                           "firstday": firstday,
                                           "secondday": secondday,
                                           "thirdday": thirdday,
                                           "firstday": firstday,

                                           "is_yotei_visible": is_yotei_visible,
                                           "is_jisseki_visible": is_jisseki_visible,
                                           "kintai_yotei": kintai_yotei,
                                           "kintai_jisseki": kintai_jisseki,
                                           })


def saveKintai_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    add_to_kintai = Kintai(
        edit_username=username,
        type=("予定"),
        created_month=month,
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        done=True,
        Month=nextmonth,
    )

    add_to_kintai.save()

    return redirect("moveToKintai")


def deleteKintai_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    type = ("予定")
    delete_Kintai = Kintai.objects.all().filter(Month=nextmonth, edit_username=username, type=type)
    delete_Kintai.delete()

    return redirect("moveToKintai")


def saveKintai_jisseki(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_kintai = Kintai(
        edit_username=username,
        type="実績",
        teiji=(request.POST["teiji"]),
        overtime=(request.POST["overtime"]),
        created_month=month,
        done=True,
        Month=previousmonth,
    )

    add_to_kintai.save()

    return redirect("moveToKintai")


def deleteKintai_jisseki(request):
    username = request.user.username
    type = "実績"
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    delete_Kintai = Kintai.objects.all().filter(Month=previousmonth, edit_username=username, type=type)
    delete_Kintai.delete()

    return redirect("moveToKintai")


def kintai_kakunin(request, kakunin_id):
    is_kakunin_ok = Kintai.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = True
    is_kakunin_ok.done = True
    is_kakunin_ok.save()
    return redirect("moveToConfirm")


def kintai_sashimodoshi(request, kakunin_id):
    is_kakunin_ok = Kintai.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.done = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")


# 〜〜〜〜〜〜〜出張情報

def moveToshucchou(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    value_yotei = Btrip.objects.values_list('B_money', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                         type="予定", ).reverse()
    value_gout_yotei = Btrip.objects.values_list('gout', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                           type="予定", )

    value_jisseki = Btrip.objects.values_list('B_money', flat=True).filter(Month=previousmonth, edit_username=username,
                                                                           type="実績", ).reverse()
    value_gout_jisseki = Btrip.objects.values_list('gout', flat=True).filter(Month=previousmonth,
                                                                             edit_username=username, type="実績", )

    value_yotei_kakunin = Btrip.objects.values_list('kakunin', flat=True).filter(Month=nextmonth,
                                                                                 edit_username=username, type="予定", )
    value_jisseki_kakunin = Btrip.objects.values_list('kakunin', flat=True).filter(Month=previousmonth,
                                                                                   edit_username=username, type="実績", )

    is_yotei_visible = Btrip.objects.values('is_visible').filter(Month=nextmonth, edit_username=username, type="予定")
    is_jisseki_visible = Btrip.objects.values('is_visible').filter(Month=month, edit_username=username, type="実績")
    print("kakunin-", value_yotei_kakunin)
    print("is_visible", is_yotei_visible, is_jisseki_visible)
    today = datetime.date.today()

    def last_day_of_month(date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

    firstday = today.replace(day=1)
    secondday = today.replace(day=2)
    thirdday = today.replace(day=3)

    lastday = last_day_of_month(dateToday)
    lastday_sec = (last_day_of_month(lastday) - datetime.timedelta(days=1))
    lastday_third = (last_day_of_month(lastday) - datetime.timedelta(days=2))
    # print("today",day)
    # print("firstday",days)
    shucchou_yotei = Btrip.objects.all().filter(edit_username=username, created_month=month, type="予定")
    shucchou_jisseki = Btrip.objects.all().filter(edit_username=username, created_month=month, type="実績")
    return render(request, "shucchou.html", {"yotei": value_yotei,
                                             "gout_yotei": value_gout_yotei,
                                             "jisseki": value_jisseki,
                                             "gout_jisseki": value_gout_jisseki,
                                             "yotei_kakunin": value_yotei_kakunin,
                                             "jisseki_kakunin": value_jisseki_kakunin,
                                             "lastday": lastday,
                                             "lastday_sec": lastday_sec,
                                             "lastday_third": lastday_third,
                                             "today": today,
                                             "firstday": firstday,
                                             "secondday": secondday,
                                             "thirdday": thirdday,
                                             "firstday": firstday,
                                             "is_yotei_visible": is_yotei_visible,
                                             "is_jisseki_visible": is_jisseki_visible,
                                             "shucchou_yotei": shucchou_yotei,
                                             "shucchou_jisseki": shucchou_jisseki,
                                             })


def saveshucchou_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    add_to_Btrip = Btrip(
        edit_username=username,
        type=("予定"),
        created_month=month,
        B_money=(request.POST["B_money"]),
        gout=(request.POST["gout"]),
        done=True,
        Month=nextmonth,
    )

    add_to_Btrip.save()

    return redirect("moveToshucchou")


def deleteshucchou_yotei(request):
    username = request.user.username
    dateToday = datetime.date.today()
    type = ("予定")
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    delete_Kintai = Btrip.objects.all().filter(Month=nextmonth, edit_username=username, type=type)
    delete_Kintai.delete()

    return redirect("moveToshucchou")


def saveshucchou_jisseki(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    add_to_btrip = Btrip(
        edit_username=username,
        type=("実績"),
        B_money=(request.POST["B_money"]),
        gout=(request.POST["gout"]),
        created_month=month,
        done=True,
        Month=previousmonth,
    )

    add_to_btrip.save()

    return redirect("moveToshucchou")


def deleteshucchou_jisseki(request):
    username = request.user.username
    dateToday = datetime.date.today()
    type = ("実績")
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    delete_Kintai = Btrip.objects.all().filter(Month=previousmonth, edit_username=username, type=type)
    delete_Kintai.delete()

    return redirect("moveToshucchou")


# confirm form

def moveToConfirm(request):
    username = request.user.username
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    # dateToday_previous = dateToday-datetime.timedelta(10)
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]

    kintai_yotei = Kintai.objects.all().filter(created_month=month, type="予定")
    kintai_jisseki = Kintai.objects.all().filter(created_month=month, type="実績")
    shucchou_yotei = Btrip.objects.all().filter(created_month=month, type="予定")
    shucchou_jisseki = Btrip.objects.all().filter(created_month=month, type="実績")

    kintai_all = Kintai.objects.all().filter(created_month=month)
    shucchou_all = Btrip.objects.all().filter(created_month=month)
    user_list = User.objects.values_list('username', flat=True).distinct()
    print("userlist-", user_list)
    today = datetime.date.today()

    firstday = datetime.date.today().replace(day=1)

    def last_day_of_month(date):
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month + 1, day=1) - datetime.timedelta(days=1)

    print("last day-", last_day_of_month(dateToday))
    print("today-", today)
    print("first day-", firstday)

    lastday = last_day_of_month(dateToday)
    dateToday = datetime.date.today()
    month = dateToday.strftime('%B')
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]

    print("previousmonth-", previousmonth)
    print("thismonth", month)
    print("nextmonth", nextmonth)

    return render(request, "confirm.html", {
        "kintai_yotei": kintai_yotei,
        "kintai_jisseki": kintai_jisseki,
        "shucchou_yotei": shucchou_yotei,
        "shucchou_jisseki": shucchou_jisseki,
        "user_list": user_list,
        "kintai_all": kintai_all,
        "shucchou_all": shucchou_all,
        "lastday": lastday,
        "today": today,
        "firstday": firstday,
    })


def shucchou_kakunin(request, kakunin_id):
    is_kakunin_ok = Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = True
    is_kakunin_ok.done = True
    is_kakunin_ok.save()
    return redirect("moveToConfirm")


def shucchou_sashimodoshi(request, kakunin_id):
    is_kakunin_ok = Btrip.objects.get(id=kakunin_id)
    is_kakunin_ok.kakunin = False
    is_kakunin_ok.done = False
    is_kakunin_ok.save()
    return redirect("moveToConfirm")


def confirm_all_kintai(request):
    confirm_cursor = connection.cursor()
    confirm_cursor.execute('UPDATE useractivities_kintai set kakunin=True, done=True;')
    return redirect("moveToConfirm")


def confirm_all_shucchou(request):
    confirm_cursor = connection.cursor()
    confirm_cursor.execute('UPDATE useractivities_btrip set kakunin=True, done=True;')
    return redirect("moveToConfirm")


def viewKintai_yotei(request, username):
    dateToday = datetime.date.today()
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    value_yotei = Kintai.objects.values_list('teiji', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                        type="予定", ).reverse()
    value_overtime_yotei = Kintai.objects.values_list('overtime', flat=True).filter(Month=nextmonth,
                                                                                    edit_username=username, type="予定", )

    return render(request, "view_hover/kintai_view_yotei.html", {"yotei": value_yotei,
                                                                 "overtime_yotei": value_overtime_yotei,
                                                                 })


def viewKintai_jisseki(request, username):
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    value_jisseki = Kintai.objects.values_list('teiji', flat=True).filter(Month=previousmonth, edit_username=username,
                                                                          type="実績", ).reverse()
    value_overtime_jisseki = Kintai.objects.values_list('overtime', flat=True).filter(Month=previousmonth,
                                                                                      edit_username=username,
                                                                                      type="実績", )
    print("jisseki----", value_jisseki)
    return render(request, "view_hover/kintai_view_jisseki.html", {"jisseki": value_jisseki,
                                                                   "overtime_jisseki": value_overtime_jisseki,
                                                                   })


def viewShucchou_yotei(request, username):
    dateToday = datetime.date.today()
    dateToday_next = dateToday + datetime.timedelta(31)
    nextmonth = dateToday_next.strftime('%B')
    value_yotei = Btrip.objects.values_list('B_money', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                         type="予定", ).reverse()
    value_overtime_yotei = Btrip.objects.values_list('gout', flat=True).filter(Month=nextmonth, edit_username=username,
                                                                               type="予定", )

    return render(request, "view_hover/shucchou_view_yotei.html", {"yotei": value_yotei,
                                                                   "overtime_yotei": value_overtime_yotei,
                                                                   })


def viewShucchou_jisseki(request, username):
    now = datetime.datetime.now()
    previousmonth_1 = now.month - 1 if now.month > 1 else 12
    previousmonth = calendar.month_name[previousmonth_1]
    value_jisseki = Btrip.objects.values_list('B_money', flat=True).filter(Month=previousmonth, edit_username=username,
                                                                           type="実績", ).reverse()
    value_overtime_jisseki = Btrip.objects.values_list('gout', flat=True).filter(Month=previousmonth,
                                                                                 edit_username=username, type="実績", )
    print("jisseki----", value_jisseki)
    return render(request, "view_hover/shucchou_view_jisseki.html", {"jisseki": value_jisseki,
                                                                     "overtime_jisseki": value_overtime_jisseki,
                                                                     })

# notify if everyone done
