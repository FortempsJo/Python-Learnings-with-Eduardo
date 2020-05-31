from bs4 import BeautifulSoup
import requests
import json
import lxml
import base64
from basicauth import encode
import logging
import http.client as http_client
from urllib.parse import urlparse
from requests_oauthlib import OAuth2Session
http_client.HTTPConnection.debuglevel = 1

session_requests = requests.Session()
response = session_requests.get("https://api.sonos.com/login/v3/oauth?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&scope=playback-control-all&redirect_uri=https://fortempssonos.ddns.net")
print ("First Query Get (AUthorize): ",response)
soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       break

url = "https://api.sonos.com/login/v3/oauth?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&scope=playback-control-all&redirect_uri=https://fortempssonos.ddns.net"
payload = {'name':'_csrf' , '_csrf': MyKey , 
           'response_type': 'code',
           'value' : "Continue"
          }
response = session_requests.post(url,payload)
print ("response first post (Authorize) : ",response)

clientid='jose.fortemps@outlook.com'
secret='Mexico13'
url = "https://api.sonos.com/login/v3/signin"
payload = {'name':'_csrf' , '_csrf': MyKey ,
           'username':clientid,
           'password':secret,
           'grant_type':'password'
           }
response = session_requests.post(url,data=payload)
print ("response second post (Signin) :",response)
soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       break

encoded_str= encode('746927e2-5bd0-4f90-81cf-b39b7c8d55a6','c5715943-1337-4a85-8f4d-dc839974c41c')
url = "https://api.sonos.com/login/v3/oauth/authorize?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&redirect_uri=https://fortempssonos.ddns.net&scope=playback-control-all"
payload = {
           '_csrf': MyKey,
           'clientId':"746927e2-5bd0-4f90-81cf-b39b7c8d55a6",
           'redirectUri':"https://fortempssonos.ddns.net",
           'responseType':"code",
           'authScope':"playback-control-all",
           'authState':"test_state",
           'action':'submit'
          }
headers = {'Authorization' : encoded_str }
response = session_requests.post(url,data=payload,headers=headers,allow_redirects=True)
print ('reponse third post (Authorize : get code): ',response)
urlwithcode=urlparse(response.url)
ac=urlwithcode[4][-8:]

headers = {
           'Authorization' : encoded_str,
          }
url = "https://api.sonos.com/login/v3/oauth/access?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&redirect_uri=https://fortempssonos.ddns.net&scope=playback-control-all"
payload = {
           'grant_type': 'authorization_code',
           'code' : ac,
           'redirectUri':"https://fortempssonos.ddns.net",
          }
response = session_requests.post(url,data=payload,headers=headers,allow_redirects=True)
print ('reponse fourth post (Access : Post Access Token): ',response)
Token = json.loads(response.text)
AccessToken = Token["access_token"]
RefreshToken = Token["refresh_token"]
print ("Tokens : ",AccessToken," - ", RefreshToken)

headers = {
           'Authorization' : 'Bearer '+AccessToken,
           'Content-Type' : 'application/json',
           'Content-Length' : '0',
           'User-Agent' : 'Apache-HttpClient/4.5.10 (Java/1.8.0_162)'
          }
url = "https://api.ws.sonos.com/control/api/v1/households"
payload = {'authScope':"playback-control-all"}
response = session_requests.get(url,data=payload,headers=headers,allow_redirects=True)
print("Query HouseHold : ",response)
print("Query HouseHold : ",response.headers)

data = json.loads(response.text)
HouseHold = data["households"]
print (HouseHold)
HouseHoldId = HouseHold[0]
HouseHoldId = HouseHoldId["id"]
print ("HouseHoldid : ",HouseHoldId)

# ---------------------------  Refresh Access Token ------------------------------------------ #
# headers = {
#           'Authorization' : encoded_str,
#          }
# url = "https://api.sonos.com/login/v3/oauth/access"
# payload = {
#            'grant_type': 'refresh_token',
#            'refresh_token' : RefreshToken
#           }
# response = session_requests.post(url,data=payload,headers=headers,allow_redirects=True)
# print ('reponse Fifth post (Access : Refresh Access Token): ',response)
# data = json.loads(response.text)
# print ("Refresh Token Response : ",data)
# AccessToken = data["access_token"]
# RefreshToken = data["refresh_token"]
# print ("Tokens 2 : ",AccessToken," - ", RefreshToken)
# print ('Token = ',Token)
# session_requests = OAuth2Session(token=Token)
# print (' Query Hearders Get Groups : ',session_requests.headers)
# print (' Query params Get Groups : ',session_requests.params)
# print ('Query Scope Get Groups : ',session_requests.scope)
# print ('Query Token Get Groups : ',session_requests.token)
# print ('Query State Get Groups : ',session_requests.state)
# print ('Query Kwargs Get Groups : ',session_requests._client)
# print (session_requests.client_id)

# ---------------------------- Get Groups ---------------------------------------------------- #

url = "https://api.ws.sonos.com/control/api/v1/households/" + HouseHoldId + "/groups"
response = session_requests.get(url)
print ('response.url : ',response.url)
print ('response.headers : ',response.headers)
print ('response.text : ',response.text)

headers = {
           'Authorization' : 'Bearer '+ AccessToken
          }
response = session_requests.get(url,headers=headers)

print("Query Groups : ",response)
print("Headers : ",response.headers)
print("Groups : ",response.text)

