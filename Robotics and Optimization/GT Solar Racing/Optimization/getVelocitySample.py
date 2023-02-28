import math
import json
from datetime import datetime
import math
from datetime import timedelta
global testedvel
testedVel = []

def getInititalVelocity(days : dict, loop : list):
    waitTime = 0
    totalTime = 0
    totalDistance = 0
    loopIndex = 0
    maxVel = maxVelocity(days)
    global testedVel
    testedVel.append(maxVel)
    for day in days:
        totalTime += day['drivingTime']
        date = day["startDate"]
        for segment in day['segments']:
            if segment['type'] == 1 or segment["type"] == 0:
                totalDistance += segment["distance"]
            if segment['type'] == 1:
                waitTime += datetime.strptime(date + " " + segment["holdTime"],'%Y-%m-%d %H:%M' ).timestamp() - datetime.strptime(date,'%Y-%m-%d' ).timestamp()
            if segment["type"] == 2 and loop[loopIndex] == 1:
                waitTime += datetime.strptime(date + " " + segment["holdTime"],'%Y-%m-%d %H:%M' ).timestamp() - datetime.strptime(date,'%Y-%m-%d' ).timestamp()
    initalVelocity = totalDistance / (totalTime - (waitTime / 3600))
    if initalVelocity < 20:
        initalVelocity = 20
    testedVel.append(math.ceil(initalVelocity))
    return math.ceil(initalVelocity)

def getNewVelocity(preVel, data):
    days = data['simulation']['days']
    #Currrent Time is put in place to serve as time tracker in the situation there are multiple checkstops in a given day
    currentTime = 0
    leftOver = []
    for day in days:
        #save date
        date = day['startDate']
        startTime = day['startTime']
        currentTime = date + " " + startTime
        epochCurrent = datetime.strptime(currentTime,'%Y-%m-%d %H:%M' ).timestamp()
        for segment in day['segments']:
            try:
                distance = segment["distance"]
                if len(leftOver) > 0:
                    distance -= leftOver[0]
                    leftOver = []
            except KeyError:
                pass
            #Checks if a given segment is a base leg
            if segment['type'] == 1:
                openCheck = date + " " + segment["openTime"]
                epochOpen = datetime.strptime(openCheck, '%Y-%m-%d %H:%M').timestamp()
                #Based on current velocity what is the amount of time needed to get to the end of the segment
                timeNeeded = (float (distance)) / preVel
                
                #Make time in seconds
                timeSeconds = timeNeeded * 3600
                #Finds the new time by adding current Time with amount of seconds needed
                epochNew = epochCurrent + timeSeconds
                #Checks of we get to end of segment before it opens
                if epochNew < epochOpen:
                    return getNewVelocity(preVel - 1, data)
                else:
                    epochDriverResume = datetime.strptime(date + ' ' + segment["driverResumption"], '%Y-%m-%d %H:%M').timestamp()
                    epochCurrent = epochNew + 2700 
                    #If the time after wait is before the driver resumption time, then set the current time to the
                    #driver resumption time                
                    if epochCurrent < epochDriverResume:
                        epochCurrent = epochDriverResume
            elif segment['type'] == 0:
                closeCheck = date + " " + segment["closeTime"]
                epochClose = datetime.strptime(closeCheck, '%Y-%m-%d %H:%M').timestamp()
                #Based on current velocity what is the amount of time needed to get to the end of the segment
                timeNeeded = (float (distance)) / preVel
                #Make time in seconds
                timeSeconds = timeNeeded * 3600
                #Finds the new time by adding current Time with amount of seconds needed
                epochNew = epochCurrent + timeSeconds
                #Checks of we get to end of segment before it opens
                if epochNew > epochClose:
                    return getNewVelocity(preVel + 1, data)
                else:
                    epochCurrent = epochNew
            #When there is no Stage Stop at the end of the day
            elif segment["type"] == 3:
                epochEndofDay = datetime.strptime(date + ' ' + segment["closeTime"], '%Y-%m-%d %H:%M').timestamp()
                timeRemaining = epochEndofDay - epochCurrent
                timeRemaining = timeRemaining / 3600
                distanceTraveled = preVel * timeRemaining
                leftOver.append(distanceTraveled)
    return preVel


def adjustVelocity(preVel, result):
    if result == -2:
        print("Go Faster")
        preVel += 2
    if result == -1:
        print("Go Slower")
        preVel -= 1
    global testedVel
    if preVel in testedVel:
        return -1
    testedVel.append(preVel)
    return preVel

def maxVelocity(days):
    firstDistance = days[0]['segments'][0]['distance']
    date = days[0]['startDate']
    firstStartTime = days[0]['startTime']
    epochStartTime = datetime.strptime(date + " " + firstStartTime,'%Y-%m-%d %H:%M' ).timestamp()
    firstOpenTime = days[0]['segments'][0]['openTime']
    epochOpenTime = datetime.strptime(date + " " + firstOpenTime,'%Y-%m-%d %H:%M').timestamp()
    changeTime = epochOpenTime - epochStartTime
    changeTimeHour = changeTime /3600
    maxVelocity = math.floor(firstDistance/changeTimeHour)
    return maxVelocity
