import requests
import paho.mqtt.client as mqtt
import json
import time

broker="MQTT IP ADDRESS" # the mqtt sever address on your system

client = mqtt.Client("stars")
print("Connecting to broker ", broker)
client.connect(broker)

teamId = 25  #team id, find your team id at https://statsapi.web.nhl.com/api/v1/teams
teamName = 'Dallas Stars' #team name 
scores = {
    'away': 0,
    'home': 0
}
try:
  response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId=' + str(teamId)) #checks api for the schedule of your team
except:
  print("An exception occurred") #print if there is error with internet

data = response.json()  #get json response from request

totalGames = data['totalGames'] #get total games for your team on the given day

if totalGames > 0: #selection if team has game... if no games scherduled theres no need to run 
    gameData = data['dates'][0]['games'][0]['teams'] # get teams in the game
    status = data['dates'][0]['games'][0]['status']['abstractGameState'] #get status of the game either preview, live or final
    print(status)

    scores['away'] = gameData['away']['score'] #set scores from the gsame to away and home team
    scores['home'] = gameData['home']['score'] 


    if gameData['away']['team']['name'] == teamName: #sets your team to the home or away team for the given game
        teamScore = scores['away']
        myTeam = 'away'
        otherTeam = 'home'
    else:
        teamScore = scores['home']
        myTeam = 'home'
        otherTeam = 'away'

    while(status != 'Final'): #while loop continues until the game statuus is final
        try:
            response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId='+str(teamId))  #get response fro m nhl api on your team
        except:
            print("An exception occurred") # if internet is not working
        data = response.json()
        gameData = data['dates'][0]['games'][0]['teams'] #update game data
        status = data['dates'][0]['games'][0]['status']['abstractGameState'] # update game status
        
        if status != 'Live':
            time.sleep(60) #wait 60 seconds and try again if game is not live yet
            print("...........Waiting on game.......")

        while(status == 'Live'): #while loop continues while game status is live
            try:
                client.connect(broker)
                response = requests.get('https://statsapi.web.nhl.com/api/v1/schedule?teamId='+str(teamId)) #get new response for your team
            except:
                print("An exception occurred")
            data = response.json()
            gameData = data['dates'][0]['games'][0]['teams']
            status = data['dates'][0]['games'][0]['status']['abstractGameState']

            if(gameData[myTeam]['score'] > scores[myTeam]): #now check if your team scores goal
                scores[myTeam] = gameData[myTeam]['score'] #update score
                print('goal my team')
                client.publish("/stars", "G") #mqtt publish to stars topict to light up goal light
                

            if(gameData[otherTeam]['score'] > scores[otherTeam]): #now if other team scores
                scores[otherTeam] = gameData[otherTeam]['score'] #update there score 
                print('goal other team')
            
            if(gameData[myTeam]['score'] != scores[myTeam]): #if score does match score store in program update it, sometimes goals are taken away due to challenges
                scores[myTeam] = gameData[myTeam]['score']
            if(gameData[otherTeam]['score'] != scores[otherTeam]):
                scores[otherTeam] = gameData[otherTeam]['score']

            time.sleep(30) #sleep 30 seconds and check again you can update this to check api more or less frequently. I find 30 seconds works good but soemtimes is a bit too long. 



    if(gameData[myTeam]['score'] > gameData[otherTeam]['score']):
        print('WINNNERS')
        client.publish("/stars", 'W') #publish to stars topic to for light after a win. 
        #team winning code goes here



    print(scores) #after game is complete print result of game. 
    print(status)
