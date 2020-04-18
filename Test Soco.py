import soco
speakers_list = soco.discover()
print (speakers_list)
for speaker in speakers_list:
    print (speaker.player_name + " : " + speaker.ip_address)    

print ("Second Iteration")

speaker = speakers_list.pop()
print (speaker.player_name + " : " + speaker.ip_address)

from soco.discovery import by_name
Name_Speaker = input ("Donne moi le nom du Sonos : ")
# Name_Speaker = "Office"
speaker =by_name(Name_Speaker)
print (speaker.player_name + " : " + speaker.ip_address)
speaker.play()

Track = speaker.get_current_track_info()
Next_Track = input ("Allez à la piste suivante : (OK/NOK) : ")
print ("Input donné : " + Next_Track)
if Next_Track == "OK": 
   print ("Go to next track !!!")
   speaker.next()
# else print ("No Go to Next Track !!!")











