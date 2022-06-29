from tkinter import *
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

def func(soc, guessVelocity):
    config = "Input/MR17 JSON.json"
    f = open(config)
    data = json.load(f)
    track = data["simulation"]["track"]
    days = data["simulation"]["days"]
    loop = [0]
    maximum = ([], None, 0, 0, 0)
    results = {}
    originalDataframe = read_track_data(track, loop)
    velocity = getInititalVelocity(days, loop)
    velocity = getNewVelocity(velocity, data)
    velocity = guessVelocity
    results[str(loop)] = (None, 0, 0, 0)
    car = CarData(data["car"])
    done = False
    while not done:
        print("testing velocity " + str(velocity))
        if velocity == -1:
            break
        print("RUNNING TDC")
        df = timeDrivingChargingColumn(originalDataframe, velocity, days)
        print("RUNNING POWERIN")
        powerInList = [800] * len(df)
        df["Power In"] = powerInList
        #df = project_solar_irradiance(df, 20000)
        print("RUNNING POWER OUT")
        df, finalDistance, finalSOC = segmentGenerator(df, velocity, car, 0, soc, 5)
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

    #createSOCDistanceGraph(df, "SOCDistance.png", velocity)
    #createSOCTimeGraph(df, "SOCTime.png", velocity)
    #createPowerOutDistance(df, "PowerOutDistance.png", velocity)
    #createPowerTimeGraph(df, "PowerTime.png", velocity)
    #return results
    return df, velocity

################# GUI STUFF #################################

#"""

root = Tk()
root.title("Strategy Simulation GUI")

e = Entry(root, width = 50, bg = "gray", borderwidth = 5)
e.pack()
e.insert(0, "Put in a guess velocity ")

vel = 0.0

def calculateTargetVelocity():
    velocity = func(100.00, float(e.get()))[1]
    #vel = velocity
    hello = "Your target velocity is " + str(velocity) + "!"
    myLabel = Label(root, text = hello)
    myLabel.pack()
def createGraphs():
    #df = pd.DataFrame()
    #print(func(100, float(e.get))[0])
    tuple = func(100, float(e.get()))
    df = tuple[0]
    vel = tuple[1]

    hello = "Your target velocity is " + str(vel) + "!"
    myLabel = Label(root, text=hello)
    myLabel.pack()

    createSOCDistanceGraph(df , "SOCDistance.png", vel)
    createSOCTimeGraph(df, "SOCTime.png", vel)
    createPowerOutDistance(df, "PowerOutDistance.png", vel)

# Creating the Widgets
createGraphsButton = Button(root, text = "Simulate!", padx = 50, pady = 10, command = createGraphs, fg = "green")
#createGraphsButton = Button(root, text = "!", padx = 50, pady = 10, command = createGraphs, fg = "blue")
openCSVButton = Button(root, text = "Open Spreadsheets!", padx = 50, pady = 10, command = createGraphs, fg = "blue", state = DISABLED)

# Putting that widget on the screen

#targetVelocityButton.pack()
createGraphsButton.pack()
openCSVButton.pack()

button_quit = Button(root, text = "Exit Program", command = root.quit)

button_quit.pack()

#myLabel1.grid(row = 0, column = 0)
#myLabel2.grid(row = 1, column = 0)

root.mainloop()

#"""
