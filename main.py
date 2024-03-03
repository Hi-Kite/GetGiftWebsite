from flask import Flask, render_template, request
from mcrcon import MCRcon
import atexit

@atexit.register
def close():
    mcr.disconnect()
    print("[RCON] 关闭连接。")

ip = ""
password = ""
port = ""

haveGiftUsernamesFileName = "HaveGiftUsernames.txt"

mcr = MCRcon(ip, password, port)
mcr.connect()
print("[RCON] 连接成功！")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/xinshoulibao", methods=["GET"])
def xinshoulibao():
    username = request.args.get("username")
    if (username == None or username == ""):
        return "出错。"
    with open(haveGiftUsernamesFileName, "r") as file:
        for line in file:
            if (line == "{}\n".format(username)):
                return "您已经领取过新手礼包了！"
    
    text1 = "{} has the following entity data: \"minecraft:dirt\"".format(username)
    text2 = "Gave 1 [Diamond] to {}".format(username)
    
    if (mcr.command("data get entity {} Inventory[{{Slot:0b}}].id".format(username)) == text1):
        if (mcr.command("give {} diamond 1".format(username)) == text2):
            with open(haveGiftUsernamesFileName, "a") as file:
                file.write("{}\n".format(username))
        else:
            return "领取失败！"
    else:
        return "请将1个泥土放到您的第一格物品栏（快捷栏第一格）。"
    return render_template("get.html", username = username)

app.run("0.0.0.0")