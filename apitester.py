from locust import HttpLocust, TaskSet, between
import requests
from pymongo import MongoClient
from dbhandler import *

initUsers()

active_users = []

def cmd_get_task_list(l):
    pass

class UserTask(TaskSet):
    tasks = {cmd_get_task_list:1}
    def on_start(self):
        print("UserTask.on_start")
        self.game_handle()
        pass

    def on_stop(self):
        print("UserTask.on_stop")
        pass

    def game_handle(self):
        user = chose_user()
        r = requests.get(GameHandlerUrl.format(user.account, user.agentid))
        if r.status_code == 200:
            result = json.loads(r.content)
            if result["data"]["code"] == 0:
                tu = result["data"]["url"]
                tu = urllib.parse.urlparse(tu)
                tu = urllib.parse.parse_qs(tu.query)
                descode = tu["descode"][0]
                token = tu["token"][0]
                hallserver = tu["domain"][0]
                hallport = tu["port"][0]
                user.set_proxy_info(hallserver, hallport)
                self.token_handle(token, descode,user)
        else:
            print("GameHandle failed, status_code:{}".format(r.status_code))
            pass

    def token_handle(self,token,descode,user):
        r = requests.get(TokenHandlerUrl.format(token, descode))
        if r.status_code == 200:
            result = r.content.split("=")[1]
            user.login(result)
        pass

class GameUser(HttpLocust):
    print("GameUser")
    task_set = UserTask
    wait_time = between(5.0,9.0)