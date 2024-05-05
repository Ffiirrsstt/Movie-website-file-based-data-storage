from flask import abort
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv 
import jwt
import json
import os

from fastapi import APIRouter
apiLogin = APIRouter()
load_dotenv()

# รหัสผ่านเป็นแบบเข้ารหัส
pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

def checkUsername(dataUsername):
    userDataPath = os.path.join(os.getcwd(), "database", "userData.json")
    with open(userDataPath, "r") as userDataFile:
        userData = json.load(userDataFile)
    return [datauser for datauser in userData if datauser.get("username")==dataUsername]

# สร้าง JWT token
def createAccessToken(data: dict, expiresDelta: timedelta):
    toEncode = data.copy()
    expire = datetime.utcnow() + expiresDelta
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, os.environ["SECRETS_KEY"], algorithm="HS256")
    return encodedJwt

@apiLogin.post("/login")
async def loginAccessToken(formData: OAuth2PasswordRequestForm = Depends()):
    result = checkUsername(formData.username)
    user =   result[0] if result else False

    if not user or not pwdContext.verify(formData.password, user.get("password")):
        return {"login":False}

    accessTokenExpires = timedelta(minutes=60)

    accessToken = createAccessToken(
        data={"subject": user.get("username")}, expiresDelta = accessTokenExpires
    )
    return {"accessToken": accessToken, "tokenType": "Bearer","login":True}

@apiLogin.get("/users/data")
async def checkAccessToken (token: str = Depends(oauth2Scheme)):
    try:
        payload = jwt.decode(token, os.environ["SECRETS_KEY"], algorithms=["HS256"])
        username: str = payload.get("subject")
        user = checkUsername(username)
        if not user:
            abort(404, description="Username Not Found")
        return {"username": username}
    except jwt.ExpiredSignatureError:
        abort(401, description="Token has expired")
    except jwt.InvalidTokenError:
        abort(401, description="Invalid token")

