import json
from bson import json_util

# ใช้งาน env
import os

import pandas as pd

# เพื่อแยกไฟล์ API ออกมาจาก server
from fastapi import APIRouter
apiMovies = APIRouter()

dataMoviesPath = os.path.join(os.getcwd(), "database", "datasetsMovie.csv")
userDataPath = os.path.join(os.getcwd(), "database", "userData.json")

dataMovies = pd.read_csv(dataMoviesPath).to_dict("records")

# จำนวน ดังนี้
# Movies = 61
# Anime = 24
# liveAction = 4

def readUser():
    with open(userDataPath, "r") as userDataFile:
         return json.load(userDataFile)

def  checkDatabase(database,col,data):
    return  [dataInDatabase for dataInDatabase in database if dataInDatabase.get(col)==data]

def  writeUserData(userData):
    with open(userDataPath, "w") as userDataFile:
        json.dump(userData, userDataFile)

@apiMovies.get('/')
def index():
    movies = checkDatabase(dataMovies,"formats","Movies")[:6]
    anime = checkDatabase(dataMovies,"formats","Anime")[:6]
    liveAction = checkDatabase(dataMovies,"formats","Live Action")[:6]
    # views ในที่นี้เป็นคอลัมภ์จำนวนผู้ชม (ในที่นี้ฐานข้อมูลเราเมคตัวเลขขึ้นมา)
    popular = sorted(dataMovies, key=lambda x: x.get("views", 0), reverse=True)[:6]

    return json_util.dumps({'Popular': popular,'Movies': movies,'Anime': anime,'liveAction': liveAction})

@apiMovies.get('/show/Movies')
def nextMovies(dataSkip:int):
    movies = checkDatabase(dataMovies,"formats","Movies")[dataSkip:dataSkip+6]
    return json_util.dumps(movies)

@apiMovies.get('/show/Animation')
def nextAnimation(dataSkip:int):
    anime = checkDatabase(dataMovies,"formats","Anime")[dataSkip:dataSkip+6]
    return json_util.dumps(anime)

@apiMovies.get('/show/Live-Action')
def nextLiveAction(dataSkip:int):
    liveAction = checkDatabase(dataMovies,"formats","Live Action")[dataSkip:dataSkip+6]
    return json_util.dumps( liveAction)

@apiMovies.get('/movies/detail')
def detail(index:int,username:str):
    userData = readUser()
    resultDataDetail = (checkDatabase(dataMovies,"index",index))
    dataDetail = resultDataDetail[0] if resultDataDetail else False
    if dataDetail :
        resultUsername = checkDatabase(userData,"username",username)
        if resultUsername:
            user = resultUsername[0] if resultUsername else False
            if user:
                user["viewTitle"] = dataDetail.get("title")
                writeUserData(userData)
    
    return json_util.dumps(dataDetail)

@apiMovies.get('/movies/search')
def searchData(dataSearch:str):
    resultSearch = [dataMovie for dataMovie in dataMovies if
                    dataSearch.lower() in dataMovie.get("title").lower() or
                    dataSearch.lower() in dataMovie.get("genres").lower() or
                    dataSearch.lower() in dataMovie.get("formats").lower() or
                    dataSearch.lower() in dataMovie.get("keywords").lower()]

    return json_util.dumps(resultSearch)