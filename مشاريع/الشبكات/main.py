import requests
import os
import sys
import time
import datetime
import calendar
 
# import json

clientID="37c84afe-456d-438c-abc1-10ac2476e150"
Password1="ef1c21ab-2d8f-4e59-a7d8-0d7466e6a823"
REG_TAX_ID="376564970"
TaxActivityCode="1312"
Previous_DateTime = datetime.datetime.today() - datetime.timedelta(days=1)
print ('Previous Date: ' + str(Previous_DateTime))
Previous_Date=Previous_DateTime.strftime('%Y-%m-%d')
print ('Previous Date: ' + str(Previous_Date))
date=str(Previous_Date)
App_PATH = os.path.abspath(os.path.split(sys.argv[0])[0])
SavingLoction=App_PATH
#date="2023-1-31"
pageNo=1
pageSize=2
Year=""
isYear=False
isjson=False
for arg in sys.argv[1:]:
    if "year=" in arg :
      try:
        Year = int(arg.split("=")[1])
        isYear=True
      except Exception as e :
        print(e)
        print("fps is 60 , it must be intger number")
    elif "json" in arg:
        isjson = True
    

base_url = "https://id.eta.gov.eg"
api_url="https://api.invoicing.eta.gov.eg"
urlPrefix = '/api/v1.0'
Login_url = "/connect/token"
documentpackages=f"/documentpackages/requests?pageNo={pageNo}&pageSize={pageSize}"
documenttypes="/documenttypes"


url = base_url+Login_url
documentpackagesurl=base_url+documentpackages
documenttypesurl=base_url+urlPrefix+documenttypes

def documentPdfUrl(uuid):
 return api_url+urlPrefix+f"/documents/{uuid}/pdf"

def searchPackages(date,pageSize=1000,direction="Received"):
  return  api_url+urlPrefix+f"/documents/search?submissionDateFrom={date}&submissionDateTo={date}T23:59:59&continuationToken=&pageSize={pageSize}&issueDateFrom=&issueDateTo=&direction={direction}&status=&documentType=&receiverType=&receiverId=&issuerType=&issuerId="


def searchPackagesbyAll(submissionDateFrom,submissionDateTo,issuerId='',issuerType='',receiverId='',receiverType='',documentType='',status='',issueDateFrom='',issueDateTo='',continuationToken='',pageSize=1000,direction="Received"):
  return  api_url+urlPrefix+f"/documents/search?submissionDateFrom={submissionDateFrom}&submissionDateTo={submissionDateTo}&continuationToken={continuationToken}&pageSize={pageSize}&issueDateFrom={issueDateFrom}&issueDateTo={issueDateTo}&direction={direction}&status={status}&documentType={documentType}&receiverType={receiverType}&receiverId={receiverId}&issuerType={issuerType}&issuerId={issuerId}"


Token_value=""

prams = {
    'grant_type' : 'client_credentials',
            'client_id' : clientID,
            'client_secret' : Password1,
            'scope' : 'InvoicingAPI'
}
            
        

headers={}
print(url)
print(prams)
noConnection=True
DelayCallAPI=2 #API calls quota exceeded! maximum admitted 1 per 2s.
initDelay=2
delayConnection=initDelay
timeout=5
pathexceptions=SavingLoction+f"\{date}"
mytime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

if not os.path.exists(pathexceptions):
    os.makedirs(pathexceptions)
while(noConnection):
    try:
        time.sleep(DelayCallAPI)
        r = requests.post(url,data=prams,headers=[],timeout=timeout)
        noConnection=False
        delayConnection=initDelay
        try:
            if os.path.isfile(pathexceptions+f"\\No internet.txt"):
                os.remove(pathexceptions+f"\\No internet.txt")
            if os.path.isfile(pathexceptions+f"\\Timeout.txt"):
                os.remove(pathexceptions+f"\\Timeout.txt")
        except :
            print("can`t remove")
    except requests.exceptions.ConnectionError as e:
        with open(pathexceptions+f"\\No internet.txt", 'w') as f:
            
            f.write(f"{mytime} | No internet, when login , delay to resending is {delayConnection}")
        time.sleep(delayConnection)
        delayConnection*=2
    except  requests.Timeout :
        with open(pathexceptions+f"\\Timeout.txt", 'w') as f:
            
            f.write(f"{mytime} | Timeout, when login ,delay to resending is {delayConnection}")
        delayConnection*=2
        time.sleep(delayConnection)
        

print(r.content)
try:
    Token_value=r.json()['access_token']
except:
     with open(pathexceptions+f"\\No access_token.txt", 'wb') as f:
            #data.raw.decode_content = True
            f.write(r.content)
            print('exit No access_token')
            exit()
headers = {"Authorization":f"Bearer {Token_value}"}
print(headers)
#download
def downloadInv(date=date,isSent=False,isReceived=False,pageSize=pageSize,isjson=isjson,isPDF=False):
    mytime=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    directionSent='Sent'
    directionReceived='Received'
    direction=directionReceived
    if(isSent):
        direction=directionSent
    if(isReceived):
        direction=directionReceived  

    path=SavingLoction+f"\{date}\{direction}"
    if not os.path.exists(path):
        os.makedirs(path)

    searchPackagesurl=searchPackages(date=date,pageSize=pageSize,direction=direction)
    time.sleep(DelayCallAPI)
    delayConnection=initDelay
    noConnection=True
    while(noConnection):
        try:
            r1 = requests.get(searchPackagesurl,data=headers,headers=headers,timeout=timeout)
            noConnection=False
            delayConnection=initDelay   
            try:
                    if os.path.isfile(pathexceptions+f"\\Timeout.txt"):
                        os.remove(pathexceptions+f"\\Timeout.txt")      
                    if os.path.isfile(pathexceptions+f"\\No internet.txt"):
                        os.remove(pathexceptions+f"\\No internet.txt")
            except :
                print("can`t remove")
        except requests.exceptions.ConnectionError as e:
            with open(pathexceptions+f"\\No internet.txt", 'w') as f:
                    
                f.write(f"{mytime} | No internet, when get inv ,delay to resending is {delayConnection}")
            delayConnection*=2
            time.sleep(delayConnection)    
        except  requests.Timeout :
            with open(pathexceptions+f"\\Timeout.txt", 'w') as f:
                
                f.write(f"{mytime} | Timeout, when get inv ,delay to resending is {delayConnection}")
            delayConnection*=2
            time.sleep(delayConnection)
                
            
    print(r1.content)

    try:
        result=r1.json()['result']
    except :
        with open(path+f"\\No Result.txt", 'wb') as f:
            #data.raw.decode_content = True
            f.write(r1.content)
            print('exit No Result')
            exit()
    if(isjson):
        with open(path+f"\{date}-{directionSent}.json", 'w', encoding="utf-8") as f:
            #data.raw.decode_content = True
            f.write(str(result))
    if(isPDF):
        for inv in result:
            uuid=inv['uuid']
            internalId=inv['internalId']
            typeName=inv['typeName']
            receiverId=  inv['receiverId'] if(direction==directionSent) else inv['issuerId']
            uuid=inv['uuid']
            uuid=inv['uuid']

            time.sleep(DelayCallAPI)
            noConnection=True
            while(noConnection):
                try:
                    r2 = requests.get(documentPdfUrl(uuid),data=headers,headers=headers)
                    noConnection=False
                    delayConnection=initDelay
                    try:
                        if os.path.isfile(pathexceptions+f"\\Timeout.txt"):
                            os.remove(pathexceptions+f"\\Timeout.txt")
                        if os.path.isfile(pathexceptions+f"\\No internet.txt"):
                            os.remove(pathexceptions+f"\\No internet.txt")
                    except :
                        print("can`t remove")
                        
                except requests.exceptions.ConnectionError as e:
                    with open(pathexceptions+f"\\No internet.txt", 'w') as f:
                        
                        f.write(f"{mytime} | No internet, when download Pdf ,delay to resending is {delayConnection}")
                    delayConnection*=2
                    time.sleep(delayConnection)
                except  requests.Timeout :
                    with open(pathexceptions+f"\\Timeout.txt", 'w') as f:
                        
                        f.write(f"{mytime} | Timeout, when download Pdf ,delay to resending is {delayConnection}")
                delayConnection*=2
                time.sleep(delayConnection)    

                
                
        
            with open(path+f"\{uuid}-{typeName}-{receiverId}.pdf", 'wb') as f:
                #data.raw.decode_content = True
                f.write(r2.content)

        print(len(result))  


def print_all_days_in_year(year,isjson=isjson,isPDF=False):
    """Prints all days of a given year.

    Args:
        year: The year for which to print the days (integer).
    """

    if not isinstance(year, int):
        raise TypeError("Year must be an integer.")

    if year < 0:  # Or any other reasonable lower bound
        raise ValueError("Year must be a non-negative integer.")


    for month in range(1, 13):  # Months are 1-indexed
        for day in range(1, calendar.monthrange(year, month)[1] + 1): 
                print(f"{year}-{month:02}-{day:02}")
                downloadInv(f"{year}-{month:02}-{day:02}",True,pageSize=5,isjson=isjson,isPDF=isPDF)
                downloadInv(f"{year}-{month:02}-{day:02}",isReceived=True,pageSize=4,isjson=isjson,isPDF=isPDF)
#print(result.json()['result'])
# receiver
downloadInv(date,True,pageSize=5)
downloadInv(date,isReceived=True,pageSize=4)

if(isYear):
    print(Year)
    print_all_days_in_year(Year,isjson=isjson)
# uuid-internalId-typeName-date-receiverId-typeName
# {uuid}-{internalId}-{typeName}-{receiverId}