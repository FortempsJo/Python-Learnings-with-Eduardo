from soco.discovery import any_soco
from soco.services import *

player = any_soco()

service_classes = [
    AVTransport,
    ContentDirectory,
    DeviceProperties,
    RenderingControl,
    ZoneGroupTopology,
    AlarmClock,
    SystemProperties,
    MusicServices,
    Queue,
    GroupManagement,
    GroupRenderingControl,
]

for service_class in service_classes:
    service = service_class(player)
    print("## {}".format(service.service_type))
    for action in service.iter_actions():
        print("* `", action, "`")
    print()
    