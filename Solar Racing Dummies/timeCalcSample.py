from datetime import datetime
import pandas as pd
#from sympy import true

global dayNum
global dayList

def timeDrivingChargingColumn(overallDF: pd.DataFrame,
                velocity: int,
                days: dict):
    finalDF = overallDF
    val = overallDF.values
    startTimes = []
    endTimes = []
    #These 3 list wil be added to dataframe
    timeList = []    
    drivingList = []
    chargingList = []
    #List keeps track of index and dataframe to be added at that index for charging/waiting periods
    insertList = []
    global dayNum
    dayNum = 0
    global dayList
    dayList = []
    segmentInfo = makeSegmentDict(days)
    velocity =  float(velocity) * 0.44704
    for day in days:
        date = day['startDate']
        dayList.append(date)
        startTime = day['startTime']
        currentTime = date + " " + startTime
        epochCurrent = datetime.strptime(currentTime,'%Y-%m-%d %H:%M' ).timestamp()
        #Make a list of each of the start times
        startTimes.append(epochCurrent)
        endTimes.append(epochCurrent + 32400)
    #Add the first start time into the overall timeList
    timeList.append(startTimes[dayNum])
    drivingList.append(False)
    chargingList.append(True)
    for index, v in enumerate(val):
        #Ignores first line which represents a line of beginning of race with details
        if (index == 0):
           #Key is used for segmentInfo dictionary; basically includes the details of the the stop
            key = v[0]
            continue 
        if (v[0] != ""):
            locList = ["", v[1], 0, v[3], v[4], v[5]]
            addedDataframe, currentTime = getNewRows(segmentInfo[key], timeList[index - 1], dayList[dayNum], locList)
            insertList.append((index, addedDataframe))
            timeList.append(currentTime)
            drivingList.append(False)
            chargingList.append(True)
            key = v[0]
            continue
        if timeList[index - 1] >= endTimes[dayNum]:
            locList = ["", v[1], 0, v[3], v[4], v[5]]
            dayNum += 1
            mornEvenDF = morningEveningCharge(locList, timeList[index - 1], dayList[dayNum])
            insertList.append((index, mornEvenDF))
            timeList.append(startTimes[dayNum])
            drivingList.append(True)
            chargingList.append(True)
            continue
        changeTime = round(float(v[2] / velocity), 0)
        #Adding change in time with previous time
        newTime  = timeList[index - 1] + changeTime
        timeList.append(newTime)
        drivingList.append(True)
        chargingList.append(True)
    #Adding time, driving, and charging lists to dataframe
    finalDF["Time"] = timeList
    finalDF["Driving"] = drivingList
    finalDF["Charging"] = chargingList
    #add dataframes in insertList
    offset = 0
    for ind, datafra in insertList:
        finalDF = pd.concat([finalDF.iloc[:ind + offset], datafra, finalDF.iloc[ind + offset:]]).reset_index(drop=True)
        offset += len(datafra.index)   
    return finalDF


def getNewRows(sinfo : list, currentTime : int, date : str, locat : list):
    #Stage Stop [0, closeTime]
    if sinfo[0] == 0: 
        epochClose = datetime.strptime(date + " " + sinfo[1],'%Y-%m-%d %H:%M' ).timestamp()
        t = epochClose - currentTime
        if t < 0:
            print("FAILURE MEGA FAIL JUST THE WORST")

    #Check Point [1, openTime, closeTime, holdTime, driveResunption]
    elif sinfo[0] == 1:
        epochAfterHold = currentTime + 2700   #adds 45 minutes
        epochDriverResume = datetime.strptime(date + " " + sinfo[4],'%Y-%m-%d %H:%M' ).timestamp()
        if epochAfterHold > epochDriverResume:    #Don't need to wait any more time
            #create rows for 45 minutes
            t = 2700     
        else:   #Need to wait more
            #create rows for time between resumetime and current time
            t = epochDriverResume - currentTime

    #Optional Loop [2, closeTime, wait Time]
    elif sinfo[0] == 2:
        pass

    info = {"Name": [], "Distance(m)": [], "DistanceInterval": [], "Elevation(m)": [], "Latitude": [],
    "Longitude": [], "Time": [], "Driving": [], "Charging": []}

    #Process for creating the new dataframe in at most 30 minutes increments
    while t > 0:
        info["Name"].append(locat[0])
        info["Distance(m)"].append(locat[1])
        info["DistanceInterval"].append(locat[2])
        info["Elevation(m)"].append(locat[3])
        info["Latitude"].append(locat[4])
        info["Longitude"].append(locat[5])
        info["Driving"].append(False)
        info["Charging"].append(True)
        if t > 1800:
            currentTime += 1800
        else:
            currentTime += t
        info["Time"].append(currentTime)
        t -= 1800

    newData = pd.DataFrame(data=info)

    if sinfo[0] == 0:
        global dayNum
        dayNum += 1
        chargeDF = morningEveningCharge(locat, currentTime, dayList[dayNum])
        currentTime = datetime.strptime(dayList[dayNum] + " " + "09:00",'%Y-%m-%d %H:%M' ).timestamp()
        frames = [newData, chargeDF]
        newData = pd.concat(frames)
    

    return newData, currentTime


def morningEveningCharge(locat: list, currentTime : int, newDay: str):
    info = {"Name": [], "Distance(m)": [], "DistanceInterval": [], "Elevation(m)": [], "Latitude": [],
    "Longitude": [], "Time": [], "Driving": [], "Charging": []}
    count = 0
    #Evening Charge
    while count < 4:
        info["Name"].append(locat[0])
        info["Distance(m)"].append(locat[1])
        info["DistanceInterval"].append(locat[2])
        info["Elevation(m)"].append(locat[3])
        info["Latitude"].append(locat[4])
        info["Longitude"].append(locat[5])
        info["Driving"].append(False)
        info["Charging"].append(True)
        currentTime += 1800
        info["Time"].append(currentTime)
        count += 1
    #Row signifying the end of the day (should be saying the time between 8:00 and 8:30, the car is doing nothing)
    info["Name"].append(locat[0])
    info["Distance(m)"].append(locat[1])
    info["DistanceInterval"].append(locat[2])
    info["Elevation(m)"].append(locat[3])
    info["Latitude"].append(locat[4])
    info["Longitude"].append(locat[5])
    info["Driving"].append(False)
    info["Charging"].append(False)
    currentTime += 1800
    info["Time"].append(currentTime)

    #Grab the time of 7:00 the next day
    currentTime = datetime.strptime(newDay + " " + "07:00",'%Y-%m-%d %H:%M' ).timestamp()
    count = 0
    #Morning Charge
    while count < 5:
        info["Name"].append(locat[0])
        info["Distance(m)"].append(locat[1])
        info["DistanceInterval"].append(locat[2])
        info["Elevation(m)"].append(locat[3])
        info["Latitude"].append(locat[4])
        info["Longitude"].append(locat[5])
        info["Driving"].append(False)
        info["Charging"].append(True)
        info["Time"].append(currentTime)
        currentTime += 1800
        count += 1

    newDF = pd.DataFrame(data=info)
    return newDF

def makeSegmentDict(days):
    result = {}
    for day in days:
        for segment in day["segments"]:
            infoList = []
            infoList.append(segment["type"])
            if segment["type"] == 3 or segment["type"] == 4:
                continue
            name = segment["name"]
            if segment["type"] == 0:
                infoList.append("18:00")
            elif segment["type"] == 1:
                infoList.append(segment["openTime"])
                infoList.append(segment["closeTime"])
                infoList.append(segment["holdTime"])
                infoList.append(segment["driverResumption"])
            elif segment["type"] == 2:
                infoList.append(segment["closeTime"])
                infoList.append(segment["waitTime"])
            result[name] = infoList
    return result
