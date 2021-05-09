import json
import boto3
import random
from boto3.dynamodb.conditions import Key , Attr


#function for first time user with input as happy mood
def happy_mood(emotion,mood,hr,user_count):
    
    
    #track1 music
    a1 = " "
    track_number='track1'
    track1_music = []
    
    #connect to DB
    client = boto3.resource("dynamodb")
    table = client.Table("Emotion_tracks")
    
    #Retrieves records from DynamoDB emotion tracks table
    response = table.query(KeyConditionExpression=Key('mood').eq(mood) & Key('Track_no').eq(track_number))
    
    #extracts track1 music
    items = response['Items']
    for item in items:
        track1_music = item['Tracks']
    


    if emotion == "powerful":
        a1 = track1_music[0]
    elif emotion == "peaceful":
        a1 = track1_music[1]
    elif emotion == "joyful":
        a1 = track1_music[2]
    elif emotion == "thankful":
        a1 = track1_music[3]
    elif emotion == "loving":
        a1 = track1_music[4]
    elif emotion == "proud":
        a1 = track1_music[5]
       
    
    
    #track2 music
    a2 = " "
    track2_music = []
    track_number = "track2"
    
    #connect to DB
    client = boto3.resource("dynamodb")
    table = client.Table("Emotion_tracks")
    
    #Retrieves records from DynamoDB emotion tracks table
    response = table.query(KeyConditionExpression=Key('mood').eq(mood) & Key('Track_no').eq(track_number))
    
    items = response['Items']
    for item in items:
        track2_music = item['Tracks']
 
        
    
    #remove a1 from track2 list to avoid repetition
    if a1 in track2_music:
        track2_music.remove(a1)
    
    
    if emotion == "powerful":
        a2 = random.choice(track2_music)
    elif emotion == "peaceful":
        a2 = random.choice(track2_music)
    elif emotion == "joyful":
        a2 = random.choice(track2_music)
    elif emotion == "thankful":
        a2 = random.choice(track2_music)
    elif emotion == "loving":
        a2 = random.choice(track2_music)
    elif emotion == "proud":
        a2 = random.choice(track2_music)   
    
    
    #track3 music
    a3 = " "
    track_number = 'track3'
    track3_music=[]
    
    if hr == "poor":
        
        #connect to DB
        client = boto3.resource("dynamodb")
        table = client.Table("Emotion_tracks")
    
        #Retrieves records from DynamoDB emotion tracks table
        response = table.query(KeyConditionExpression=Key('mood').eq(mood) & Key('Track_no').eq(track_number))
        items = response['Items']
        for item in items:
            track3_music = item['Tracks']
        
        a3 = random.choice(track3_music)
       
    
    else:
        if a2 in track1_music:
            track1_music.remove(a2)
        if a1 in track1_music:
            track1_music.remove(a1)
        a3 = random.choice(track1_music)
        
    return(a1,a2,a3)
        
        
        

def lambda_handler(event,context):
    #Inputs
    #UserID, emotion, mood, heart rate input through API URL
    userId = event['queryStringParameters']['userId']
    emotion = event['queryStringParameters']['emotion']
    mood = event['queryStringParameters']['mood']
    heart_rate = event['queryStringParameters']['hr']
    myList = [] 
    res = []
    
    #mapping of heart rate
    if heart_rate >= 84:
        hr = 'poor'
    elif heart_rate >= 55 and heart_rate <= 69:
        hr = 'good'
    elif heart_rate >= 70 and heart_rate <= 78:
        hr = 'average'
    elif heart_rate >= 79 and heart_rate <= 83:
        hr = 'below_average'
    else:
        hr = "Invalid"
        
    
    
    #connection with DynamoDB
    client = boto3.resource("dynamodb")
    table = client.Table("UserTracks")
    
    
    #Retrieves records from DynamoDB user tracks table
    response = table.query(KeyConditionExpression=Key('UserID').eq(userId))
    items = response['Items']
    
    #if no record is found
    if not items:
        user_count = 0
    
        if mood == "happy":
            res = happy_mood(emotion,mood,hr,user_count)
            
            
            
            
            
            
        #update info to user_tracks table
        user_count = user_count + 1
        client = boto3.resource('dynamodb')
        table = client.Table('UserTracks')
        input = {'UserID' : userId , 'UserCount' : user_count , 'Track_sequence' : res}
        
        res = table.put_item(Item=input) 
        
        
    #for more than one time user
    #else:
       
    
    
    #retrieve music links from song database
        client = boto3.resource('dynamodb')
        table = client.Table('Songs')

        for item in res:
            response = table.query(KeyConditionExpression=Key('TrackID').eq(item))
            items = response['Items']
            for i in items:
                songs = item['link']
        
        
    
    return {
        'statusCode': 200,
        'body': json.dumps(songs)
    }
