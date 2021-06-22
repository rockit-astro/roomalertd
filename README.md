## Room Alert daemon

`roomalertd` is a Pyro proxy for querying the Room Alert via http.

`roomalert` is a commandline utility that queries the Room Alert daemons.

See [Software Infrastructure](https://github.com/warwick-one-metre/docs/wiki/Software-Infrastructure) for an overview of the W1m software architecture and instructions for developing and deploying the code.

### Configuration

Configuration is read from json files that are installed by default to `/etc/roomalertd`.
A configuration file is specified when launching the Room Alert server, and the `roomalert` frontend will search for files matching the specified Room Alert when launched.

```python
{
  "daemon": "nites_roomalert", # Run the server as this daemon. Daemon types are registered in `warwick.observatory.common.daemons`.
  "log_name": "nites_roomalertd", # The name to use when writing messages to the observatory log.
  "query_ratelimit": 5, # Reuse cached values if additional queries are received within this many seconds of the last.
  "roomalert_ip": "10.2.6.187", # IP address of the Room Alert to query.
  "roomalert_port": 80, # Port of the Room Alert to query.
  "roomalert_query_timeout": 5, # Number of seconds allowed before a query fails.
  "roomalert_legacy_api": true, # Set true for older devices that return nonstandard json.
  "reboot_power_timeout": 30, # (optional) If defined, attempt to power cycle the Room Alert if it has not responded to queries in this many seconds.
  "reboot_power_daemon": "onemetre_power", # (optional) Power daemon name for power cycling the Room Alert.
  "reboot_power_switch": "roomalert", # (optional) Power daemon switch name for power cycling the Room Alert.
  "reboot_power_delay": 15, # (optional) Number of seconds to keep the Room Alert switched off when power cycling.
  "sensors": [ 
    {
      "id": "internal_temperature", # Key name in the output status.
      "label": "Internal Temp", # Human-readable display label for the output status.
      "units": "\u00B0C", # Human-readable display units for the output status.
      "type": "digital", # "digital" (1-wire RJ11 socket), "internal" for the internal temp/humidity sensors on non-legacy devices, or "switch" for the switch inputs on the back.
      "index": 0, # Sensor index in the roomalert sensors output array (each type has its own array in the roomalert output).
      "key": "tempc" # Sensor key in the roomalert sensor data.
    },
    {
      "id": "security_system",
      "label": "Tel. Sec. Sys",
      "values": ["TRIPPED", "SAFE"], # For "type": "digital", human-readable display labels for open and closed.
      "type": "switch",
      "index": 7,
      "key": "status"
    }
  ]
}
```

### Initial Installation

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package           | Description |
| ----------------- | ------ |
| observatory-roomalert-server | Contains the `roomalertd` server and systemd service file. |
| observatory-roomalert-client | Contains the `roomalert` commandline utility for controlling the Room Alert server. |
| python3-warwick-observatory-roomalert | Contains the python module with shared code. |
| observatory-roomalert-data | Contains the json configuration for all of the Room Alerts. |

The `observatory-roomalert-server`, `observatory-roomalert-client`, `observatory-roomalert-data` packages should be installed on the `gotoserver` machine (for SuperWASP and GOTO) and the `clasp-tcs` machine (for CLASP).
The `observatory-roomalert-client` and `observatory-roomalert-data` packages can also be installed on the 1m machines, but this now uses [domealertd](https://github.com/warwick-one-metre/domealertd) instead of a Room Alert.

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable roomalertd@<config>
sudo systemctl start roomalertd@<config>
```

where `config` is the name of the json file for the appropriate telescope.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `warwick.observatory.common.daemons` for the daemon specified in the json config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl stop roomalertd@<config>
sudo systemctl start roomalertd@<config>
```

### Testing Locally

The Room Alert server and client can be run directly from a git clone:
```
./roomalertd test.json
ROOMALERTD_CONFIG_ROOT=. ./roomalert test status
```
