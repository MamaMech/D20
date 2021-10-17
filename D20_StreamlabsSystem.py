# ---------------------------
#   Import Libraries
# ---------------------------
import os
import sys
import json
import codecs
import clr
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))  # point at lib folder for classes / references

clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

# Import your Settings class
# from Settings_Module import MySettings

# ---------------------------
#   [Required] Script Information
# ---------------------------

ScriptName = "D20"
Website = "https://www.twitch.tv/mamamech"
Description = "TODO"
Creator = "MamaMech"
Version = "1.0.0"

# ---------------------------
#   [Required] Initialize Data (Only called on load)
# ---------------------------
def Init():
    return
# ---------------------------
#   Dictionaries
# ---------------------------

HP = 100
currentHP = HP

# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    global currentHP
    if data.IsChatMessage() and data.GetParam(0).lower() == "!d20":
        if currentHP > 0:
            roll = random.randint(1, 40)
            if roll == 20:
                damage = random.randint(1, 24) + random.randint(1, 24)
                currentHP = currentHP - damage
                Parent.SendStreamMessage(
                    "You hit with a " + str(roll) + "! You're damage is doubled and you did " + str(damage) + " HP worth of damage.")
                if currentHP <= 0:
                    Parent.SendStreamMessage("You killed the monster! Congrats!")
            elif roll == 1:
                damage = random.randint(1, 12) + random.randint(1, 12)
                currentHP = currentHP + damage
                Parent.SendStreamMessage("You missed with a " + str(roll) + "! That's a nat 1! The monster is healed by " + str(damage) + "HP! Bummer :(")
            elif roll >= 10:
                damage = random.randint(1, 12) + random.randint(1, 12)
                currentHP = currentHP - damage
                Parent.SendStreamMessage("You hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage.")
                if currentHP <= 0:
                    Parent.SendStreamMessage("You killed the monster! Congrats!")
            elif roll < 10:
                Parent.SendStreamMessage("You missed with a " + str(roll) + "!")
        elif currentHP <= 0:
            Parent.SendStreamMessage("The monster is dead!")
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!hp":
        if currentHP >= 75:
            Parent.SendStreamMessage("The monster has taken a few hits, but has a lot of fight let.")
        elif currentHP >= 50:
            Parent.SendStreamMessage("The monster is officially bloodied! It's breathing heavily, but it's not backing down.")
        elif currentHP >= 25:
            Parent.SendStreamMessage("The monster is looking rough. It's energy is low and showing signs of weakness. Victory is in sight!")
    elif data.IsChatMessage() and data.GetParam(0).lower() =="!resethp" and Parent.HasPermission(data.User, "Moderator", ""):
        currentHP = 100
        Parent.SendStreamMessage("The HP has been reset.")

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return

# ---------------------------
#   [Required] Test Code
# ---------------------------

# class Data:
#     message = ""
#     User = "Sierra"
#     UserName = "MamaMech"
#
#     def __init__(self, message):
#         self.message = message
#
#     def IsChatMessage(self):
#         return True
#
#     def GetParam(self, index):
#         try:
#             return self.message.split()[index]
#         except:
#             return ""
#
# class Parent:
#     user_points = 5000
#     user_is_mod = True
#
#     def Log(self, message):
#         return
#
#     def SendStreamMessage(self, message):
#         print(message)
#
#     def GetPoints(self, user):
#         return self.user_points
#
#     def RemovePoints(self, user, user_name, point_cost):
#         self.user_points = 5000 - point_cost
#
#     def HasPermission(self, user, perm, ignore):
#         return self.user_is_mod
#
#
# Init()
# Parent = Parent()
# while True:
#     msg = Data(raw_input())
#     Execute(msg)