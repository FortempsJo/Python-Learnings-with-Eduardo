import sys
sys.path.append('c:\\Users\\José\\Skydrive\\Documents\\Programming\\Python\\CLI-Sonos')

from sonos.config import local_store

ACTIVE_GROUP_FILE = 'group.json'


def save_active_group(group_id):
    local_store.save(ACTIVE_GROUP_FILE, group_id)


def get_active_group():
    return local_store.load(ACTIVE_GROUP_FILE)
