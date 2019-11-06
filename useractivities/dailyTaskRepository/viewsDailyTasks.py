from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import TaskItem, TaskProject, TaskType, TaskUser, TaskTable
from django.db import connection
from django.utils.timezone import localtime, now
from django.utils import timezone

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
        "SELECT category_today  from useractivities_taskitem where date =(select max(date) from "
        "useractivities_taskitem WHERE date < DATE('now') )  and edit_username = %s",
        [username])
    cursor2.execute(
        "SELECT today from useractivities_taskitem where date =(select max(date) from useractivities_taskitem WHERE "
        "date < DATE('now') )  and edit_username = %s", [username])

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


def taskView(request):
    dateToday = datetime.date.today()
    # username = request.user.username
    all_todo_items = TaskTable.objects.all().order_by('tasktype').distinct()
    all_user_items = TaskTable.objects.values_list('edit_username',flat=True).distinct()
    tasktypes = TaskTable.objects.values_list('tasktype', flat=True).distinct()
    all_time_items = TaskTable.objects.values_list('time', flat=True).distinct()
    color = ('blue', 'white', 'green', 'red')
    return render(request, "home.html", {"all_items": all_todo_items,
                                         "all_user_items": all_user_items,
                                         "all_time_items": all_time_items,
                                         "dateToday": dateToday,
                                         "tasktypes":tasktypes,
                                         "color":color,
                                         })


def back(request):
    return redirect('/')


def addTask(request):
    username = request.user.username

    add_to_project_yesterday = TaskTable(
        taskProject=(request.POST["category_yesterday"]), task=(request.POST["yesterday"]),
        tasktype=("1昨日やったこと"), edit_username=username)

    add_to_project_today = TaskTable(
        taskProject=(request.POST["category_today"]), task=(request.POST["today"]),
        tasktype=("2今日やること"), edit_username=username)

    add_to_project_bad = TaskTable(
        taskProject=(request.POST["category_bad"]), task=(request.POST["bad"]),
        tasktype=("3困っていること"), edit_username=username)

    add_to_project_other = TaskTable(
        taskProject=(request.POST["category_other"]), task=(request.POST["other"]),
        tasktype=("4その他"), edit_username=username)

    add_to_project_yesterday.save()
    add_to_project_today.save()
    add_to_project_bad.save()
    add_to_project_other.save()

    return redirect("taskView")

def addrow(request,todo_id):
    username = request.user.username
    dateToday = datetime.date.today()
    timenow=datetime.datetime.now().strftime('%H:%M:%S:%M')
    cursoradd = connection.cursor()

    cursor_Ttype = connection.cursor()
    cursor_Ttype.execute("SELECT tasktype FROM useractivities_tasktable WHERE id=%s", [todo_id])
    task_type = cursor_Ttype.fetchone()[0]

    cursoradd.execute("INSERT INTO useractivities_tasktable (edit_username, taskProject, tasktype, task,date,time)VALUES (%s,'',%s,'',%s,%s)",[username,task_type,dateToday,timenow])

    return redirect("taskView")


def saveTask(request, todo_id):
    username = request.user.username
    cursor_Ttype = connection.cursor()
    cursor_Ttype.execute("SELECT tasktype FROM useractivities_tasktable WHERE id=%s", [todo_id])
    task_type = cursor_Ttype.fetchone()[0]

    save_new_data = TaskTable(
        taskProject=(request.POST["category%d" % todo_id]), task=(request.POST["yesterday%d" % todo_id]),
        tasktype=(task_type), edit_username=username)

    save_new_data.save(todo_id)
    return redirect("deleteTask_id", todo_id)


def deleteTask(request, user):
    dateToday = datetime.date.today()
    cursor_delete = connection.cursor()
    cursor_delete.execute("DELETE FROM useractivities_tasktable WHERE edit_username=%s and date=%s", [user,dateToday])
    return redirect("taskView")


def deleteTask_id(request, todo_id):
    cursor_delete = connection.cursor()
    cursor_delete.execute("DELETE FROM useractivities_tasktable WHERE id=%s", [todo_id])
    return redirect("taskView")


def saveTodo(request, todo_id):
    item_to_save = TaskItem.objects.get(id=todo_id)
    item_to_save.save()
    return redirect("taskView")


def search(request):
    cursor_Ttype = connection.cursor()
    cursor_Ttype.execute("SELECT DISTINCT taskproject FROM useractivities_tasktable WHERE tasktype='2今日やること'")
    tuple_project = cursor_Ttype.fetchall()
    taskproject_list=[i[0] for i in tuple_project] #to make the tuple to a queryset(to remove comma and brackets)
    print(taskproject_list)
    task_list = TaskTable.objects.all()
    task_filter = TaskFilter(request.POST, queryset=task_list)
    user_list = TaskTable.objects.values_list(
        'edit_username', flat=True).distinct()
    # category_list = TaskTable.objects.values_list(
    #     'taskProject', flat=True).distinct()
    date_list = TaskTable.objects.values_list('date', flat=True).distinct()
    type_list = TaskTable.objects.values_list('tasktype', flat=True).distinct()
    print(user_list)
    return render(request, "search/user_list.html",
                  {"filter": task_filter,
                   "user_list": user_list,
                   "category_list": taskproject_list,
                   "type_list": type_list,
                   "date_list": date_list, }
                  )


def moveToSearch(request):
    # task_list = TodoItem.objects.all()
    # task_filter = TaskFilter(request.POST, queryset=task_list)
    return render(request, "search/user_list.html")
