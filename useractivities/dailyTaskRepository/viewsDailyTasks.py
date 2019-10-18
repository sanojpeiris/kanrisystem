from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import TaskItem
from django.db import connection


def moveToLogin(request):
    return render(request, "login.html")


def moveToTodo(request):
    all_todo_items = TaskItem.objects.all()
    category_yesterday = TaskItem.objects.values_list(
        'category_yesterday', flat=True).distinct()
    category_today = TaskItem.objects.values_list(
        'category_today', flat=True).distinct()
    category_bad = TaskItem.objects.values_list(
        'category_bad', flat=True).distinct()
    category_other = TaskItem.objects.values_list(
        'category_other', flat=True).distinct()
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    username = request.user.username
    cursor1.execute(
        "SELECT category_today  from useractivities_taskitem where date =(select max(date) from useractivities_taskitem WHERE date < DATE('now') )  and edit_username = %s",
        [username])
    cursor2.execute(
        "SELECT today from useractivities_taskitem where date =(select max(date) from useractivities_taskitem WHERE date < DATE('now') )  and edit_username = %s",
        [username])

    row_category_today = cursor1.fetchone()
    row_today = cursor2.fetchone()

    return render(request, "todo.html", {"all_items": all_todo_items,
                                         "category_yesterday": category_yesterday,
                                         "category_today": category_today,
                                         "category_bad": category_bad,
                                         "category_other": category_other,
                                         "category_yesterday_con": row_category_today,
                                         "yesterday_con": row_today,
                                         })


def moveToHistory(request):
    all_todo_items = TaskItem.objects.all()
    all_user_items = User.objects.all()
    return render(request, "history.html", {"all_items": all_todo_items, "all_user_items": all_user_items})


def taskView(request):
    dateToday = datetime.date.today()
    all_todo_items = TaskItem.objects.all()
    return render(request, "home.html", {"all_items": all_todo_items,
                                         "dateToday": dateToday,
                                         })


def viewHistory(request):
    all_todo_items = TaskItem.objects.all()
    all_user_items = User.objects.all()
    # today = TodoItem.objects.values("today")

    if request.method == "POST":
        username_op = request.POST["user"]
        category_op = request.POST["category_today"]
        period_op = request.POST["period"]
        today = TaskItem.objects.filter(edit_username=username_op)
        category_today = TaskItem.objects.filter(edit_username=username_op)
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
    new_item = TaskItem(
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
    return redirect("taskView")


def saveTask(request, todo_id):
    username1 = request.user.username
    new_item = TaskItem(
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
    new_item.save(todo_id)
    # item_to_save = TaskItem.objects.get(new_item)
    # item_to_save.save(todo_id)
    return redirect("deleteTodo", todo_id)


# password = User.objects.get(id=userId)
# password.set_password(password1)
# password.save()

def deleteTodo(request, todo_id):
    item_to_delete = TaskItem.objects.get(id=todo_id)
    item_to_delete.delete()
    return redirect("taskView")


def saveTodo(request, todo_id):
    item_to_save = TaskItem.objects.get(id=todo_id)
    item_to_save.save()
    return redirect("taskView")


def search(request):
    task_list = TaskItem.objects.all()
    task_filter = TaskFilter(request.POST, queryset=task_list)
    user_list = TaskItem.objects.values_list(
        'edit_username', flat=True).distinct()
    category_list = TaskItem.objects.values_list(
        'category_today', flat=True).distinct()
    date_list = TaskItem.objects.values_list('date', flat=True).distinct()
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



