from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import TodoItem
from django.db import connection

def moveToLogin(request):
    return render(request, "login.html")


def moveToTodo(request):
    all_todo_items = TodoItem.objects.all()
    category_yesterday = TodoItem.objects.values_list(
        'category_yesterday', flat=True).distinct()
    category_today = TodoItem.objects.values_list(
        'category_today', flat=True).distinct()
    category_bad = TodoItem.objects.values_list(
        'category_bad', flat=True).distinct()
    category_other = TodoItem.objects.values_list(
        'category_other', flat=True).distinct()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor1.execute("SELECT category_today from useractivities_todoitem where date = (select max(date) from useractivities_todoitem WHERE date < DATE('now') )")
    cursor2.execute("SELECT today from useractivities_todoitem where date = (select max(date) from useractivities_todoitem WHERE date < DATE('now') )")

    row_category_today = cursor1.fetchone()
    row_today = cursor2.fetchone()
    return render(request, "todo.html", {"all_items": all_todo_items,
                                         "category_yesterday": category_yesterday,
                                         "category_today": category_today,
                                         "category_bad": category_bad,
                                         "category_other": category_other,
                                         "category_yesterday_con":row_category_today,
                                         "yesterday_con":row_today,
                                         })


def moveToHistory(request):
    all_todo_items = TodoItem.objects.all()
    all_user_items = User.objects.all()
    return render(request, "history.html", {"all_items": all_todo_items, "all_user_items": all_user_items})


def taskView(request):
    dateToday = datetime.date.today()
    all_todo_items = TodoItem.objects.all()
    return render(request, "home.html", {"all_items": all_todo_items,
                                         "dateToday": dateToday,
                                         })


def viewHistory(request):
    all_todo_items = TodoItem.objects.all()
    all_user_items = User.objects.all()
    # today = TodoItem.objects.values("today")

    if request.method == "POST":
        username_op = request.POST["user"]
        category_op = request.POST["category_today"]
        period_op = request.POST["period"]
        today = TodoItem.objects.filter(edit_username=username_op)
        category_today = TodoItem.objects.filter(edit_username=username_op)
        # if category_op == category:
        return render(request, "history.html", {"today_items": today,
                                                "category_items": category_today,
                                                "username_op": username_op,
                                                "category_op": category_op,
                                                "period_op": period_op,
                                                "all_items": all_todo_items,
                                                "all_user_items": all_user_items
                                                })

    else:
        return redirect(moveToHistory)


def back(request):
    return redirect('/')


def addTask(request):
    username1 = request.user.username
    new_item = TodoItem(
        # edit_username=username1,
        # category=request.POST.getlist("category"),
        # content=request.POST.getlist("content"),
        # variety="today",
        edit_username=username1,
        yesterday=request.POST["yesterday"],
        today=request.POST["today"],
        bad=request.POST["bad"],
        other=request.POST["other"],
        category_yesterday=request.POST["category_yesterday"],
        category_today=request.POST["category_today"],
        category_bad=request.POST["category_bad"],
        category_other=request.POST["category_other"],
    )
    new_item.save()
    return redirect("todoView")


def saveTask(request):
    yesterday = TodoItem(yesterday=request.POST["category_yesterday"])
    yesterday.save()
    return redirect("todoView")


def deleteTodo(request, todo_id):
    item_to_delete = TodoItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return redirect("todoView")


def search(request):
    task_list = TodoItem.objects.all()
    task_filter = TaskFilter(request.POST, queryset=task_list)
    user_list = TodoItem.objects.values_list(
        'edit_username', flat=True).distinct()
    category_list = TodoItem.objects.values_list(
        'category_today', flat=True).distinct()
    date_list = TodoItem.objects.values_list('date', flat=True).distinct()
    return render(request, "search/user_list.html",
                  {"filter": task_filter,
                   "user_list": user_list,
                   "category_list": category_list,
                   "date_list": date_list, }
                  )


def moveToSearch(request):
    # task_list = TodoItem.objects.all()
    # task_filter = TaskFilter(request.POST, queryset=task_list)
    return render(request, "search/user_list.html")

