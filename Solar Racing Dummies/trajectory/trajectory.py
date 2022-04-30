from dis import dis
from operator import index

from Trajectory.socError import SOCError
from models.car_data import CarData
import pandas as pd
import numpy as np
import Trajectory.constants as constants

segmentDF = pd.DataFrame(columns = ["Starting Index", "Ending Index", "Power Out"])

def segmentGenerator(
        track : pd.DataFrame,
        target_velocity : float,
        car : CarData,
        index_1 : int,
        initial_soc : int,  
        min_soc : int
) :
    global minimum_soc
    minimum_soc = min_soc
    try :

        # define margin more accurately later
        # segmentDF = pd.DataFrame(columns = ["Starting Index", "Ending Index", "SOC"])

        track["Power Out"] = np.nan
        track["Net Power"] = np.nan
        track["SOC"] = np.nan
        track.loc[index_1,"SOC"] = initial_soc     #The initial SOC here is hardcoded in the trajectory_test file. Need to read from config file instead.

        if index_1 == 0:
            index_1 = 1

        elevation_change = track.loc[index_1, "Elevation(m)"] - track.loc[index_1 - 1, "Elevation(m)"]
        distance_change = track.loc[index_1, "Distance(m)"] - track.loc[index_1 - 1, "Distance(m)"]
        eAngle1 = np.rad2deg(np.arctan(elevation_change/distance_change))

        for index_n in range(index_1,len(track.index)) :
            if index_n == 0: #We don't want to start at index 0 on the track df
                continue
            # to take into accunt the checkpoints and stagestops which determine segments (Driving == false)
            if (track.loc[index_n,"Driving"] == False) :
                if (track.loc[index_n - 1,"Driving"] == True) :
                    makeSegment(index_1, index_n - 1, track, target_velocity, car)
                if (track.loc[index_n  + 1,"Driving"] == True) :
                    index_1 = index_n + 1
                    elevation_change = track.loc[index_1, "Elevation(m)"] - track.loc[index_n, "Elevation(m)"]
                    distance_change = track.loc[index_1, "Distance(m)"] - track.loc[index_n, "Distance(m)"]
                    eAngle1 = np.rad2deg(np.arctan(elevation_change/distance_change))
                track.loc[index_n,"Power Out"] = 0
                socCalculations(index_n,track)
                continue

            elevation_change = track.loc[index_n, "Elevation(m)"] - track.loc[index_n - 1, "Elevation(m)"]
            distance_change = track.loc[index_n, "Distance(m)"] - track.loc[index_n - 1, "Distance(m)"]
            eAngleN = np.rad2deg(np.arctan(elevation_change/distance_change))

            if ((np.sign(eAngle1) != np.sign(eAngleN)) or ((np.sign(eAngle1) + np.sign(eAngleN) == 2) and abs(eAngle1 - eAngleN) >= constants.margin)):
                makeSegment(index_1, index_n - 1, track, target_velocity, car)
                index_1 = index_n
                eAngle1 = eAngleN

        makeSegment(index_1, len(track.index) - 1, track, target_velocity, car)

    except SOCError as e :
        print(e)
        return None, -1, -1

    return (track,track.loc[len(track.index) - 1,"Distance(m)"],track.loc[len(track.index) - 1,"SOC"])

def motorPower(
        index_1 : int,
        index_n : int,
        track : pd.DataFrame,
        target_velocity: float,
        car: CarData
) :
    # calculate elevation angle by doing final elevation - initial elevation / final distance - initial distance

    vertDistance = track.loc[index_n, "Elevation(m)"] - track.loc[index_1, "Elevation(m)"]
    horDistance = track.loc[index_n, "Distance(m)"] - track.loc[index_1, "Distance(m)"]

    elevation_angle = np.arctan(vertDistance / horDistance)  #In radians

    # car.force takes in air density, velocity, elevation angle, turn angle, and acceleration.
    # The turn angle and acceleration are assumed to be 0

    forceResistance = car.force(constants.air_density, target_velocity, elevation_angle, 0, 0)
    motorForce = forceResistance

    powerOut = motorForce * target_velocity

    print(powerOut)

    for index in range(index_1,index_n + 1):
        track.loc[index, "Power Out"] = powerOut
        socCalculations(index,track)
    return powerOut

def socCalculations(
        index : int,
        track : pd.DataFrame
):

    #Net Power Calculations

    track.loc[index, "Net Power"] = track.loc[index, "Power In"] - track.loc[index, "Power Out"]

    #SOC Calculations

    #(1000 * 3600) is the conversion of total capacity from kWh to J
    #Multiplying and dividing by 100 converts SOC from a percent to a decimal and vice-versa.

    time_change = track.loc[index, "Time"] - track.loc[index - 1, "Time"]
    net_energy = track.loc[index, "Net Power"] * time_change  #If the car is draining battery, this should be negative.
    current_battery_capacity = track.loc[index - 1, "SOC"] / 100 * constants.INITIAL_CAPACITY * (1000 * 3600)  
    new_battery_capacity = current_battery_capacity + net_energy
    track.loc[index, "SOC"] = round(new_battery_capacity / (constants.INITIAL_CAPACITY * (1000 * 3600)) * 100,2)

    #Reality Check: 

    if track.loc[index, "SOC"] < minimum_soc:
        raise SOCError

def socRemaining(
        track : pd.DataFrame,
        soc_current : float
) :
    # the initial capacity is 4.74kWh = 4740Wh. Should change after every iteration
    # gives the SOC remaining after each segment

    running_intial_capacity = (soc_current / 100) * constants.INITIAL_CAPACITY

    track["SOC"] = np.nan

    for index_1, row in track.iterrows():
        powerOut = track.loc[index_1, "Power Out"]
        powerIn = track.loc[index_1, "Power In"]
        timeInt = track.loc[index_1 + 1, "Time"] - track.loc[index_1, "Time"]
        # time is in seconds, convert to hours /3600
        timeInt = timeInt / 3600
        # multiply the netPower times the time in hours
        # capacity_lost = capacity_lost - capacity_gained
        capacity_lost = (powerOut - powerIn) * timeInt
        soc = round(((running_intial_capacity - capacity_lost) / constants.INITIAL_CAPACITY) * 100, 2)
        if (soc <= 5) :
            # You have passed the critical SOC point. Try with a new target velocity.
            return (None, -1)
        else :
            track.loc[index_1, "SOC"] = soc
    return (track, 1)

def makeSegment(index_1 : int,
                index_n : int,
                track : pd.DataFrame,
                target_velocity : float,
                car: CarData,
) :
    powerOut = motorPower(index_1, index_n, track, target_velocity, car)
    segmentDF.loc[len(segmentDF.index)] = [index_1, index_n, powerOut]
