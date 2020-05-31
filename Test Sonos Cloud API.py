from bs4 import BeautifulSoup
import requests
import json
import lxml
import base64
from basicauth import encode
import logging
import http.client as http_client
from urllib.parse import urlparse

from SonosAPISettings import AUTH_URL, SONOS_CLIENT_ID,SONOS_CLIENT_SECRET,CLIENT_REDIRECT_URL,CLIENT_SCOPE,SONOS_TEST_STATE,SIGNIN_URL,SONOS_USER_ID,SONOS_PASSWORD,ACCESS_TOKEN_URL,SONOS_CONTROL_API_BASE_URL

http_client.HTTPConnection.debuglevel = 0
session_requests = requests.Session()

url = AUTH_URL
params = {
           'client_id'     : SONOS_CLIENT_ID,
           'response_type' : 'code',
           'state'         : SONOS_TEST_STATE,
           'scope'         : CLIENT_SCOPE,
           'redirect_uri'  : CLIENT_REDIRECT_URL
        }
response = session_requests.get(url,params=params)
session_requests.close()
print ("First Get API : Create Authorization Code: ",response)

soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       break

payload = {
           '_csrf': MyKey , 
           'value' : "Continue"
          }
response = session_requests.post(url,data=payload,params=params)
session_requests.close()
print ("First Authorization API Continue : Create Authorisation Code (Post) : ",response)

url_Signin = SIGNIN_URL
payload = {
           '_csrf'     : MyKey ,
           'username'  : SONOS_USER_ID,
           'password'  : SONOS_PASSWORD,
           'grant_type':'password'
           }
response = session_requests.post(url_Signin,data=payload)
session_requests.close()
print ("Signin Process :",response)
soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       break

url = url+"/authorize"
encoded_str= encode(SONOS_CLIENT_ID,SONOS_CLIENT_SECRET)
headers = {'Authorization' : encoded_str }
payload = {
           '_csrf'       : MyKey,
           'clientId'    : SONOS_CLIENT_ID,
           'redirectUri' : CLIENT_REDIRECT_URL,
           'responseType':"code",
           'authScope'   : CLIENT_SCOPE,
           'authState'   : SONOS_TEST_STATE,
           'action'      : 'submit'
          }
response = session_requests.post(url,params=params,headers=headers,data=payload)
session_requests.close()
print ("First Authorization API Okay : Give Consent - Return Code (Post) : ",response)
urlwithcode=urlparse(response.url)
ac=urlwithcode[4][-8:]

url = ACCESS_TOKEN_URL
headers = {'Authorization' : encoded_str}
payload = {
           'grant_type': 'authorization_code',
           'code' : ac,
           'redirectUri': CLIENT_REDIRECT_URL
          }
response = session_requests.post(url,params=params,headers=headers,data=payload)
session_requests.close()
print ('Second Authorization API (Create Token): ',response)
Token = json.loads(response.text)
AccessToken = Token["access_token"]
RefreshToken = Token["refresh_token"]

url = SONOS_CONTROL_API_BASE_URL + "/households"
headers = {
           'Authorization' : 'Bearer '+AccessToken,
           'Content-Type' : 'application/json',
          }
response = session_requests.get(url,headers=headers)
session_requests.close()
print("Sonos Control API Discovery : Query HouseHold : ",response)
data = json.loads(response.text)
HouseHold = data["households"]
HouseHoldId = HouseHold[0]
HouseHoldId = HouseHoldId["id"]
print ("HouseHoldid : ",HouseHoldId)

url = SONOS_CONTROL_API_BASE_URL + "/households/" + HouseHoldId + "/groups"
headers = {
           'Authorization' : 'Bearer '+ AccessToken,
           'Content-Type' : 'application/json',
          }
response = session_requests.get(url,headers=headers)
session_requests.close()
print("Sonos Control API Discovery : Query Groups : ",response)
Groups = json.loads(response.text)
GroupsList = Groups['groups']
# print("Groups : ",GroupsList)
Group_Names = [group['name'] for group in GroupsList]
Group_Ids   = [group['id'] for group in GroupsList]
print ("Group Names : ",Group_Names)
print ("Group Ids   : ",Group_Ids)

url = SONOS_CONTROL_API_BASE_URL + "/households/" + HouseHoldId + "/playlists"
headers = {
           'Authorization' : 'Bearer '+ AccessToken,
           'Content-Type' : 'application/json',
          }
response = session_requests.get(url,headers=headers)
session_requests.close()
print("Sonos Control API Discovery : Query Playlists : ",response)
print ("PlayList : ",response.text)
PlayLists = json.loads (response.text)
PlayLists = PlayLists ['playlists']
PlayList_Names = [playlist['name']for playlist in PlayLists]
PlayList_Ids   = [playlist['id']for playlist in PlayLists]
print ("PlayLists Names : ",PlayList_Names)
print ("PlayLists Ids   : ",PlayList_Ids)

# GroupId = 'RINCON_7828CAFC491A01400:2981147567'
GroupId = 'RINCON_B8E93772FB9401400:312'
# GroupId = 'RINCON_B8E937D796BA01400:3792525276'

PlayListId = "27"
PlayListId = "10"
url = SONOS_CONTROL_API_BASE_URL + "/groups/" + GroupId + "/playlists"
headers = {
           'Authorization' : 'Bearer '+ AccessToken,
           'Content-Type' : 'application/json'
          }
payload = {
            'action' : 'REPLACE',
            'playlistId' : f'{PlayListId}',
            'playOnCompletion' : True,
            'playModes' : {
                            'shuffle' : True
                          }
          }
payload = json.dumps(payload)
response = session_requests.post(url,data=payload,headers=headers)
session_requests.close()
print("Sonos Control API  : LoadPlaylist : ",response)
print ("response : ",response.text)

url = SONOS_CONTROL_API_BASE_URL + "/groups/" + GroupId + "/playback/play"
headers = {
           'Authorization' : 'Bearer '+ AccessToken,
           'Content-Type' : 'application/json'
          }
response = session_requests.post(url,headers=headers)
session_requests.close()
print("Sonos Control API  : Playback\Play : ",response)

url = SONOS_CONTROL_API_BASE_URL + "/groups/" + GroupId + "/playback"
headers = {
           'Authorization' : 'Bearer '+ AccessToken,
           'Content-Type' : 'application/json'
          }
response = session_requests.get(url,headers=headers)
session_requests.close()
print("Sonos Control API  : Playback Status : ",response)
print("PlayBack Status : ",response.text)