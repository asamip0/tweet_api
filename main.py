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
        return{
            Response(status_code=status.HTTP_204_NO_CONTENT),
            "message:" "tweet deleted"} 

@app.get('/tweet_fetch')
def tweet_fetch(db: Session = Depends(get_db)):
    return db.query(models.Tweet).all()
    
