import json
import boto3
from boto3.dynamodb.conditions import Key , Attr


def lambda_handler(event,context):
    
    userId = event['queryStringParameters']['userId']
    chosen_track = event['queryStringParameters']['chosen_track']
    
    
     #connection with DynamoDB
    client = boto3.resource("dynamodb")
    table = client.Table("UserTracks")
    
    
    #Retrieves records from DynamoDB user tracks table
    response = table.query(KeyConditionExpression=Key('UserID').eq(userId))
    items = response['Items']
    
    for item in items:
        count = item['UserCount']
        sequence = item['Track_sequence']
        
   
   
    #for first time users
    if count == 1:
        #update item in database
        res = {chosen_track:90}

        input = {'UserID': userId,'UserCount' : count,'Track_sequence' : sequence , 'weightage' : res}
        result = table.put_item(Item=input) 
        
    
    #for more than one time users
    #else:
        
    
    

    return {
        'statusCode': 200,
        'body': json.dumps("hello")
    }
