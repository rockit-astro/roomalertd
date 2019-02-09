#!/usr/bin/env python3.6
#
# This file is part of roomalertd.
#
# roomalertd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# roomalertd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with roomalertd.  If not, see <http://www.gnu.org/licenses/>.

"""Simulates the output of the broken HTTP server in the roomalerts"""

import datetime
import random
import socket

PORT = 1234
ROOMALERT_TEMP = (25, 30)
ROOMALERT_HUMIDITY = (5, 15)
EXTERNAL_TEMP = (10, 20)
EXTERNAL_HUMIDITY = (80, 100)
INTERNAL_TEMP = (15, 25)
INTERNAL_HUMIDITY = (60, 80)
TRUSS_TEMP = (15, 25)
ON_BATTERY = False
HATCH_CLOSED = True
TRAP_CLOSED = False

DATA_TEMPLATE = '{{"name":"SAFT Dome","date":"{}","uptime":"{}","scale":1,'\
    '"macaddr":"00:20:4A:F0:AB:DC","devtype":"32","refresh":"60","channel":"12",'\
    '"picvers":"04","msus_expires":"","display_expiration":"0","interval":"60",'\
    '"gtmd_interval":"3600","version":"v2.5.1","port":80,"ip":"{}",'\
    '"serial":"RA32-123797","internal_sen":[{{"lab":"InternalMaster","tf":"{:.2f}",'\
    '"tc":"{:.2f}","hf":"{:.2f}","hc":"{:.2f}","hic":"{:.2f}","lf":"{:.2f}","lc":"{:.2f}",'\
    '"ala":0,"t":38,"en":1,"h":"{:.2f}","hh":"{:.2f}","lh":"{:.2f}","hi":"{:.2f}",'\
    '"hic":"{:.2f}","hhi":"{:.2f}","hhic":"{:.2f}","lhi":"{:.2f}","lhic":"{:.2f}","hen":0}},'\
    '{{"lab":"Analog Sensor 1","volts":"2.55","highv":"2.91","lowv":"0.00","units":'\
    '{{"refMin":"0","refMax":"0","scaleMin":"0","scaleMax":"0","sym":"V","en":"0"}},'\
    '"ala":"0","t":"65","en":"0"}},{{"lab":"Analog Sensor 2","volts":"2.67","highv":"2.72",'\
    '"lowv":"2.57","units":{{"refMin":"0","refMax":"0","scaleMin":"0","scaleMax":"0",'\
    '"sym":"V","en":"0"}},"ala":"0","t":"65","en":"0"}},{{"lab":"Power Sensor","t":"power",'\
    '"stat":{},"ala":1}}],"signal_twr":[{{"RE":{{"en":0,"stat":0}},"OR":{{"en":0,"stat":0}},'\
    '"GR":{{"en":0,"stat":0}},"BL":{{"en":0,"stat":0}},"WH":{{"en":0,"stat":0}},"A1":{{"en":0,'\
    '"stat":0}},"A2":{{"en":0,"stat":0}},"RY":{{"en":0,"stat":0}},"attach_type":0,'\
    '"lab":"Light Tower 1","tower_id":1}},{{"RE":{{"en":0,"stat":0}},"OR":{{"en":0,'\
    '"stat":0}},"GR":{{"en":0,"stat":0}},"BL":{{"en":0,"stat":0}},"WH":{{"en":0,"stat":0}},'\
    '"A1":{{"en":0,"stat":0}},"A2":{{"en":0,"stat":0}},"RY":{{"en":0,"stat":0}},'\
    '"attach_type":0,"lab":"Light Tower 2","tower_id":2}}],"relay":[{{"lab":'\
    '"Relay Output 1","stat":0,"relay_id":1}},{{"lab":"Relay Output 2","stat":0,'\
    '"relay_id":2}}],"sensor":[{{"lab":"External","tf":"{:.2f}","tc":"{:.2f}",'\
    '"hf":"{:.2f}","hc":"{:.2f}","hic":"{:.2f}","lf":"{:.2f}","lc":"{:.2f}","ala":0,'\
    '"t":38,"en":1,"h":"{:.2f}","hh":"{:.2f}","lh":"{:.2f}","hi":"{:.2f}","hic":"{:.2f}",'\
    '"hhi":"{:.2f}","hhic":"{:.2f}","lhi":"{:.2f}","lhic":"{:.2f}","hen":0}},{{"lab":"Internal",'\
    '"tf":"{:.2f}","tc":"{:.2f}","hf":"{:.2f}","hc":"{:.2f}","hic":"{:.2f}","lf":"{:.2f}",'\
    '"lc":"{:.2f}","ala":0,"t":38,"en":1,"h":"{:.2f}","hh":"{:.2f}","lh":"{:.2f}",'\
    '"hi":"{:.2f}","hic":"{:.2f}","hhi":"{:.2f}","hhic":"{:.2f}","lhi":"{:.2f}","lhic":"{:.2f}",'\
    '"hen":0}},{{"lab":"Truss","tf":"{:.2f}","tc":"{:.2f}","hf":"{:.2f}","hc":"{:.2f}",'\
    '"hic":"{:.2f}","lf":"{:.2f}","lc":"{:.2f}","ala":0,"t":38,"en":0}},{{"lab":"Ext. Sensor'\
    '4","tf":"76.10","tc":"24.50","hf":"89.81","hc":"32.12","hic":"32.12","lf":"63.60","lc":"17.56'\
    '","ala":0,"t":0,"en":0}},{{"lab":"Ext. Sensor 5","tf":"32.00","tc":"0.00","hf":"32.00",'\
    '"hc":"0.00","hic":"0.00","lf":"32.00","lc":"0.00","ala":0,"t":0,"en":0}},'\
    '{{"lab":"Ext. Sensor 6","tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00","hic":"0.00",'\
    '"lf":"32.00","lc":"0.00","ala":0,"t":0,"en":0}},{{"lab":"Ext. Sensor 7","tf":"32.00",'\
    '"tc":"0.00","hf":"32.00","hc":"0.00","hic":"0.00","lf":"32.00","lc":"0.00","ala":0,"t":0,'\
    '"en":0}},{{"lab":"Ext. Sensor 8","tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00",'\
    '"hic":"0.00","lf":"32.00","lc":"0.00","ala":0,"t":0,"en":0}}],"s_sen":[{{"lab":"Hatch",'\
    '"en":1,"ala":1,"stat":{}}},{{"lab":"Trap","en":1,"ala":1,"stat":{}}},'\
    '{{"lab":"Switch Sen 3","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 4","en":1,"ala":1,'\
    '"stat":0}},{{"lab":"Switch Sen 5","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 6","en":1,'\
    '"ala":1,"stat":0}},{{"lab":"Switch Sen 7","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 8",'\
    '"en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 9","en":1,"ala":1,"stat":0}},'\
    '{{"lab":"Switch Sen 10","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 11","en":1,"ala":1,'\
    '"stat":0}},{{"lab":"Switch Sen 12","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 13","en":1,'\
    '"ala":1,"stat":0}},{{"lab":"Switch Sen 14","en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 15",'\
    '"en":1,"ala":1,"stat":0}},{{"lab":"Switch Sen 16","en":1,"ala":1,"stat":0}}],'\
    '"wireless_sen":[{{"lab":"No WiSH 1","ala":0,"ser":"000000000000","en":0,"in":-1,"tstamp":'\
    '"08/04/15 17:27:26","upd":"0","rssi":"0","bat":"0.00","t":0,"tf":"32.00","tc":"0.00",'\
    '"hf":"32.00","hc":"0.00","lf":"32.00","lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,'\
    '"ala":0,"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4",'\
    '"en":1,"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,"ser":"000000000000","en":0,'\
    '"in":-1,"tstamp":"08/04/15 17:27:26","upd":"0","rssi":"0","bat":"0.00","t":0,'\
    '"tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00","lf":"32.00","lc":"0.00",'\
    '"digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,'\
    '"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1",'\
    '"ala":0,"ser":"000000000000","en":0,"in":-1,"tstamp":"08/04/15 17:27:26","upd":"0",'\
    '"rssi":"0","bat":"0.00","t":0,"tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00",'\
    '"lf":"32.00","lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,"t":0}},'\
    '{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,'\
    '"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,"ser":"000000000000","en":0,"in":-1,'\
    '"tstamp":"08/04/15 17:27:26","upd":"0","rssi":"0","bat":"0.00","t":0,"tf":"32.00",'\
    '"tc":"0.00","hf":"32.00","hc":"0.00","lf":"32.00","lc":"0.00","digi_sen":[{{'\
    '"lab":"No WiSH 2","en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],'\
    '"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,'\
    '"ser":"000000000000","en":0,"in":-1,"tstamp":"08/04/15 17:27:26","upd":"0","rssi":"0",'\
    '"bat":"0.00","t":0,"tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00","lf":"32.00",'\
    '"lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3",'\
    '"en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,"stat":0}}]}},'\
    '{{"lab":"No WiSH 1","ala":0,"ser":"000000000000","en":0,"in":-1,"tstamp":'\
    '"08/04/15 17:27:26","upd":"0","rssi":"0","bat":"0.00","t":0,"tf":"32.00","tc":"0.00",'\
    '"hf":"32.00","hc":"0.00","lf":"32.00","lc":"0.00","digi_sen":[{{"lab":"No WiSH 2",'\
    '"en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":'\
    '"No WiSH 4","en":1,"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,"ser":'\
    '"000000000000","en":0,"in":-1,"tstamp":"08/04/15 17:27:26","upd":"0","rssi":"0",'\
    '"bat":"0.00","t":0,"tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00","lf":"32.00",'\
    '"lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3",'\
    '"en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,"stat":0}}]}},{{"lab":'\
    '"No WiSH 1","ala":0,"ser":"000000000000","en":0,"in":-1,"tstamp":"08/04/15 17:27:26",'\
    '"upd":"0","rssi":"0","bat":"0.00","t":0,"tf":"32.00","tc":"0.00","hf":"32.00",'\
    '"hc":"0.00","lf":"32.00","lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,'\
    '"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,'\
    '"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,"ser":"000000000000","en":0,"in":-1,'\
    '"tstamp":"08/04/15 17:27:26","upd":"0","rssi":"0","bat":"0.00","t":0,"tf":"32.00",'\
    '"tc":"0.00","hf":"32.00","hc":"0.00","lf":"32.00","lc":"0.00","digi_sen":[{{"lab":'\
    '"No WiSH 2","en":0,"ala":0,"t":0}},{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],'\
    '"s_sen":[{{"lab":"No WiSH 4","en":1,"ala":0,"stat":0}}]}},{{"lab":"No WiSH 1","ala":0,'\
    '"ser":"000000000000","en":0,"in":-1,"tstamp":"08/04/15 17:27:26","upd":"0",'\
    '"rssi":"0","bat":"0.00","t":0,"tf":"32.00","tc":"0.00","hf":"32.00","hc":"0.00",'\
    '"lf":"32.00","lc":"0.00","digi_sen":[{{"lab":"No WiSH 2","en":0,"ala":0,"t":0}},'\
    '{{"lab":"No WiSH 3","en":0,"ala":0,"t":0}}],"s_sen":[{{"lab":"No WiSH 4","en":1,'\
    '"ala":0,"stat":0}}]}}]}}'

# pylint: disable=invalid-name
# pylint: disable=too-few-public-methods

def fahrenheit(tc):
    """Convert a temperature in deg C to fahrenheit"""
    return tc * 9. / 5 + 32

def heat_index(h, tc):
    """Calculate the heat index for a given humidity and temperature"""
    c1 = -42.379
    c2 = 2.04901523
    c3 = 10.14333127
    c4 = -0.22475541
    c5 = -6.83783E-3
    c6 = -5.481717E-2
    c7 = 1.22874E-3
    c8 = 8.5282E-4
    c9 = -1.99E-6
    tf = fahrenheit(tc)
    return c1 + c2*tf + c3*h + c4*tf*h + c5*tf*tf + c6*h*h + c7*tf*tf*h + c8*tf*h*h + c9*tf*tf*h*h

class TemperatureSensor:
    """Simulated temperature sensor that returns a random temperature within
       the defined limits"""
    def __init__(self, t_lim):
        self.hc = t_lim[1]
        self.lc = t_lim[0]
        self.tc = 0 # Value is set in values()

    def values(self):
        """Returns the format parameters for this sensor"""
        self.tc = self.lc + (self.hc - self.lc) * random.random()
        return (
            fahrenheit(self.tc),
            self.tc,
            fahrenheit(self.hc),
            self.hc,
            self.hc,
            fahrenheit(self.lc),
            self.lc)

class TemperatureHumiditySensor:
    """Simulated temperature+humidity sensor that returns random temp+humidity
       within the defined limits"""
    def __init__(self, t_lim, h_lim):
        self.hc = t_lim[1]
        self.lc = t_lim[0]
        self.tc = 0 # Value is set in values()
        self.hh = h_lim[1]
        self.lh = h_lim[0]
        self.h = 0 # Value is set in values()

    def values(self):
        """Returns the format parameters for this sensor"""
        self.tc = self.lc + (self.hc - self.lc) * random.random()
        self.h = self.lh + (self.hh - self.lh) * random.random()

        return (
            fahrenheit(self.tc),
            self.tc,
            fahrenheit(self.hc),
            self.hc,
            self.hc,
            fahrenheit(self.lc),
            self.lc,
            self.h,
            self.hh,
            self.lh,
            heat_index(self.h, self.tc),
            self.h,
            heat_index(self.hh, self.hc),
            self.hc,
            heat_index(self.lh, self.lc),
            self.lc)

def uptime():
    """Returns the system uptime in the format used by the roomalert"""
    with open('/proc/uptime', 'r') as f:
        seconds = int(float(f.readline().split()[0]))
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return '{}d {:02d}:{:02d}:{:02d}'.format(days, hours, minutes, seconds)

def spawn_server():
    """Spawns the fake webserver"""
    random.seed()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', PORT))
    sock.listen(1)

    ra = TemperatureHumiditySensor(ROOMALERT_TEMP, ROOMALERT_HUMIDITY)
    external = TemperatureHumiditySensor(EXTERNAL_TEMP, EXTERNAL_HUMIDITY)
    internal = TemperatureHumiditySensor(INTERNAL_TEMP, INTERNAL_HUMIDITY)
    truss = TemperatureSensor(TRUSS_TEMP)

    while True:
        conn, _ = sock.accept()
        request = conn.recv(4096)
        if request.startswith(b'GET /getData.htm HTTP'):
            date = datetime.datetime.utcnow().strftime('%m/%d/%y %H:%M:%S')
            ip = socket.gethostbyname(socket.gethostname())

            params = (date, uptime(), ip) + ra.values() + (0 if ON_BATTERY else 1,) + \
                external.values() + internal.values() + truss.values() + \
                (1 if HATCH_CLOSED else 0, 1 if TRAP_CLOSED else 0)

            response = DATA_TEMPLATE.format(*params)
            conn.sendall(response.encode('ascii'))
        else:
            conn.sendall('HTTP/1.1 404 ERROR\r\n\r\nERROR 404\r\n'.encode('ascii'))
        conn.close()

if __name__ == '__main__':
    spawn_server()
