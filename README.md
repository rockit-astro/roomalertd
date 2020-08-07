## W1m/NITES/GOTO Room Alert daemon [![Travis CI build status](https://travis-ci.org/warwick-one-metre/roomalertd.svg?branch=master)](https://travis-ci.org/warwick-one-metre/roomalertd)

Part of the observatory software for the Warwick one-meter, NITES, and GOTO telescopes.

`roomalertd` is a Pyro proxy for querying the Room Alert via http.

`roomalert` is a commandline utility that queries the onemetre/GOTO/NITES Room Alert daemons.

`roomalertsim.py` (not packaged in a RPM) is a test script that emulates the W1m Room Alert as a legacy-style device.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Software Setup

After installing `observatory-roomalert-server`, the `roomalertd` must be enabled using:
```
sudo systemctl enable roomalertd@<telescope>
```

where `<telescope>` can be `onemetre`, `nites`, `superwasp`, or `goto`.

The service will automatically start on system boot, or you can start it immediately using:
```
sudo systemctl start roomalertd@<telescope>
```

Finally, open a port in the firewall so that other machines on the network can access the daemon:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```

where `<port>` is (defined in the warwick-observatory-common daemon config):

| Telescope | Port |
| --------- | ---- |
| onemetre  | 9008 |
| NITES     | 9008 |
| SuperWASP | 9023 |
| GOTO      | 9020 |


### Configuration

The IPs and sensors to expose in each daemon are defined in the matching json files.
