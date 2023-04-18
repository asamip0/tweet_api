from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel

from datetime import datetime
from fastapi.params import Body
from sqlite3 import IntegrityError

# from datetime import timedelta

import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# creating a tweet model
class TweetSchema(BaseModel):
    tweet: str
    created_on = datetime.now()
    modified_on = datetime.now()


app = FastAPI()

my_tweets = []


@app.post("/add_tweet/", status_code=status.HTTP_201_CREATED)
def add_tweet(tweet: TweetSchema, db: Session = Depends(get_db)):
    tweet_obj = models.Tweet(**tweet.dict())
    try:
        db.add(tweet_obj)
        db.commit()
        return {"message": "tweet created"}
    except Exception as e:
        print(e)
        return {"message": "Tweet Already exists"}
    return tweet_obj


# Delete data from db of particular id
@app.delete("/delete_tweet/{id}")
def delete_tweet(id: int, db: Session = Depends(get_db)):
    tweet_model = db.query(models.Tweet).filter(models.Tweet.id == id).first()

    if tweet_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid id :{id}"
        )
    else:
        db.query(models.Tweet).filter(models.Tweet.id == id).delete()
        db.commit()
        return {
            Response(status_code=status.HTTP_204_NO_CONTENT),
            "message:" "tweet deleted",
        }


@app.get("/tweet_fetch")
def tweet_fetch(db: Session = Depends(get_db)):
    return db.query(models.Tweet).all()





import json
import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/encode/")
def root():
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = current_time[:-3]

    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path) as fkey:
        _key = fkey.read().replace("\\n", "\n")
        private_key = RSA.importKey(_key)
    
    json_data = {"MerchantId": "16","ApiUserName": "KhaltiFT","TimeStamp": time}
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data)
    
    response = {
        "TimeStamp": time,
        "Signature": signature
    }
    
    return response

def get_concat_values_from_json(item):
    obj = json.loads(item)
    sign_data = ""
    for prop in sorted(obj):
        if prop.lower() != "signature":
            try:
                sign_data += obj[prop]
            except:
                sign_data += ""
    return sign_data

def generate_rsa_signature(private_key, text):
    h = SHA256.new(text.encode('utf-8'))
    signature = pkcs1_15.new(private_key).sign(h)
    return base64.b64encode(signature).decode('utf-8')



import json
import base64
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


app = FastAPI()


class PaymentData(BaseModel):
    MerchantId: str
    ApiUserName: str

class PaymentResponse(BaseModel):
    Signature: str
    TimeStamp: str


def get_concat_values_from_json(item):
    obj = json.loads(item)
    sign_data = ""
    for prop in sorted(obj):
        if prop.lower() != "signature":
            try:
                sign_data += obj[prop]
            except:
                sign_data += ""
    return sign_data


def generate_rsa_signature(private_key, text):
    signature = private_key.sign(
        text, padding.PKCS1v15(), hashes.SHA256())
    return base64.b64encode(signature).decode('utf-8')


@app.post("/payment")
async def generate_payment_signature(payment_data: PaymentData):
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = (current_time[:-3])
    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path, "rb") as fkey:
        private_key = serialization.load_pem_private_key(
            fkey.read(), password=None)

    json_data = {"ApiUserName": payment_data.ApiUserName,"MerchantId": payment_data.MerchantId,  "TimeStamp": f"{time}"}
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data.encode())
    return PaymentResponse(Signature=signature, TimeStamp=time)

@app.post("/accpayment")
async def generate_payment_signature():
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = (current_time[:-3])
    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path, "rb") as fkey:
        private_key = serialization.load_pem_private_key(
            fkey.read(), password=None)

    json_data = {
    "ApiUserName": "KhaltiFT",
    "DestinationAccName": "Sabin Dawadi",
    "DestinationAccNo": "19000000000000000005",
    "DestinationBank": "FTTESTBANK",
    "DestinationCurrency": "NPR",
    "MerchantId": "16",
    "MerchantProcessID": "test02",
    "MerchantTxnId": "test02",
    "SourceAccName": "Khalti ACC",
    "SourceAccNo": "19000000000000000018",
    "SourceBank": "FTTESTBANK",
    "SourceCurrency": "NPR",
    "TimeStamp": f"{time}",
    "TransactionRemarks": "fundTransfer UAT",
    "TransactionRemarks2": "",
    "TransactionRemarks3": ""
   }
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data.encode())
    return PaymentResponse(Signature=signature, TimeStamp=time)

@app.post("/numbervalidate")
async def generate_payment_signature():
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = (current_time[:-3])
    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path, "rb") as fkey:
        private_key = serialization.load_pem_private_key(
            fkey.read(), password=None)

    json_data = {
    "AccountName": "Sabin D",
    "AccountNumber": "9840186256",
    "ApiUserName": "KhaltiFT",
    "BankCode": "FTTESTBANK",
    "IsMobile": "Y",
    "MerchantId": "16",
    "TimeStamp": f"{time}",
   }
    
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data.encode())
    return PaymentResponse(Signature=signature, TimeStamp=time)




@app.post("/numberfundtransfer")
async def generate_payment_signature():
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = (current_time[:-3])
    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path, "rb") as fkey:
        private_key = serialization.load_pem_private_key(
            fkey.read(), password=None)

    json_data = {
    "Amount": "1999",
    "ApiUserName": "KhaltiFT",
    "DestinationAccName": "Sabin Dwa",
    "DestinationAccNo": "19000000000000000005",
    "DestinationBank": "FTTESTBANK",
    "DestinationCurrency": "NPR",
    "IsDestinationMobile": "Y",
    "MerchantId": "16",
    "MerchantProcessID": "samiptest03",
    "MerchantTxnId": "test10",
    "SourceAccName": "Khalti ACC",
    "SourceAccNo": "19000000000000000018",
    "SourceBank": "FTTESTBANK",
    "SourceCurrency": "NPR",
    "TimeStamp": f"{time}",
    "TransactionRemarks": "test03:KhaltiFT",
    "TransactionRemarks2": "test01",
    "TransactionRemarks3": "test01"
   }
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data.encode())
    return PaymentResponse(Signature=signature, TimeStamp=time)



@app.post("/lookup")
async def generate_payment_signature():
    
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    time = (current_time[:-3])
    key_file_path = "/home/samip/Downloads/PrivateKey_20230411145746.pem"
    with open(key_file_path, "rb") as fkey:
        private_key = serialization.load_pem_private_key(
            fkey.read(), password=None)

    json_data = {
    "ApiUserName": "KhaltiFT",
    "MerchantId": "16",
    "MerchantTxnId": "test055",
    "TimeStamp": f"{time}"
   }
    json_data = json.dumps(json_data)
    concat_data = get_concat_values_from_json(json_data)
    signature = generate_rsa_signature(private_key, concat_data.encode())
    return PaymentResponse(Signature=signature, TimeStamp=time)