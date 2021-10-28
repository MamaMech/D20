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
#   Functions
# ---------------------------
def get_hp():
    try:
        with open('monsterhp.txt') as file:
            lines = file.readlines()
            return int(lines[0])
    except:
        return 1000

HP = get_hp()
currentHP = HP


# ---------------------------
#   [Required] Execute Data / Process messages
# ---------------------------
def Execute(data):
    global currentHP
    if data.IsChatMessage() and data.GetParam(0).lower() == "!d20":
        inventory = get_user_inventory()
        if data.UserName not in inventory:
            setup_user(data.UserName)
        inventory = get_user_inventory()
        userinventory = inventory[data.UserName]
        if data.GetParam(1).lower() in userinventory:
            if currentHP > 0:
                roll = random.randint(1, 40)
                if roll == 20:
                    damage = get_damage(data.GetParam(1)) + get_damage(data.GetParam(1))
                    currentHP = currentHP - damage
                    write_hp(currentHP)
                    add_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " hit with a " + str(roll) + "! Your damage is doubled and you did " + str(damage) + " HP worth of damage" + " with a {}.".format(data.GetParam(1)) if data.GetParam(1) != "" else data.UserName + " hit with a " + str(roll) + "! Your damage is doubled and you did " + str(damage) + " HP worth of damage.")
                    # Also can be written as:
                    # Parent.SendStreamMessage("{} hit with a {}! Your damage is doulbed and you did {} HP worth of damage with a {}.".format(data.UserName, str(roll), str(damage), data.GetParam(1)))
                    if currentHP <= 0:
                        Parent.SendStreamMessage(data.UserName + " killed the monster! Congrats!")
                        dead_monster()
                elif roll == 1:
                    damage = get_damage(data.GetParam(1)) + get_damage(data.GetParam(1))
                    currentHP = currentHP + damage
                    write_hp(currentHP)
                    remove_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " missed with a " + str(roll) + "! That's a nat 1! The monster is healed by " + str(damage) + "HP! Bummer :(")
                elif roll >= 10:
                    damage = get_damage(data.GetParam(1))
                    currentHP = currentHP - damage
                    write_hp(currentHP)
                    add_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage" + " with a {}.".format(data.GetParam(1)) if data.GetParam(1) != "" else data.UserName + " hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage.")
                    if currentHP <= 0:
                        Parent.SendStreamMessage(data.UserName + " killed the monster! Congrats!")
                        dead_monster()
                elif roll < 10:
                    Parent.SendStreamMessage(data.UserName + " missed with a " + str(roll) + "!")
            elif currentHP <= 0:
                Parent.SendStreamMessage("The monster is dead and the code broke. Ask a mod to !resethp.")
        elif data.GetParam(1).lower() not in lootlist:
            if currentHP > 0:
                roll = random.randint(1, 40)
                if roll == 20:
                    damage = 2
                    currentHP = currentHP - damage
                    write_hp(currentHP)
                    add_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " hit with a " + str(roll) + "! Your damage is doubled and you did " + str(damage) + " HP worth of damage" + " with a {}.".format(data.GetParam(1)) if data.GetParam(1) != "" else data.UserName + " hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage.")
                    # Also can be written as:
                    # Parent.SendStreamMessage("{} hit with a {}! Your damage is doulbed and you did {} HP worth of damage with a {}.".format(data.UserName, str(roll), str(damage), data.GetParam(1)))
                    if currentHP <= 0:
                        Parent.SendStreamMessage(data.UserName + " killed the monster! Congrats!")
                        dead_monster()
                elif roll == 1:
                    damage = 2
                    currentHP = currentHP + damage
                    write_hp(currentHP)
                    remove_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " missed with a " + str(roll) + "! That's a nat 1! The monster is healed by " + str(damage) + "HP! Bummer :(")
                elif roll >= 10:
                    damage = 1
                    currentHP = currentHP - damage
                    write_hp(currentHP)
                    add_user_damage(data.UserName, damage)
                    Parent.SendStreamMessage(data.UserName + " hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage" + " with a {}.".format(data.GetParam(1)) if data.GetParam(1) != "" else data.UserName + " hit with a " + str(roll) + " and did " + str(damage) + " HP worth of damage.")
                    if currentHP <= 0:
                        Parent.SendStreamMessage(data.UserName + " killed the monster! Congrats!")
                        dead_monster()
                elif roll < 10:
                    Parent.SendStreamMessage(data.UserName + " missed with a " + str(roll) + "!")
            elif currentHP <= 0:
                Parent.SendStreamMessage("The monster is dead and the code broke. Ask a mod to !resethp.")
        elif data.GetParam(1).lower() in lootlist and data.GetParam(1).lower() not in userinventory:
            Parent.SendStreamMessage(data.UserName + ", you cannot use that weapon yet because it is not in your inventory. Check your inventory using \"!myinventory\".")
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!myinventory":
        inventory = get_user_inventory()
        userinventory = inventory[data.UserName]
        Parent.SendStreamMessage(", ".join(userinventory))
    elif data.IsChatMessage() and data.GetParam(0).lower() == "!hp":
        if currentHP >= 75:
            Parent.SendStreamMessage("The monster has taken a few hits, but has a lot of fight left.")
        elif currentHP >= 50:
            Parent.SendStreamMessage("The monster is officially bloodied! It's breathing heavily, but it's not backing down.")
        elif currentHP >= 25:
            Parent.SendStreamMessage("The monster is tired, but still pushing back.")
        elif currentHP >= 0:
            Parent.SendStreamMessage("The monster is looking rough. It's energy is low and showing signs of weakness. Victory is in sight!")
    elif data.IsChatMessage() and data.GetParam(0).lower() =="!resethp" and Parent.HasPermission(data.User, "Moderator", ""):
        currentHP = 1000
        write_hp(currentHP)
        remove_all_damage()
        Parent.SendStreamMessage("The HP has been reset.")
    elif data.IsChatMessage() and data.GetParam(0).lower() =="!aboutd20":
        Parent.SendStreamMessage("d20 is a minigame where you can use weapons to attack a general monster by typing \"!d20 (weapon)\" in the chat. You can check the monster's hp using \"!hp\" and you will get a general statement about it. All weapons are one word.")

# ---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
# ---------------------------
def Tick():
    return
# ---------------------------
#   [Required] Functions
# ---------------------------

def get_damage(weapon):
    if weapon == "dagger":
        return random.randint(1, 8)
    elif weapon == "staff":
        return random.randint(1, 12)
    elif weapon == "spell":
        return random.randint(1, 20)
    elif weapon == "bow":
        return random.randint(1, 12)
    elif weapon == "handaxe":
        return random.randint(1, 12)
    elif weapon == "scimitar":
        return random.randint(1, 12)
    elif weapon == "longsword":
        return random.randint(1, 16)
    elif weapon == "maul":
        return random.randint(1, 12) + random.randint(1, 12)
    elif weapon == "flail":
        return random.randint(1, 16)
    elif weapon == "warhammer":
        return random.randint(1, 16)
    elif weapon == "lance":
        return random.randint(1, 24)
    elif weapon == "greataxe":
        return random.randint(1, 24)
    elif weapon == "shortsword":
        return random.randint(1, 12)
    elif weapon == "glaive ":
        return random.randint(1, 20)
    elif weapon == "javelin":
        return random.randint(1, 12)
    elif weapon == "longbow":
        return random.randint(1, 16)
    elif weapon == "greatsword":
        return random.randint(1, 12) + random.randint(1, 12)
    elif weapon == "mastersword":
        return random.randint(1, 40)
    else:
        return 1


def write_hp(currenthp):
    with open('monsterhp.txt', 'w') as f:
        f.write(str(currenthp))

def get_user_damage():
    try:
        with open("damage.json") as f:
            return json.load(f)
    except:
        return {}
def add_user_damage(UserName, weapon_damage):
    dict_damage = get_user_damage()
    if UserName in dict_damage:
        dict_damage[UserName] = dict_damage[UserName] + weapon_damage
    else:
        dict_damage[UserName] = weapon_damage
    with open("damage.json", 'w') as f:
        json.dump(dict_damage, f)
def remove_user_damage(UserName, weapon_damage):
    dict_damage = get_user_damage()
    if UserName in dict_damage:
        dict_damage[UserName] = dict_damage[UserName] - weapon_damage
    else:
        dict_damage[UserName] = 0 - weapon_damage
    with open("damage.json", 'w') as f:
        json.dump(dict_damage, f)
def remove_all_damage():
    with open("damage.json", 'w') as f:
        json.dump({}, f)
def dead_monster():
    global currentHP
    dict_damage = get_user_damage()
    for username in dict_damage:
        add_inventory(username)
    message = ""
    for username, user_damage in dict_damage.items():
        message = message + str(username) + ":" + str(user_damage) + " "
    Parent.SendStreamMessage("Here's the damage table - " + message)
    Parent.SendStreamMessage("The monster's HP has been reset and anybody who contributed received a loot weapon. Use \"!myinventory\" to check what you got.")
    remove_all_damage()
    currentHP = 1000
    write_hp(1000)
def write_inventory(inventory):
    with open("d20inventory.json", 'w') as f:
        json.dump(inventory, f)
def get_user_inventory():
    try:
        with open("d20inventory.json") as f:
            return json.load(f)
    except:
        return {}
def add_inventory(username):
    inventory = get_user_inventory()
    if username not in inventory:
        setup_user()
        return write_inventory(inventory)
    elif username in inventory:
        userinventory = inventory[username]
        choices = []
        for item, weight in loot:
            choices.extend([item] * weight)
        weapon = random.choice(choices)
        userinventory.append(weapon)
        inventory[username] = userinventory
        write_inventory(inventory)
        return
    return True
def setup_user(username):
    inventory = get_user_inventory()
    inventory[username] = ["dagger", "spell", "bow", "staff"]
    write_inventory(inventory)


# ---------------------------
#   Store
# ---------------------------
#TODO d20_store = {""}

loot = [
("handaxe", 5),
("scimitar", 5),
("longsword", 5),
("maul", 5),
("flail", 5),
("warhammer", 4),
("lance", 4),
("greataxe", 4),
("shortsword", 4),
("glaive", 3),
("javelin", 3),
("longbow", 3),
("greatsword", 3),
("mastersword", 1)
]
lootlist = "handaxe", "scimitar", "longsword", "maul", "flail", "warhammer", "lance", "greataxe", "shortsword", "glaive", "javelin", "longbow", "greatsword", "mastersword"

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