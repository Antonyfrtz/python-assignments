import urllib.request
import json
from datetime import datetime
from tqdm.auto import tqdm
from time import sleep

date=datetime.now()
#No of days passed in current month (max 28-31)
days=date.day
#First part of date selector string
drawdate=datetime.today().strftime('%Y-%m')

def drawNo(day):
    r=urllib.request.urlopen("https://api.opap.gr/draws/v3.0/1100/draw-date/"+day+"/"+day+"/draw-id")
    html=r.read()
    html=html.decode()
    data=json.loads(html)
    if len(data)!=0:
        return data[0]
    else:
        return 0

def StatTrack(first):
    r=urllib.request.urlopen("https://api.opap.gr/draws/v3.0/1100/"+str(first))
    html=r.read()
    html=html.decode()
    data=json.loads(html)
    numbers=data["winningNumbers"]["list"]
    Inserter(numbers)

def Inserter(numbers):
    for i in range(len(numbers)):
        A[numbers[i]-1]+=1

A=[0]*80
print("\n Loading, please wait...\n")
for i in tqdm(range(1,days+1)):
    #Date format
    if i<=9:
        j="0"+str(i)
    else:
        j=str(i)
    selectedday=drawdate+"-"+j
    if drawNo(selectedday)==0:
        if (i==1 or i==21 or i==31):
            print("\n\n Whoops!No results found for the",str(i)+"st of",date.strftime('%B'),"\n")
        elif (i==2 or i==22):
            print("\n\n Whoops!No results found for the",str(i)+"nd of",date.strftime('%B'),"\n")
        elif (i==3 or i==23):
            print("\n\n Whoops!No results found for the",str(i)+"rd of",date.strftime('%B'),"\n")
        else:
            print("\n\n Whoops!No results found for the",str(i)+"th of",date.strftime('%B'),"\n")
        sleep(5)
    else:
        #First draw number of the "i"th day
        first=drawNo(selectedday)
        #Retrieve the numbers and sort them into the main array
        StatTrack(first)
#Print out results
print("\n Results:\n")
for i,number in zip(range(1,81),A):
    print("",i,"appears",number,"times")
    print(" ------------------")
