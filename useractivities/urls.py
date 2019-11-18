from django.urls import path

from useractivities.dailyTaskRepository import viewsDailyTasks
from useractivities.userRepository import viewsUser

urlpatterns = [
    path("", viewsDailyTasks.moveToLogin, name="login"),
    path("register", viewsUser.register, name="register"),
    path("updateUser", viewsUser.updateUser, name="updateUser"),
    path("login", viewsUser.login, name="login"),
    path("logout", viewsUser.logout, name="logout"),
    path("home", viewsUser.moveToHome, name="home"),
    path("home_with_alert", viewsUser.homeAlert, name="home_with_alert"),
    path("moveToLogin", viewsDailyTasks.moveToLogin, name="moveToLogin"),
    path("moveToHome", viewsUser.moveToHome, name="moveToHome"),
    path("moveToRegister", viewsUser.moveToRegister, name="moveToRegister"),
    path("moveToUpdateUser", viewsUser.moveToUpdateUser, name="moveToUpdateUser"),
    path("moveToTodo", viewsDailyTasks.moveToTodo, name="moveToTodo"),
    path("taskView", viewsDailyTasks.taskView, name="taskView"),
    path("addTask", viewsDailyTasks.addTask, name="addTask"),
    path("saveTask/<int:todo_id>", viewsDailyTasks.saveTask, name="saveTask"),
    path("deleteTask/<str:user>", viewsDailyTasks.deleteTask, name="deleteTask"),
    path("deleteTask_id/<int:todo_id>", viewsDailyTasks.deleteTask_id, name="deleteTask_id"),
    path("back", viewsDailyTasks.back, name="back"),
    path("moveToUpdatePassword", viewsUser.moveToUpdatePassword, name="moveToUpdatePassword"),
    path("updatePassword", viewsUser.updatePassword, name="updatePassword"),
    path("closeWindow", viewsUser.closeWindow, name="closeWindow"),
    path("search", viewsDailyTasks.search, name="search"),
    path("base", viewsDailyTasks.moveToSearch, name="moveToSearch"),
    path("saveTodo/<int:todo_id>", viewsDailyTasks.saveTodo, name="saveTodo"),
    path("addrow/<int:todo_id>", viewsDailyTasks.addrow, name="addrow"),
    path("sendMessage",viewsDailyTasks.sendMessage,name="sendMessage"),
    path("saveState/<int:message_id>", viewsDailyTasks.saveState, name="saveState"),
    path("deleteState/<int:message_id>", viewsDailyTasks.deleteState, name="deleteState"),
    # path("addrow_task/<int:todo_id>", viewsDailyTasks.addrow_task, name="addrow_task"),





]
