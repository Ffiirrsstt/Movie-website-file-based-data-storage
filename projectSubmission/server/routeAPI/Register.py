# ใช้งาน env
import os
import json

from passlib.context import CryptContext
from pydantic import BaseModel

# เพื่อแยกไฟล์ API ออกมาจาก server
from fastapi import APIRouter
apiRegister = APIRouter()

userDataPath = os.path.join(os.getcwd(), "database", "userData.json")
pwContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

class account(BaseModel):
    userData: str
    passwordData: str

def readUser():
    with open(userDataPath, "r") as userDataFile:
        return json.load(userDataFile)

def  writeUserData(userData):
    with open(userDataPath, "w") as userDataFile:
        json.dump(userData, userDataFile)

@apiRegister.post("/register")
async def register(dataAccount:account):
    userData = readUser()
    hashedPassword = pwContext.hash(dataAccount.passwordData)

    accountId = len(userData)
    dataInsert  = {"idUser":accountId,"username" : dataAccount.userData,
                    "password":hashedPassword,"viewTitle": ""}

    userData.append(dataInsert)
    writeUserData(userData)
    return {"message": "Registration successful."}

@apiRegister.get("/register/User")
async def checkUserforRegister(dataUsername:str):
    #ถ้าเช็กออกมาว่าเป็น true คือผ่าน ไม่มี username ซ้ำ
    userData = readUser()
    resultCheck = all(user.get("username") != dataUsername for user in userData)
    return {"resultCheck": resultCheck}
