"""Util Functions for ES Push."""
# Copyright 2016 Russell Troxel
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import certifi
import sys
import yaml


def _config(configfile):
    """Parse Yaml Config File."""
    try:
        with open(configfile, 'r') as f:
            conf = yaml.load(f)
    except IOError:
        # msg = "Could not open config file: {0}"
        # logging.info(msg.format(configfile))
        sys.exit(1)
    else:
        return conf


def _prepare_es_config(es_config):
    """Prepare elasticsearch config entry for use in py-elasticsearch."""
    es_config["http_auth"] = (
        es_config.pop("username"),
        es_config.pop("password")
    )
    es_config["ca_certs"] = certifi.where()
    return es_config
