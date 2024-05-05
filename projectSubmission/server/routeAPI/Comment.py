import os
import json
from bson import json_util

from flask import abort
from fastapi import APIRouter
from datetime import datetime

from urllib.parse import unquote

from model import sentiment as modelPredict

from pydantic import BaseModel

apiComment = APIRouter()

commentDataPath = os.path.join(os.getcwd(), "database", "comment.json")

class commentForm(BaseModel):
    dataComment:str
    sentiment:str
    username:str

class commentFormEdit(BaseModel):
    username:str
    textCommentEdit:str
    idComment:int
    createData:datetime
    
class commentFormDelete(BaseModel):
    username:str
    idComment:int
    createData:datetime

def  readComment():
    with open(commentDataPath, "r") as commentFile:
        return json.load(commentFile)

def  writeComment(commentData):
    with open(commentDataPath, "w") as commentFile:
        json.dump(commentData, commentFile)

def findOne(commentData,col,data):
    result =  [dataCM for dataCM in commentData if dataCM.get(col)==data]
    return result[0] if result else False

def find(commentData,col,data):
    return [dataCM for dataCM in commentData if dataCM.get(col)==data]


def checkUser(commentData,username,commentEdit,createData):
    dataComment = [dataCM for dataCM in commentData if dataCM.get("idComment")==commentEdit and dataCM.get("created")==createData.isoformat()]
    if dataComment:
        if dataComment[0].get("username") == username:
            return True
    return False

def delelteUpdate(commentData):
    writeComment(commentData)
    commentData = commentData[-20:]
    commentData.sort(key=lambda x: x["created"], reverse=True)
    return json_util.dumps(commentData)

@apiComment.post('/add/Comment')
def addComment(dataForm:commentForm):
    commentData = readComment()
    commentId = len(commentData)
    dataInsert  = {"idComment":commentId,"comment" : dataForm.dataComment
    ,"sentiment":dataForm.sentiment,"username":dataForm.username
    ,"edit":False
    ,"edited":False,"created":datetime.utcnow().isoformat()
    }
    commentData.append(dataInsert)
    writeComment(commentData)
    return {"message": "Comment successfully posted."}

@apiComment.get('/show/Comment')
def AllComment(username:str,pageComment:int,findData:str):
    commentData = readComment()
    findeData = json.loads(findData)
    findKey = "".join((key for key in findeData.keys()))
    findValue = "".join((value for value in findeData.values()))

    if findKey!="":
        commentData = find(commentData,findKey,findValue)

    commentData.sort(key=lambda x: x["created"], reverse=True)
    totalComment = len(commentData)
    
    commentData = commentData[(pageComment-1)*20:pageComment*20]

    for data in commentData:
        data["edit"] = True if data.get("username") == username else False


    return ({"commentData":json_util.dumps(commentData),"count" : totalComment})

@apiComment.put('/comment/edit')
def editComment(dataForm:commentFormEdit):
    commentData = readComment()
    # เช็กผู้ใช้
    resultCheck = checkUser(commentData,dataForm.username,dataForm.idComment,dataForm.createData)
    if not resultCheck:
        abort(401, description="The username used does not match the account being operated.")
    
    sentiment = modelPredict(dataForm.textCommentEdit)
    for comment in commentData:
        if comment.get("idComment") == dataForm.idComment and comment.get("created")==dataForm.createData.isoformat():
            comment.update({
            "comment": dataForm.textCommentEdit,
            "sentiment": sentiment,
            "edit": True,
            "edited": True,
            "created": datetime.utcnow().isoformat()
        })
        #      = {"idComment":dataForm.idComment,
        # "comment": dataForm.textCommentEdit, "sentiment":sentiment,"username":dataForm.username
        # ,"edit": True,"edited":True,"created":datetime.utcnow().isoformat()}

    for data in commentData:
        data["edit"] = True if data.get("username") == dataForm.username else False

    return delelteUpdate(commentData)

@apiComment.delete('/comment/delete')
def deleteComment(data:commentFormDelete):
    commentData = readComment()
    username = data.username
    idComment = data.idComment
    createData = data.createData

    commentData = readComment()
    # เช็กผู้ใช้
    resultCheck = checkUser(commentData,username,idComment,createData)
    if not resultCheck:
        abort(401, description="The username used does not match the account being operated.")

    commentData = [dataCM for dataCM in commentData if dataCM.get("idComment") !=idComment or dataCM.get("created") !=createData.isoformat()]

    return delelteUpdate(commentData)