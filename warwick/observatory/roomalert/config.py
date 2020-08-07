#
# This file is part of roomalertd
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

"""Helper function to validate and parse the json config file"""

import json
import sys
import traceback
import jsonschema
from warwick.observatory.common import daemons

LEGACY_SENSOR_TYPES = {
    'digital': ('sensor', float),
    'switch': ('switch_sen', bool)
}

MODERN_SENSOR_TYPES = {
    'digital': ('sensor', float),
    'internal': ('internal_sen', float),
    'switch': ('s_sen', bool)
}

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': ['daemon', 'log_name', 'query_ratelimit', 'roomalert_ip', 'roomalert_port', 'roomalert_query_timeout',
                 'roomalert_legacy_api', 'sensors'],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'query_ratelimit': {
            'type': 'number',
            'min': 0
        },
        'roomalert_ip': {
            'type': 'string',
        },
        'roomalert_port': {
            'type': 'number',
        },
        'roomalert_query_timeout': {
            'type': 'number',
            'min': 0
        },
        'roomalert_legacy_api': {
            'type': 'boolean'
        },
        'reboot_power_daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'reboot_power_switch': {
            'type': 'string'
        },
        'reboot_power_delay': {
            'type': 'number',
            'min': 5
        },
        'reboot_power_timeout': {
            'type': 'number',
            'min': 30
        },
        'sensors': {
            'type': 'array',
            'items': {
                'type': 'object',
                'additionalProperties': False,
                'required': ['id', 'type', 'index', 'key', 'label'],
                'properties': {
                    'id': {
                        'type': 'string',
                    },
                    'type': {
                        'type': 'string',
                        'enum': ['digital', 'internal', 'switch']
                    },
                    'index': {
                        'type': 'number',
                        'min': 0
                    },
                    'key': {
                        'type': 'string'
                    },
                    'label': {
                        'type': 'string',
                    },
                    'units': {
                        'type': 'string',
                    },
                    'values': {
                        'type': 'array',
                        'minItems': 2,
                        'maxItems': 2,
                        'items': {
                            'type': 'string'
                        }
                    },
                }
            }
        }
    }
}


class ConfigSchemaViolationError(Exception):
    """Exception used to report schema violations"""
    def __init__(self, errors):
        message = 'Invalid configuration:\n\t' + '\n\t'.join(errors)
        super(ConfigSchemaViolationError, self).__init__(message)


def __create_validator():
    """Returns a template validator that includes support for the
       custom schema tags used by the observation schedules:
            daemon_name: add to string properties to require they match an entry in the
                         warwick.observatory.common.daemons address book
    """
    validators = dict(jsonschema.Draft4Validator.VALIDATORS)

    # pylint: disable=unused-argument
    def daemon_name(validator, value, instance, schema):
        """Validate a string as a valid daemon name"""
        try:
            getattr(daemons, instance)
        except Exception:
            yield jsonschema.ValidationError('{} is not a valid daemon name'.format(instance))
    # pylint: enable=unused-argument

    validators['daemon_name'] = daemon_name
    return jsonschema.validators.create(meta_schema=jsonschema.Draft4Validator.META_SCHEMA,
                                        validators=validators)


def validate_config(config_json):
    """Tests whether a json object defines a valid environment config file
       Raises SchemaViolationError on error
    """
    errors = []
    try:
        validator = __create_validator()
        for error in sorted(validator(CONFIG_SCHEMA).iter_errors(config_json),
                            key=lambda e: e.path):
            if error.path:
                path = '->'.join([str(p) for p in error.path])
                message = path + ': ' + error.message
            else:
                message = error.message
            errors.append(message)
    except Exception:
        traceback.print_exc(file=sys.stdout)
        errors = ['exception while validating']

    if errors:
        raise ConfigSchemaViolationError(errors)


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validate_config(config_json)

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.query_ratelimit = config_json['query_ratelimit']
        self.roomalert_ip = config_json['roomalert_ip']
        self.roomalert_port = int(config_json['roomalert_port'])
        self.roomalert_query_timeout = int(config_json['roomalert_query_timeout'])
        self.roomalert_legacy_api = bool(config_json['roomalert_legacy_api'])
        self.sensors = config_json['sensors']

        self.reboot_power_daemon = None
        power_daemon = config_json.get('reboot_power_daemon', None)
        if power_daemon:
            self.reboot_power_daemon = getattr(daemons, power_daemon)

        self.reboot_power_switch = config_json.get('reboot_power_switch', None)
        self.reboot_power_delay = int(config_json.get('reboot_power_delay', 5))
        self.reboot_power_timeout = int(config_json.get('reboot_power_timeout', 30))

    def resolve_sensor_measurement(self, sensor, data):
        sensor_type = (LEGACY_SENSOR_TYPES if self.roomalert_legacy_api else MODERN_SENSOR_TYPES)[sensor['type']]
        return sensor_type[1](data[sensor_type[0]][sensor['index']][sensor['key']])
