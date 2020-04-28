# -*- coding: utf-8 -*-
"""This module contains methods for discovering Sonos devices on the
network."""

from __future__ import unicode_literals

import logging
import socket
import select
from textwrap import dedent
import time
import struct

from soco import config
from soco.utils import really_utf8

_LOG = logging.getLogger(__name__)

# pylint: disable=too-many-locals, too-many-branches

def discover(timeout=5, include_invisible=False, interface_addr=None):
    
    def create_socket(interface_addr=None):
        _sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # UPnP v1.0 requires a TTL of 4
        _sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack("B", 4)
        )
        if interface_addr is not None:
            _sock.setsockopt(
                socket.IPPROTO_IP,
                socket.IP_MULTICAST_IF,
                socket.inet_aton(interface_addr),
            )
        return _sock
    # pylint: disable=invalid-name
    PLAYER_SEARCH = dedent(
        """\
        M-SEARCH * HTTP/1.1
        HOST: 239.255.255.250:1900
        MAN: "ssdp:discover"
        MX: 1
        ST:ssdp:all
        """
        # ST: urn:schemas-upnp-org:device:ZonePlayer:1
    ).encode("utf-8")
    MCAST_GRP = "239.255.255.250"
    MCAST_PORT = 1900
    
    _sockets = []
    # Use the specified interface, if any
    if interface_addr is not None:
        try:
            address = socket.inet_aton(interface_addr)
        except socket.error:
            raise ValueError(
                "{0} is not a valid IP address string".format(interface_addr)
            )
        _sockets.append(create_socket(interface_addr))
        _LOG.info("Sending discovery packets on default interface")
    else:
        # Find the local network address using a couple of different methods.
        # Create a socket for each unique address found, and one for the
        # default multicast address
        addresses = set()
        try:
            addresses.add(socket.gethostbyname(socket.gethostname()))
        except socket.error:
            pass
        try:
            addresses.add(socket.gethostbyname(socket.getfqdn()))
        except socket.error:
            pass
        for address in addresses:
            try:
                _sockets.append(create_socket(address))
            except socket.error as e:
                _LOG.warning(
                    "Can't make a discovery socket for %s: %s: %s",
                    address,
                    e.__class__.__name__,
                    e,
                )
        # Add a socket using the system default address
        _sockets.append(create_socket())
        # Used to be logged as:
        # list(s.getsockname()[0] for s in _sockets)
        # but getsockname fails on Windows with unconnected unbound sockets
        # https://bugs.python.org/issue1049
        _LOG.info("Sending discovery packets on %s", _sockets)

    for _ in range(0, 3):
        # Send a few times to each socket. UDP is unreliable
        for _sock in _sockets:
            _sock.sendto(really_utf8(PLAYER_SEARCH), (MCAST_GRP, MCAST_PORT))

    t0 = time.time()
    while True:
        # Check if the timeout is exceeded. We could do this check just
        # before the currently only continue statement of this loop,
        # but I feel it is safer to do it here, so that we do not forget
        # to do it if/when another continue statement is added later.
        # Note: this is sensitive to clock adjustments. AFAIK there
        # is no monotonic timer available before Python 3.3.
        t1 = time.time()
        if t1 - t0 > timeout:
            return None

        # The timeout of the select call is set to be no greater than
        # 100ms, so as not to exceed (too much) the required timeout
        # in case the loop is executed more than once.
        response, _, _ = select.select(_sockets, [], [], min(timeout, 0.1))

        # Only Zone Players should respond, given the value of ST in the
        # PLAYER_SEARCH message. However, to prevent misbehaved devices
        # on the network disrupting the discovery process, we check that
        # the response contains the "Sonos" string; otherwise we keep
        # waiting for a correct response.
        #
        # Here is a sample response from a real Sonos device (actual numbers
        # have been redacted):
        # HTTP/1.1 200 OK
        # CACHE-CONTROL: max-age = 1800
        # EXT:
        # LOCATION: http://***.***.***.***:1400/xml/device_description.xml
        # SERVER: Linux UPnP/1.0 Sonos/26.1-76230 (ZPS3)
        # ST: urn:schemas-upnp-org:device:ZonePlayer:1
        # USN: uuid:RINCON_B8*************00::urn:schemas-upnp-org:device:
        #                                                     ZonePlayer:1
        # X-RINCON-BOOTSEQ: 3
        # X-RINCON-HOUSEHOLD: Sonos_7O********************R7eU
        
        if response:
            for _sock in response:
                data, addr = _sock.recvfrom(1024)
                print (addr)
                print (data)
                _LOG.debug('Received discovery response from %s: "%s"', addr, data)
                
                #if b"Sonos" in data:
                    # Now we have an IP, we can build a SoCo instance and query
                    # that player for the topology to find the other players.
                    # It is much more efficient to rely upon the Zone
                    # Player's ability to find the others, than to wait for
                    # query responses from them ourselves.
                    # zone = config.SOCO_CLASS(addr[0])
                    # if include_invisible:
                    #     return zone.all_zones
                    # else:
                    #    return zone.visible_zones
    return "End of Discovery"


