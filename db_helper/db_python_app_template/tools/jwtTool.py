import jwt
import time
secretKey='53002GroupProject'
headers = {
  "alg": "HS256",
  "typ": "JWT"
}
expireTime=3600

def generateJwt(data):
    token = jwt.encode(data, secretKey, algorithm="HS256",headers=headers)
    return token
def decodeToken(token):
    try:
        decoded_data = jwt.decode(token, secretKey, algorithms=["HS256"])
        expired=False
        if(decoded_data['exp']>time.time()+expireTime):
            expired=True
        return decoded_data,expired,True,"success"
    except Exception as e:
        return "","",False,e

def generateToken(data):
    data['exp']=time.time() + expireTime
    token=generateJwt(data)
    return token