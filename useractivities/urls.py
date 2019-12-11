from django.urls import path

from useractivities.dailyTaskRepository import viewsDailyTasks
from useractivities.userRepository import viewsUser
from useractivities.jinkenhiRepository import viewsJinkenhi

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
    path("moveToJinkenhi", viewsJinkenhi.moveToJinkenhi, name="moveToJinkenhi"),
    path("moveToshucchou", viewsJinkenhi.moveToshucchou, name="moveToshucchou"),
    path("moveToKintai", viewsJinkenhi.moveToKintai, name="moveToKintai"),
    path("moveToConfirm", viewsJinkenhi.moveToConfirm, name="moveToConfirm"),
    path("updatePassword", viewsUser.updatePassword, name="updatePassword"),
    path("closeWindow", viewsUser.closeWindow, name="closeWindow"),
    path("search", viewsDailyTasks.search, name="search"),
    path("base", viewsDailyTasks.moveToSearch, name="moveToSearch"),
    path("saveTodo/<int:todo_id>", viewsDailyTasks.saveTodo, name="saveTodo"),
    path("addrow/<int:todo_id>", viewsDailyTasks.addrow, name="addrow"),
    path("sendMessage",viewsDailyTasks.sendMessage,name="sendMessage"),
    path("saveState/<int:message_id>", viewsDailyTasks.saveState, name="saveState"),
    path("deleteState/<int:message_id>", viewsDailyTasks.deleteState, name="deleteState"),
    path("notification_is/<int:message_id>", viewsDailyTasks.notification_is, name="notification_is"),
    path("saveKintai/yotei", viewsJinkenhi.saveKintai_yotei, name="saveKintai_yotei"),
    path("deleteKintai/yotei", viewsJinkenhi.deleteKintai_yotei, name="deleteKintai_yotei"),
    path("saveKintai/jisseki", viewsJinkenhi.saveKintai_jisseki, name="saveKintai_yotei"),
    path("deleteKintai/jisseki", viewsJinkenhi.deleteKintai_jisseki, name="deleteKintai_yotei"),
    path("saveshucchou/yotei", viewsJinkenhi.saveshucchou_yotei, name="saveshucchou_yotei"),
    path("deleteshucchou/yotei", viewsJinkenhi.deleteshucchou_yotei, name="deleteshucchou_yotei"),
    path("saveshucchou/jisseki", viewsJinkenhi.saveshucchou_jisseki, name="saveshucchou_yotei"),
    path("deleteshucchou/jisseki", viewsJinkenhi.deleteshucchou_jisseki, name="deleteshucchou_yotei"),
    path("kintai_kakunin/<int:kakunin_id>", viewsJinkenhi.kintai_kakunin, name="kintai_kakunin"),
    path("kintai_sashimodoshi/<int:kakunin_id>", viewsJinkenhi.kintai_sashimodoshi, name="kintai_sashimodoshi"),
    path("shucchou_kakunin/<int:kakunin_id>", viewsJinkenhi.shucchou_kakunin, name="shucchou_kakunin"),
    path("shucchou_sashimodoshi/<int:kakunin_id>", viewsJinkenhi.shucchou_sashimodoshi, name="shucchou_sashimodoshi"),
    path("confirm_all_kintai", viewsJinkenhi.confirm_all_kintai, name="confirm_all_kintai"),
    path("confirm_all_shucchou", viewsJinkenhi.confirm_all_shucchou, name="confirm_all_shucchou"),

    path("viewKintai_yotei/<str:username>", viewsJinkenhi.viewKintai_yotei, name="viewKintai_yotei"),
    path("viewKintai_jisseki/<str:username>", viewsJinkenhi.viewKintai_jisseki, name="viewKintai_jisseki"),
    path("viewShucchou_yotei/<str:username>", viewsJinkenhi.viewShucchou_yotei, name="viewShucchou_yotei"),
    path("viewShucchou_jisseki/<str:username>", viewsJinkenhi.viewShucchou_jisseki, name="viewShucchou_jisseki"),

    path("chat",viewsDailyTasks.chat,name="chat"),



]
