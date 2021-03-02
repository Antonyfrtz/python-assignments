import urllib.request
import json
from datetime import datetime
from tqdm.auto import tqdm

date=datetime.now()
#No of days passed in current month (max 28-31)
days=date.day
#First part of date selector string
curmonth=datetime.today().strftime('%Y-%m')

#Retrieve DrawID's for a specified date
def GetDrawIDs(day):
    r=urllib.request.urlopen("https://api.opap.gr/draws/v3.0/1100/draw-date/"+day+"/"+day+"/draw-id")
    html=r.read()
    html=html.decode()
    drawIDs=json.loads(html)
    return(drawIDs)

# +1 the selected numbers in the counter array
def Inserter(numbers):
    for i in range(len(numbers)):
        num_count[numbers[i]-1]+=1

print("\n Loading, please wait...\n")
for day in tqdm(range(1,days+1)):
    #Try to get data from urls,falls back to exception if it fails in the progress
    try:
        #Date format
        if day<=9:
            j="0"+str(day)
        else:
            j=str(day)
        selectedday=curmonth+"-"+j
        num_count=[0]*80
        draws=GetDrawIDs(selectedday)
        #Loop through DrawID's,requesting 10 per loop (maximum allowed by API) to minimize the number of requests (less requests==faster code)
        for i in range(0,len(draws),10):
            #Request 10 draws (maximum allowed by API) or as many are left if less than 10 remain
            if i+9<len(draws):
                n=10
                r=urllib.request.urlopen("https://api.opap.gr/draws/v3.0/1100/draw-id/"+str(draws[i])+"/"+str(draws[i+9]))
            else:
                n=len(draws)-i
                r=urllib.request.urlopen("https://api.opap.gr/draws/v3.0/1100/draw-id/"+str(draws[i])+"/"+str(draws[len(draws)-1]))
            html=r.read()
            html=html.decode()
            data=json.loads(html)
            #Get numbers from the n received draws
            for k in range(n):
                selecteddraw=data["content"][k]
                numbers=selecteddraw["winningNumbers"]["list"]
                Inserter(numbers)
        if day==days and date.strftime("%H:%M")<="23:56":
            print("\n\n Warning: Current day's draws (",datetime.today().strftime('%Y-%m-%d'),") have not finished. Statistics subject to change")
        #Most common number/numbers of the day in the array
        if max(num_count)!=0:
            common=max(num_count)
            popular=[]
            for i in range(0,80):
                if num_count[i]==common:
                    popular.append(str(i+1))
            print("\n\n Most occuring number/numbers of",selectedday,"is",','.join(popular),"\n")
        else:
            print(" No draws found for this date ("+selectedday+")\n")
    except:
        print("\n\n Failed to contact server/error occured for",selectedday,"\n")
