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
    path("deleteTodo/<int:todo_id>", viewsDailyTasks.deleteTodo, name="deleteTodo"),
    path("back", viewsDailyTasks.back, name="back"),
    path("moveToUpdatePassword", viewsUser.moveToUpdatePassword, name="moveToUpdatePassword"),
    path("updatePassword", viewsUser.updatePassword, name="updatePassword"),
    path("closeWindow", viewsUser.closeWindow, name="closeWindow"),
    path("moveToHistory", viewsDailyTasks.moveToHistory, name="moveToHistory"),
    path("viewHistory", viewsDailyTasks.viewHistory, name="viewHistory"),
    path("search", viewsDailyTasks.search, name="search"),
    path("moveToSearch", viewsDailyTasks.moveToSearch, name="moveToSearch"),
    path("saveTodo/<int:todo_id>", viewsDailyTasks.saveTodo, name="saveTodo"),





]
