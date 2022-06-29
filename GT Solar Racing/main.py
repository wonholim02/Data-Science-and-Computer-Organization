import json

#from sympy import Segment, continued_fraction_periodic, timed, true
from TrackPreprocessor.ProcessTrack import read_track_data
from Optimization.getVelocity import adjustVelocity, getInititalVelocity, getNewVelocity
from Optimization.timeCalc import timeDrivingChargingColumn
from TrackPreprocessor.project_solar_irradiance import project_solar_irradiance
#from Trajectory.trajectory import segmentGenerator
from Trajectory.trajectoryCopy import *
from Trajectory.powerConstant import powerOutConstant
from models.car_data import *
from graphOutput.graphOut import *

def main(config, soc):
    f = open(config)
    data = json.load(f)
    track = data["simulation"]["track"]
    days = data["simulation"]["days"]
    loop = [0,0,0]
    maximum = ([], None, 0, 0, 0)
    results = {}
    originalDataframe = read_track_data(track, loop)
    velocity = getInititalVelocity(days, loop)
    velocity = getNewVelocity(velocity, data)
    results[str(loop)] = (None, 0, 0, 0)
    car = CarData(data["car"])
    done = False
    while not done:
        print("testing velocity " + str(velocity))
        if velocity == 26:
            break
        print("RUNNING TDC")
        df = timeDrivingChargingColumn(originalDataframe, velocity, days)
        print("RUNNING POWERIN")
        powerInList = [800] * len(df)
        df["Power In"] = powerInList
        #df = project_solar_irradiance(df, 20000)
        print("RUNNING POWER OUT")
        df, finalDistance, finalSOC = segmentGenerator(df, velocity, car, 0, soc, 5)
        df.to_csv("Output/outFile.csv", index = True)
        #df, finalDistance, finalSOC = powerOutConstant(df, velocity, car, soc)
        if finalDistance >= results[str(loop)][1]:
            results[str(loop)] = (df, finalDistance, finalSOC, velocity)
            if finalSOC > 20:
                velocity = adjustVelocity(velocity, -2)
                continue
            done = True
        else:
            velocity = adjustVelocity(velocity, -1)
            df.to_csv("Output/outFile.csv", index = True)
    df.to_csv("Output/outFile.csv", index = True)
    #print(segmentDF)

    createSOCDistanceGraph(df, "SOCDistance.png", velocity)
    createSOCTimeGraph(df, "SOCTime.png", velocity)
    createPowerOutDistance(df, "PowerOutDistance.png", velocity)
    #createPowerTimeGraph(df, "PowerTime.png", velocity)
    #return results
    return velocity

print(main("Input/ASC 2021 JSON.json",100.00))



#def mainExample(configName, SoC, dayNum):
#    config = "Input/ASC 2021 JSON.json"
#    f = open(config)
#    data = json.load(f)
#    track = data["simulation"]["track"]
#    days = data["simulation"]["days"]
#    loopList = [[0,0,0]] #etc.
#    resultList = []
#    maxOption = ([], None, 0, 0) #loopList, df, distance, final SOC
#    for loop in loopList:
#        odf = read_track_data(track, loop) # could include another parameter in which it starts at a specific segment
#        vel = getInititalVelocity(data, loopList) #I will have you work on this, You can follow my initial setup, but also need to make sure the timings match up
#        #Above function ensures that we won't get to a checkpoint too fast or to a stagestop/optionalLoop too slow
#        #The same .py file will also include the increase/decrease function which is very trivial right now, could be spiced up a bit, but it works
#        vel = getNewVelocity(vel)
#        done = False
#        while not done:
#            if vel == -1:
#                distance = -1
#                break
#            df = timeDrivingChargingColumn(odf, vel, days) #puts the time, driving, and charging columns and returns the new df
#            df = project_solar_irradiance(df) #adds the irradiance column and returns the df. May also include powerIn column as well
#            df, result = powerOut(df) #adds the powerOut column and the net power while we are at. Returns new dataframe, and final net power
#
#
#        #NEED TO CHANGE
#
#
#            if abs(result) > totalPowerAvailable * 0.95: #if the new power is more than 95% of total power, decrease speed and start over
#                vel = updateVel(vel, -1)
#                continue                                #should start back at the tdcColumn function
#            elif abs(result) < totalPowerAvailable * 0.85: #If the net power is less than 85% of the total power (Remaining SOC is 15% or more)
#                vel = updateVel(vel, -2)                   #Increase speed
#                continue                                   #Start at tdcColumn() again
#            df, result, distance, finalSoc = realityCheck(df, SoC) #reality check will return result = 0 if everything works, otherwise result will be negative
#            if result < 0:
#                vel = updateVel(vel, result)   #This if statement occurs when reality check says that we did below 5% at some point (too risky)
#                continue
#            done = True
#        if distance > 0:                                        #If the the loop option is possible, distance will be above 0
#            if distance > maxOption[2]:                         #If the distance is greater than the current max option's distance, 
#                max = (loop, df, distance, finalSoC)            #this is new max Option
#            resultList.append((loop, df, distance, finalSoC))
#        else:
#            updateLoopList(loopList) #Probably do the work here, so the For loop doesn't get confused which loops it has done and not done
#    graphOutput(df)
#    return maxOption
