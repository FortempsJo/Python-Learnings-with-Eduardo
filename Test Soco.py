import soco
speakers = soco.discover()
print (speakers)
for speaker in soco.discover():
    print (speaker.player_name)


