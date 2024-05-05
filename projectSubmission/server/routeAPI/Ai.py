# model
from model import sentiment as modelPredict
from model import suggested as modelSuggested

import os
import json

from fastapi import APIRouter

apiAI = APIRouter()

def readUser():
    userDataPath = os.path.join(os.getcwd(), "database", "userData.json")
    with open(userDataPath, "r") as userDataFile:
        return json.load(userDataFile)

def find(userData,data):
    return [user for user in userData if user.get("username")==data]

@apiAI.get('/sentiment')
def sentiment(text: str):
    return {'text': text, 'sentiment': modelPredict(text)}

@apiAI.get('/suggested')
def suggested(username: str):
    userData = readUser()
    user = find(userData,username)
    if user:
        viewUserMovie = user[0].get("viewTitle")
        if viewUserMovie:
            return {'username': username, 'view':viewUserMovie,"suggested":modelSuggested(viewUserMovie) }
    return {'username': username, 'view':viewUserMovie,"suggested":False }
    