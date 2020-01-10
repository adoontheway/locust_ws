from pymongo import MongoClient
import requests
import json
import asyncio
# import urllib
import utils
import urllib.parse
import websockets
import inet
# import struct
# import struct_pb2

from Game import Common_pb2 as GameCommon
from HallServer import Message_pb2 as HallMsg

GameHandlerUrl = "http://192.168.2.214:8088/GameHandle?testAccount={}&agentid={}"
TokenHandlerUrl = "http://192.168.2.214:8088/TokenHandle?token={}&descode={}"

user_list = []
active_userids = []
class User():
    def __init__(self,userid,account,agentid):
        self.userid = userid
        self.account = account
        self.agentid = agentid
        header = GameCommon.Header()
        header.sign = 0x5f5f
        self.header = header
        pass
    def set_proxy_info(self,halladdr,hallport):
        self.hallserver = halladdr
        self.hallserver = "192.168.2.91"
        self.hallport = hallport
        pass
    async def login(self,token):
        async with websockets.connect("ws://{}:{}".format(self.hallserver,self.hallport)) as websocket:
            login_msg = HallMsg.LoginMessage()
            login_msg.session = token
            header = login_msg.header
            header.sign = 0x5f5f
            iheader = inet.UHeader()
            iheader.mainId = GameCommon.MAIN_MESSAGE_CLIENT_TO_HALL
            iheader.subId = GameCommon.CLIENT_TO_HALL_LOGIN_MESSAGE_REQ
            iheader.encode(login_msg.SerializeToString())
            await websocket.send(login_msg.SerializeToString())
            result = await websocket.recv()
            print(result)
        pass

def initUsers():
    mclient = MongoClient("mongodb://192.168.2.97:27017")
    db = mclient.gamemain
    user_coll = db.game_user
    for user in user_coll.find({"userid":{"$lt":450000}}).limit(100):
        user_list.append(User(user["userid"], user["account"],user["agentid"]))

def chose_user():
    for user in user_list:
        if user.userid not in active_userids:
            active_userids.append(user.userid)
            return user

def chose_active_one():
    pass

if __name__ == "__main__":
    initUsers()
    user = chose_user()
    r = requests.get(GameHandlerUrl.format(user.account, user.agentid))
    if r.status_code == 200:
        result = json.loads(r.content)
        if result["data"]["code"] == 0:
            tu = result["data"]["url"]
            print("raw:",tu)
            tu = urllib.parse.urlparse(tu)
            tu = urllib.parse.parse_qs(tu.query)
            # print(tu)
            descode = tu["descode"][0]
            token = urllib.parse.quote(tu["token"][0])
            hallserver = tu["domain"][0]
            hallport = tu["port"][0]
            user.set_proxy_info(hallserver, hallport)
            tu = TokenHandlerUrl.format(token, descode)
            print("request:",tu)
            r = requests.get(tu)
            if r.status_code == 200:
                result = str(r.content).split("=")[1]
                loop = asyncio.get_event_loop()
                loop.run_until_complete(user.login(result))
            else:
                print("TokenHandle failed, status:{}, stack:{}".format(r.status_code,r.reason))
    else:
        print("GameHandle failed, status_code:{}".format(r.status_code))
    print(user)