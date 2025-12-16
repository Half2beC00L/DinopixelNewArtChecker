import requests
from bs4 import BeautifulSoup
import re
import datetime


def getart(username):
    findseclink = []
    findsecdate = []
    url = f"https://dinopixel.com/user/{username}"
    headers = {"User-Agent": "APCompSci_New_Art_Checker_Bot"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all("a", href=True, title=False):
        if "-pixel-art-" in a["href"]:
            findseclink.append(a["href"])

    date = soup.find_all("div")
    for d in date:
        dtext = d.get_text()

        countslash = dtext.count("/")
        if countslash == 2:
            findsecdate.append(dtext)

    if len(findseclink) >= 2:
        return findseclink[0], findsecdate[1]

    return None, None


def check_newart(username):
    try:
        with open(f"{username}_last_art.txt", "r") as file:
            oldart = file.read().strip()
    except FileNotFoundError:
        oldart = ""

    try:
        with open(f"{username}_last_date.txt", "r") as file:
            olddate = file.read()
    except FileNotFoundError:
        olddate = "[Not run before for this user]"

    newart, artd = getart(username)
    artdate = re.sub(r'[^0-9 /]', '', artd)
    artname = re.sub(r"[^a-zA-Z ()!,?.']", '', artd)

    datenow = datetime.datetime.now()
    formatdate = datenow.strftime("%d/%m/%y at %I:%M %p")

    if newart is None:
        print(f"{username} has not posted any art.\n")
        return
    if newart != oldart:
        print(f"{username} posted new art! (from last ran, {olddate} (UTC)): {artname}\nLink: {newart}.\nDate posted: {artdate.strip()} (utilizes DD/MM/YY).\nShow them some love!\n")
        with open(f"{username}_last_art.txt", "w") as file:
            file.write(newart)
        with open(f"{username}_last_date.txt", "w") as file:
            file.write(formatdate)
    else:
        print(f"No new art (from last ran, {olddate} (UTC)) from {username}.\nLast art posted: {artname}.\nLink: {oldart}.\nDate posted: {artdate.strip()} (utilizes DD/MM/YY).\n")
        with open(f"{username}_last_date.txt", "w") as file:
            file.write(formatdate)


check_newart("makingdumbstuff07")
check_newart("bello")
check_newart("sonic_fan_buddy_boy")
check_newart("dr_grym")
