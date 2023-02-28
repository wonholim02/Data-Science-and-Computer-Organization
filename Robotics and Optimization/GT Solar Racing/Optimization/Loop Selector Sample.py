#selects the loop that can potentially work

def loopSelector(loopList : list, targetLoop : list):
 newList = []
 if targetLoop[0] == 0 and targetLoop[1] == 0 and targetLoop[2] == 0 :
     return newList
  return newList

 for li in loopList:
  check = True
  if li[0] >= targetLoop[0]: 
   if li[1] >= targetLoop[1]:
    if li[2] >= targetLoop[2]:
     check = False

  if check == True:
   newList.append(li)

 loopList = newList

 return loopList

#Samples and Test
"""Test Kit
#Test cases
cases = [[0,0,0],[0,0,1],[0,1,0],[1,0,0],[0,1,1],[1,1,0],[1,0,1],[1,1,1]]
goal = [0,1,0]
print(loopSelector(cases,goal))
goal1 = [1,0,0] #Test Result: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1]]
goal2 = [0,1,0] #Test Result: [[0, 0, 0], [0, 0, 1], [1, 0, 0], [1, 0, 1]]
goal3 = [0,0,1] #Test Result: [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0]]
goal4 = [1,1,0] #Test Result: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [1, 0, 1]]
goal5 = [0,1,1] #Test Result: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 0], [1, 0, 1]]
goal6 = [1,0,1] #Test Result: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0]]
goal7 = [1,1,1] #Test Result: [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [1, 1, 0], [1, 0, 1]]
goal8 = [0,0,0] #Test Result: []
#Test calls
print('If [1,0,0] does not work')
print(loopSelector(cases,goal1))
print('If [0,1,0] does not work')
print(loopSelector(cases,goal2))
print('If [0,0,1] does not work')
print(loopSelector(cases,goal3))
print('If [1,1,0] does not work')
print(loopSelector(cases,goal4))
print('If [0,1,1] does not work')
print(loopSelector(cases,goal5))
print('If [1,0,1] does not work')
print(loopSelector(cases,goal6))
print('If [1,1,1] does not work')
print(loopSelector(cases,goal7))
print('If [0,0,0] does not work')
print(loopSelector(cases,goal8))
Test Kit"""
