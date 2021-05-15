import json
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

   #get current time minuc 30 minutes
   timeCheck = (int(time.time())-1800)
   #print(timeCheck)

   # dynamodb client
   client = boto3.resource('dynamodb')
   dynamodb_client = boto3.client('dynamodb')

   table = client.Table('twitter_sentiment')

   response = table.scan(
    FilterExpression=Attr('created_at').gt(timeCheck) & Attr('sentiment_score').lt(1)
   )

   avgSentiment = 0
   count = 0

   for tweet in response['Items']:
      count = count +1
      avgSentiment = avgSentiment + (float(tweet.get('sentiment_score')))
      #print(tweet.get('sentiment_score'))
   if(count != 0):
      avgSentiment = avgSentiment/count
      avgSentiment = str(avgSentiment)
   else:
      avgSentiment = "0"

   timeNew = int(time.time())
   timeNew = str(timeNew)

   sentiment_id = "TSLA" + timeNew
   #print(avgSentiment)

   table_name = 'sentiment_stock'
   newSentiment  = {
     'sentiment_id': {'S': sentiment_id},
     'timestamp': {'N':  timeNew},
     'sentiment' : {'N' : avgSentiment},
     'ticker' : {'S': 'TSLA'}
   }

   dynamodb_client.put_item(TableName = table_name, Item= newSentiment)

   return None