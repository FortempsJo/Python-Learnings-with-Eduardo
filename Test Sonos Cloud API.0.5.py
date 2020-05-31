from bs4 import BeautifulSoup
import requests
import json
import lxml
import base64
from requests.auth import HTTPBasicAuth
from basicauth import encode
import logging
import http.client as http_client
from urllib.parse import urlparse
http_client.HTTPConnection.debuglevel = 1

session_requests = requests.Session()
response = session_requests.get("https://api.sonos.com/login/v3/oauth?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&scope=playback-control-all&redirect_uri=https://fortempssonos.ddns.net")
print ("First Query Get : ",response)
print ("reponse.history first Get : ",response.history)
# print ("Response Headers first Get : ",response.headers)
# print ("Response First Get : ",response.text)
soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       print ("Found MyKey : ",MyKey)
       break

url = "https://api.sonos.com/login/v3/oauth?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&scope=playback-control-all&redirect_uri=https://fortempssonos.ddns.net"
payload = {'name':'_csrf' , '_csrf': MyKey , 
           'response_type': 'code',
           'value' : "Continue"
          }
response = session_requests.post(url,payload)
print ("response first post : ",response)
print ("reponse.history first post : ",response.history)

clientid='jose.fortemps@outlook.com'
secret='Mexico13'
url = "https://api.sonos.com/login/v3/signin"
payload = {'name':'_csrf' , '_csrf': MyKey ,
           'username':clientid,
           'password':secret,
           'grant_type':'password'
           }
response = session_requests.post(url,data=payload)
print ("response second post:",response)
print ("reponse.history second post : ",response.history)
soup = BeautifulSoup(response.text, 'lxml')
Attribs_list = soup.find_all("input")
for Attribs in Attribs_list:
    if Attribs['id'] == "csrf-token":
       MyKey = Attribs['value']
       print ("Found MyKey 2 : ",MyKey)
       break

encoded_str= encode('746927e2-5bd0-4f90-81cf-b39b7c8d55a6','c5715943-1337-4a85-8f4d-dc839974c41c')
cs = clientid+secret
cs_byte = cs.encode('ascii')
b64cs_byte = base64.b64encode(cs_byte)
b64cs = b64cs_byte.decode('ascii')

url = "https://api.sonos.com/login/v3/oauth/authorize?client_id=746927e2-5bd0-4f90-81cf-b39b7c8d55a6&response_type=code&state=test_state&redirect_uri=https://fortempssonos.ddns.net&scope=playback-control-all"
print ("My Key 2 : ",MyKey)
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
print (headers)
response = session_requests.post(url,data=payload,headers=headers,allow_redirects=True)
print ('reponse third post : ',response)
print(response.history)
urlwithcode=urlparse(response.url)
print(urlwithcode[4])
poscode=urlwithcode[4].find("&code=")
print(poscode)
auth_code=urlwithcode[4][-8:]
print(auth_code)
# rr = response.raw
# print ("Response Raw : ",rr)
# print(rr.read())

ac = auth_code
ac = "cYqn33SH"
ac_byte = ac.encode('ascii')
b64ac_byte = base64.b64encode(ac_byte)
b64ac = b64ac_byte.decode('ascii')
print ("base 64 auth code : "+b64ac)

headers = {
           'Authorization' : 'Bearer '+ac,
           'Content-Type' : 'application/json',
           'Content-Length' : '0',
           'User-Agent' : 'Apache-HttpClient/4.5.10 (Java/1.8.0_162)'
          }
print (headers)
url = "https://api.ws.sonos.com/control/api/v1/households"
payload = {'authScope':"playback-control-all"}
response = session_requests.get(url,data=payload,headers=headers,allow_redirects=True)
print(response)
print(response.headers)
print(response.text)


