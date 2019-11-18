from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
from useractivities.filters import TaskFilter
from useractivities.userRepository.models import  TaskTable,TaskMessage
from django.db import connection
from django.utils.timezone import localtime, now
from django.utils import timezone

def moveToLogin(request):
    return render(request, "login.html")


def moveToTodo(request):
    username = request.user.username
    user_list=TaskTable.objects.values_list('edit_username',flat=True).distinct()
    dateToday = datetime.date.today()
    all_todo_items = TaskTable.objects.all()
    taskproject = TaskTable.objects.values_list(
        'taskProject', flat=True).distinct()
    allmessages = TaskMessage.objects.values_list(
        'message', flat=True).distinct()
    spec_user_list = TaskMessage.objects.values_list(
        'spec_user', flat=True).distinct()

    cursoruser=connection.cursor()
    cursoruser.execute("select distinct edit_username from useractivities_tasktable where date=DATE('now') and edit_username=%s",[username])
    today_user=cursoruser.fetchone()

    print("logged user-",today_user)
    cursor1 = connection.cursor()
    cursor2 = connection.cursor()
    cursor1.execute(
        "SELECT taskProject  from useractivities_tasktable where date =(select max(date) from "
        "useractivities_tasktable WHERE date < DATE('now') ) and tasktype='2今日やること' and edit_username = %s",
        [username])
    cursor2.execute(
        "SELECT task from useractivities_tasktable where date =(select max(date) from useractivities_tasktable WHERE "
        "date < DATE('now') ) and tasktype='2今日やること' and edit_username = %s", [username])

    messages=TaskMessage.objects.all()
    messages_2=TaskMessage.objects.all().filter(visible=True)
    visible=TaskMessage.objects.values_list(
        'visible', flat=True).distinct()
    print("visibleis ",visible)

    row_category_today_old = cursor1.fetchall()
    row_today_old = cursor2.fetchall()

    row_category_today=[i[0] for i in row_category_today_old]
    row_today=[i[0] for i in row_today_old]
    print(row_category_today)
    checked="checked"
    return render(request, "todo.html", {"all_items": all_todo_items,
                                         "taskproject": taskproject,
                                         "category_yesterday_con": row_category_today,
                                         "yesterday_con": row_today,
                                         "messages":messages,
                                         "messages_2":messages_2,
                                         "visibility":visible,
                                         "allmessages":allmessages,
                                         "is_checked":checked,
                                         "today_user":today_user,
                                         "user_list":user_list,
                                         "spec_user_list":spec_user_list,
                                         })


def taskView(request):
    dateToday = datetime.date.today()
    username = request.user.username
    taskproject = TaskTable.objects.values_list(
        'taskProject', flat=True).distinct()
    all_todo_items = TaskTable.objects.all()

    all_todo_items_yesterday = TaskTable.objects.all().filter(tasktype='1昨日やったこと',date=dateToday).distinct()
    all_todo_items_today = TaskTable.objects.all().filter(tasktype='2今日やること',date=dateToday).distinct()
    all_todo_items_bad= TaskTable.objects.all().filter(tasktype='3困っていること',date=dateToday).distinct()
    all_todo_items_other = TaskTable.objects.all().filter(tasktype='4その他',date=dateToday).distinct()   
    user_today=TaskTable.objects.values_list('edit_username',flat=True).order_by('date').filter(date=dateToday).distinct()

    deletebtnyesterday=TaskTable.objects.filter(date=dateToday,edit_username=username,tasktype='1昨日やったこと').count()
    deletebtntoday=TaskTable.objects.filter(date=dateToday,edit_username=username,tasktype='2今日やること').count()
    deletebtnbad=TaskTable.objects.filter(date=dateToday,edit_username=username,tasktype='3困っていること').count()
    deletebtnother=TaskTable.objects.filter(date=dateToday,edit_username=username,tasktype='4その他').count()
    
    messages=TaskMessage.objects.all().filter(visible=True)
    return render(request, "home.html", {
                                        "all_items_yesterday": all_todo_items_yesterday,
                                        "all_items_today": all_todo_items_today,
                                        "all_items_bad": all_todo_items_bad,
                                        "all_items_other": all_todo_items_other,
                                        "all_items": all_todo_items,
                                         "taskproject": taskproject,
                                         "deletebtncount_yesterday":deletebtnyesterday,
                                         "deletebtncount_yesterday":deletebtnyesterday,
                                         "deletebtncount_today":deletebtntoday,
                                         "deletebtncount_bad":deletebtnbad,
                                         "deletebtncount_other":deletebtnother,
                                         "user_today":user_today,
                                         "messages":messages,
                                         })


def back(request):
    return redirect('/')

def sendMessage(request):
    username = request.user.username
  
    add_to_message=TaskMessage(
        edit_username=username,
        message=(request.POST["message"]),
        spec_user=(request.POST["spec_user"]),
    )
    add_to_message.save()

    return redirect("moveToTodo")

def saveState(request,message_id):
    message1=connection.cursor()
    message1.execute("SELECT message from useractivities_taskmessage where id=%s",[message_id])
    message=message1.fetchone()[0]
    print("message-",message)

    is_visible = request.POST["message%d" % message_id] 
    spec_user = request.POST["senduser%d" % message_id] 
    if is_visible == "visible":
        visible = True
        makevisible=TaskMessage.objects.get(id=message_id)
        makevisible.visible = visible
        makevisible.spec_user = spec_user
        makevisible.save()
        return redirect("moveToTodo")
    else:
        invisible = False
        makeinvisible=TaskMessage.objects.get(id=message_id)
        makeinvisible.visible = invisible
        makeinvisible.spec_user = spec_user
        makeinvisible.save()
        return redirect("moveToTodo")

def deleteState(request, message_id):
    cursor_delete = connection.cursor()
    cursor_delete.execute("DELETE  FROM useractivities_taskmessage WHERE id=%s", [message_id])
    return redirect("moveToTodo")

def addTask(request):
    username = request.user.username

    add_to_project_yesterday = TaskTable(
        taskProject=(request.POST["category_yesterday"]), 
        task=(request.POST["yesterday"]),
        tasktype=("1昨日やったこと"), edit_username=username)

    add_to_project_today = TaskTable(
        taskProject=(request.POST["category_today"]), 
        task=(request.POST["today"]),
        tasktype=("2今日やること"), edit_username=username)

    add_to_project_bad = TaskTable(
        taskProject=(request.POST["category_bad"]), 
        task=(request.POST["bad"]),
        tasktype=("3困っていること"), edit_username=username)

    add_to_project_other = TaskTable(
        taskProject=(request.POST["category_other"]), 
        task=(request.POST["other"]),
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
    print(task_type)

    cursoradd.execute("INSERT INTO useractivities_tasktable (edit_username, taskProject, tasktype, task,date,time)VALUES (%s,'',%s,'',%s,%s)",[username,task_type,dateToday,timenow])

    return redirect("taskView")

def addrow_task(request,todo_id):
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
    saveTask_row=TaskTable.objects.get(id=todo_id)
    saveTask_row.taskProject=request.POST["category%d" % todo_id] 
    saveTask_row.task=request.POST["yesterday%d" % todo_id]   
    saveTask_row.save()
    return redirect("taskView")


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
    taskproject_list=TaskTable.objects.values_list(
        'taskProject', flat=True).exclude(taskProject='').distinct()
    print('projectlist-',taskproject_list)
    task_list = TaskTable.objects.all()
    task_filter = TaskFilter(request.POST, queryset=task_list)
    user_list = TaskTable.objects.values_list(
        'edit_username', flat=True).distinct()
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
    return render(request, "base.html")
