## W1m/NITES/GOTO Room Alert daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/roomalertd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/roomalertd)

Part of the observatory software for the Warwick one-meter, NITES, and GOTO telescopes.

`roomalertd` is a Pyro proxy for querying the Room Alert via http.

`roomalert` is a commandline utility that queries the onemetre/GOTO/NITES Room Alert daemons.

`roomalertsim.py` (not packaged in a RPM) is a test script that emulates the W1m Room Alert as a legacy-style device.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup (W1m)

After installing `onemetre-roomalert-server`, the `roomalertd` must be enabled using:
```
sudo systemctl enable roomalertd.service
```

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start roomalertd.service
```

Finally, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=9008/tcp --permanent
sudo firewall-cmd --reload
```

### Software Setup (GOTO and SuperWASP)

Both the GOTO and SuperWASP roomalert daemons run on the same server.
After installing `goto-roomalert-server`, the `roomalertd`s must be enabled using:
```
sudo systemctl enable goto-roomalertd.service
sudo systemctl enable superwasp-roomalertd.service
```

The services will automatically start on system boot, or you can start them immediately using:
```
sudo systemctl start goto-roomalertd.service
sudo systemctl start superwasp-roomalertd.service
```

Finally, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=9020/tcp --permanent
sudo firewall-cmd --zone=public --add-port=9023/tcp --permanent
sudo firewall-cmd --reload
```

### Hardware Setup

The IPs for the Room Alert units are hardcoded in `roomalertd`.
